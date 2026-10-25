"""
trainer.py
----------
Model training routine for Living-off-the-Land (LotL) attack detection.

Workflow:
  1. Load dataset CSV files (commands, tag).
  2. Extract features using WindowsFeaturePipeline or LinuxFeaturePipeline.
  3. Vectorize text features using CountVectorizer.
  4. Train a RandomForestClassifier.
  5. Evaluate performance on validation split.
  6. Persist model, vectorizer, and feature configuration.
"""

import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    accuracy_score, confusion_matrix, classification_report,
)

from src.features.pipeline import (
    WindowsFeaturePipeline, LinuxFeaturePipeline,
    MIN_LABELS_FOR_TRAINING,
)


def train(
    train_csv: str,
    val_csv: str,
    corpus_path: str,
    output_dir: str,
    platform: str = "windows",
    n_estimators: int = 100,
    n_jobs: int = -1,
    random_state: int = 42,
) -> dict:
    """
    Trains a RandomForest model for LotL attack detection.

    Args:
        train_csv    : Path to training CSV file.
        val_csv      : Path to validation CSV file.
        corpus_path  : Path to known command corpus for similarity check.
        output_dir   : Directory where model artifacts will be saved.
        platform     : "windows" or "linux".
        n_estimators : Number of trees in RandomForest.
        n_jobs       : Number of parallel jobs (-1 for all cores).
        random_state : Random seed for reproducibility.

    Returns:
        Dictionary of evaluation metrics on validation set.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("Building model")
    if platform == "windows":
        pipeline = WindowsFeaturePipeline(corpus_path=corpus_path)
    elif platform == "linux":
        pipeline = LinuxFeaturePipeline(corpus_path=corpus_path)
    else:
        raise ValueError(f"Unsupported platform: {platform}. Choose 'windows' or 'linux'.")

    print(f"Loading training data from {train_csv}")
    x_train_raw, y_train = _extract_features(train_csv, pipeline, training=True)

    print("::Fitting vectorizer")
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(x_train_raw)
    y_train_arr = np.array(y_train)

    print(f"Fitting classifier (n_estimators={n_estimators}, n_jobs={n_jobs})")
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        n_jobs=n_jobs,
        class_weight="balanced",
        random_state=random_state,
        verbose=0,
    )
    clf.fit(x_train, y_train_arr)

    print(f"Evaluating on validation data from {val_csv}")
    x_val_raw, y_val = _extract_features(val_csv, pipeline, training=False)
    x_val = vectorizer.transform(x_val_raw)
    y_val_arr = np.array(y_val)
    threshold = 0.35 if platform == "windows" else 0.60
    y_proba = clf.predict_proba(x_val)[:, 1]
    y_pred = np.array([
        1 if ("LOOKS_LIKE_KNOWN_LOL" in raw or prob >= threshold) else 0
        for raw, prob in zip(x_val_raw, y_proba)
    ])

    metrics = {
        "f1": round(f1_score(y_val_arr, y_pred), 4),
        "precision": round(precision_score(y_val_arr, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_val_arr, y_pred, zero_division=0), 4),
        "accuracy": round(accuracy_score(y_val_arr, y_pred), 4),
    }

    print("\n" + "=" * 50)
    print(f"F1 = {metrics['f1']}")
    print(f"Precision = {metrics['precision']}")
    print(f"Recall = {metrics['recall']}")
    print(f"Accuracy = {metrics['accuracy']}")
    print("\nConfusion matrix:")
    print(confusion_matrix(y_val_arr, y_pred))
    print("\nClassification report:")
    print(classification_report(y_val_arr, y_pred, target_names=["Good", "Bad"]))
    print("=" * 50)

    # Save standard artifacts
    clf_path = output_path / "rf_classifier.joblib"
    vec_path = output_path / "vectorizer.joblib"
    cfg_path = output_path / "feature_config.json"

    joblib.dump(clf, clf_path)
    joblib.dump(vectorizer, vec_path)

    # Also save libLOL-compatible names
    joblib.dump(clf, output_path / "model.classifier2")
    joblib.dump(vectorizer, output_path / "model.vectorizer")

    feature_names = vectorizer.get_feature_names_out().tolist()
    importances = clf.feature_importances_.tolist()
    top_features = sorted(
        [{"feature_id": i, "name": name, "importance_score": round(imp, 6)}
         for i, (name, imp) in enumerate(zip(feature_names, importances))],
        key=lambda x: x["importance_score"],
        reverse=True,
    )
    feature_config = {
        "platform": platform,
        "total_features": len(feature_names),
        "n_estimators": n_estimators,
        "val_metrics": metrics,
        "top_20_features": top_features[:20],
    }
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(feature_config, f, indent=2, ensure_ascii=False)

    print(f"Model saved to {clf_path}")
    print(f"Vectorizer saved to {vec_path}")
    print(f"Configuration saved to {cfg_path}")
    print("Done")

    return metrics


def _extract_features(csv_path: str, pipeline, training: bool) -> tuple:
    """
    Extracts features from commands in CSV file.
    """
    df = pd.read_csv(csv_path)
    if "commands" not in df.columns or "tag" not in df.columns:
        raise ValueError(f"CSV file must contain 'commands' and 'tag' columns: {csv_path}")

    x_raw = []
    y = []

    for command, tag in tqdm(zip(df["commands"], df["tag"]), total=len(df), desc="Extracting features"):
        command = str(command).strip()
        labels = pipeline(command, training=training)

        label_int = 0 if str(tag).strip().lower() == "good" else 1

        if training and label_int == 1 and len(labels) < MIN_LABELS_FOR_TRAINING:
            continue

        x_raw.append(" ".join(labels))
        y.append(label_int)

    print(f"Total samples: {len(y)} | Bad: {sum(y)} | Good: {len(y) - sum(y)}")
    return x_raw, y
