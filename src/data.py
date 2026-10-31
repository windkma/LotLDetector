"""Read labeled commands, split them, and export the numerical training data."""
import csv

import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import SEED, paths


def load_train_test(platform):
    """Read labeled commands and split directly into 90% train and 10% test."""
    frame = pd.read_csv(
        paths(platform)["dataset"],
        dtype={"commands": str, "label": str},
        keep_default_na=False,
    )
    if list(frame.columns) != ["commands", "label"]:
        raise ValueError("Dataset must have exactly two columns: commands,label.")
    if frame["commands"].str.strip().eq("").any():
        raise ValueError("Dataset contains empty commands; correct the input CSV.")
    if not frame["label"].isin(["0", "1"]).all():
        raise ValueError("Labels must be 0 (good) or 1 (bad).")
    frame["label"] = frame["label"].astype(int)
    if set(frame["label"]) != {0, 1}:
        raise ValueError("Dataset must contain both labels 0 and 1.")
    return train_test_split(
        frame, test_size=0.1, stratify=frame["label"], random_state=SEED,
    )


def save_training_dataset(path, source_rows, commands, targets, matrix, feature_names):
    """Write the exact X/y passed to fit, with source rows for traceability.

    The feature columns follow vectorizer order. Only one dense row is created
    at a time; the complete feature matrix remains sparse in memory.
    """
    if matrix.shape != (len(targets), len(feature_names)):
        raise ValueError("Feature matrix shape does not match targets and feature names.")
    if len(source_rows) != len(targets) or len(commands) != len(targets):
        raise ValueError("Source rows, commands and targets must have equal lengths.")
    matrix = matrix.tocsr()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Replace only after the entire CSV has been written successfully.
    temporary = path.with_suffix(".csv.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow([
                "source_index", "commands", "label",
                *[f"feature:{name}" for name in feature_names],
            ])
            for row_index, (source_index, command, target) in enumerate(
                zip(source_rows, commands, targets)
            ):
                values = [0] * matrix.shape[1]
                start, end = matrix.indptr[row_index:row_index + 2]
                for column, value in zip(matrix.indices[start:end], matrix.data[start:end]):
                    values[int(column)] = int(value)
                writer.writerow([int(source_index), command, int(target), *values])
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
