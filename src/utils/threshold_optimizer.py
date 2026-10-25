"""
threshold_optimizer.py
----------------------
Empirical decision threshold calibration module for imbalanced cybersecurity detection.

Provides grid-sweep optimization across probability thresholds [0.05 - 0.95]
to balance Recall, Precision, False Positive Rate (FPR), and F1-Score.

References:
- Provost & Fawcett (2001): Robust Classification for Imbalanced Datasets
- Davis & Goadrich (ICML 2006): The Relationship Between PR and ROC Curves
- Adobe libLOL (IoTBDS 2022): Section 3.1 & 4.1 on FP suppression in enterprise SOC
"""

import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def evaluate_threshold_sweep(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    raw_features: list = None,
    thresholds: list = None,
) -> pd.DataFrame:
    """
    Evaluates classification performance across multiple probability thresholds.

    Args:
        y_true       : True binary labels (0: Good, 1: Bad).
        y_proba      : Predicted probability scores for Class 1 (Bad).
        raw_features : Optional list of raw feature strings to apply BLEU override.
        thresholds   : List of float thresholds to sweep (default: 0.10 to 0.90 with step 0.05).

    Returns:
        pd.DataFrame containing threshold, precision, recall, f1, fpr, accuracy, and confusion counts.
    """
    if thresholds is None:
        thresholds = [round(t, 2) for t in np.arange(0.10, 0.95, 0.05)]

    y_true = np.array(y_true)
    y_proba = np.array(y_proba)

    records = []
    for th in thresholds:
        if raw_features is not None:
            y_pred = np.array([
                1 if ("LOOKS_LIKE_KNOWN_LOL" in raw or prob >= th) else 0
                for raw, prob in zip(raw_features, y_proba)
            ])
        else:
            y_pred = (y_proba >= th).astype(int)

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        acc = accuracy_score(y_true, y_pred)
        # Youden's Index J = Sensitivity + Specificity - 1 = Recall - FPR
        youden_j = rec - fpr

        records.append({
            "threshold": th,
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "fpr": round(float(fpr), 4),
            "accuracy": round(acc, 4),
            "youden_j": round(youden_j, 4),
            "tp": int(tp),
            "fp": int(fp),
            "fn": int(fn),
            "tn": int(tn),
        })

    return pd.DataFrame(records)


def find_optimal_threshold(df_sweep: pd.DataFrame, target_metric: str = "f1") -> dict:
    """
    Finds the optimal threshold record maximizing the target metric.
    """
    best_idx = df_sweep[target_metric].idxmax()
    return df_sweep.iloc[best_idx].to_dict()

