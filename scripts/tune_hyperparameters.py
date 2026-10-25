#
# Copyright (c) 2026 LotLDetector Project. All rights reserved.
# Hyperparameter tuning module for Random Forest (Tree depth, Leaf size, Estimator count).
#

import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.pipeline import WindowsFeaturePipeline, LinuxFeaturePipeline


def parse_args():
    parser = argparse.ArgumentParser(description="Tune Random Forest hyperparameters using GridSearchCV")
    parser.add_argument("--platform", choices=["windows", "linux"], default="windows", help="Target platform")
    parser.add_argument("--cv", type=int, default=3, help="Number of cross-validation folds (default: 3)")
    return parser.parse_args()


def main():
    args = parse_args()
    data_dir = PROJECT_ROOT / "data"
    train_csv = data_dir / "processed" / args.platform / "train.csv"
    ext_dir = data_dir / "external"

    corpus_file = "cmd_known.corpus" if args.platform == "windows" else "bash_known.corpus"
    corpus_path = str(ext_dir / corpus_file)

    if not train_csv.exists():
        print(f"Error: Train CSV not found: {train_csv}")
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print(f"  LotLDetector - Random Forest Hyperparameter Tuning")
    print(f"  Platform : {args.platform.upper()}")
    print(f"  Dataset  : {train_csv}")
    print(f"  CV Folds : {args.cv}")
    print(f"{'=' * 70}\n")

    if args.platform == "windows":
        pipeline = WindowsFeaturePipeline(corpus_path=corpus_path)
    else:
        pipeline = LinuxFeaturePipeline(corpus_path=corpus_path)

    df_train = pd.read_csv(train_csv)
    col = "commands" if "commands" in df_train.columns else "command"
    tag_col = "tag" if "tag" in df_train.columns else "label"

    commands = df_train[col].tolist()
    y_train = np.array([1 if str(t).strip().lower() in ["bad", "1"] else 0 for t in df_train[tag_col]])

    print(f"Extracting features for {len(commands)} training samples...")
    raw_features = []
    for cmd in commands:
        labels = pipeline(str(cmd).strip(), training=True)
        raw_features.append(" ".join(labels))

    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(raw_features)

    # Grid search parameter space:
    # 1. n_estimators     : Number of trees in forest
    # 2. max_depth        : Maximum depth of each tree (None = fully grown)
    # 3. min_samples_leaf : Minimum samples required at leaf node
    # 4. max_features     : Number of features to consider when looking for the best split
    param_grid = {
        "n_estimators": [50, 100, 150],
        "max_depth": [15, 30, None],
        "min_samples_leaf": [1, 2, 4],
    }

    print("\nRunning GridSearchCV across hyperparameter grid:")
    for k, v in param_grid.items():
        print(f"  - {k:<18}: {v}")
    print(f"  Total combinations : {len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_leaf'])} models x {args.cv} folds")
    print("  Optimizing scoring : F1-Score (balanced)\n")

    skf = StratifiedKFold(n_splits=args.cv, shuffle=True, random_state=42)
    rf = RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1, verbose=0)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring="f1",
        cv=skf,
        n_jobs=-1,
        verbose=1,
    )

    grid_search.fit(X_train, y_train)

    print("\n" + "=" * 70)
    print("  GRID SEARCH RESULTS (Top 5 Parameter Configurations)")
    print("=" * 70)
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df = results_df.sort_values(by="mean_test_score", ascending=False)

    top5 = results_df[["param_n_estimators", "param_max_depth", "param_min_samples_leaf", "mean_test_score", "std_test_score"]].head(5)
    print(f"{'n_estimators':>12} | {'max_depth':>10} | {'min_samples_leaf':>16} | {'Mean F1':>8} | {'Std Dev':>8}")
    print("-" * 70)
    for _, r in top5.iterrows():
        depth_str = str(r['param_max_depth']) if r['param_max_depth'] is not None else "None"
        print(f"{r['param_n_estimators']:>12} | {depth_str:>10} | {r['param_min_samples_leaf']:>16} | {r['mean_test_score']:>8.4f} | {r['std_test_score']:>8.4f}")
    print("=" * 70)

    print(f"\nBest Parameters Found:")
    print(f"  * n_estimators     : {grid_search.best_params_['n_estimators']}")
    print(f"  * max_depth        : {grid_search.best_params_['max_depth']}")
    print(f"  * min_samples_leaf : {grid_search.best_params_['min_samples_leaf']}")
    print(f"  * Best Cross-Val F1: {grid_search.best_score_:.4f}\n")


if __name__ == "__main__":
    main()

