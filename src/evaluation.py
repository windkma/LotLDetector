"""Report classification metrics for held-out test predictions."""
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score,
)


def report(y_true, results):
    y_true = list(y_true)
    predictions = [int(result["verdict"] == "BAD") for result in results]
    print(classification_report(
        y_true, predictions, labels=[0, 1],
        target_names=["Good/Neutral", "Bad"], digits=4, zero_division=0,
    ))
    tn, fp, fn, tp = confusion_matrix(y_true, predictions, labels=[0, 1]).ravel()
    neutral = sum(result["verdict"] == "NEUTRAL" for result in results)
    neutral_bad = sum(
        result["verdict"] == "NEUTRAL" and target == 1
        for result, target in zip(results, y_true)
    )
    print(f"TN={tn} FP={fp} FN={fn} TP={tp}")
    print(f"NEUTRAL={neutral} (including {neutral_bad} BAD samples)")
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
    }
