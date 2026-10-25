"""
metrics.py
----------
Evaluation metrics and report utilities for binary classification models.
"""

import numpy as np
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    accuracy_score, confusion_matrix,
)


def compute_metrics(y_true: list, y_pred: list) -> dict:
    """
    Computes standard performance metrics for binary classification.

    Args:
        y_true: Ground truth labels (0: Good, 1: Bad).
        y_pred: Predicted labels.

    Returns:
        Dictionary containing f1, precision, recall, accuracy, fpr, and confusion counts.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "fpr": round(float(fpr), 6),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
    }


def print_metrics(metrics: dict, title: str = "Evaluation Metrics") -> None:
    """Prints evaluation metrics cleanly formatted."""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")
    print(f"  F1-Score  : {metrics['f1']}")
    print(f"  Precision : {metrics['precision']}")
    print(f"  Recall    : {metrics['recall']}")
    print(f"  Accuracy  : {metrics['accuracy']}")
    print(f"  FPR       : {metrics['fpr']:.6f}")
    print("\n  Confusion Matrix:")
    print(f"    TP: {metrics['tp']}  |  FP: {metrics['fp']}")
    print(f"    FN: {metrics['fn']}  |  TN: {metrics['tn']}")
    print(f"{'=' * 50}\n")
