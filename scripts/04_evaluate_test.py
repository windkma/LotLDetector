#
# Copyright (c) 2026 LotLDetector Project. All rights reserved.
# Standalone model evaluation on unseen test datasets.
#

import sys
import os
import argparse
import pandas as pd
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.predictor import LotLPredictor


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate LotLDetector model on test dataset")
    parser.add_argument("--platform", choices=["windows", "linux"], default="windows", help="Target platform")
    parser.add_argument("--test-file", type=str, default=None, help="Optional custom test CSV file path")
    parser.add_argument("--threshold", type=float, default=None, help="Custom probability threshold")
    return parser.parse_args()


def main():
    args = parse_args()
    data_dir = PROJECT_ROOT / "data"

    if args.test_file:
        test_csv = Path(args.test_file)
    else:
        test_csv = data_dir / "processed" / args.platform / "test.csv"

    model_dir = str(PROJECT_ROOT / "models" / args.platform)
    ext_dir = data_dir / "external"
    corpus_file = "cmd_known.corpus" if args.platform == "windows" else "bash_known.corpus"
    corpus_path = str(ext_dir / corpus_file)

    if not test_csv.exists():
        print(f"Error: Test file not found: {test_csv}")
        sys.exit(1)

    print(f"\n{'=' * 65}")
    print(f"  LotLDetector - Test Evaluation")
    print(f"  Platform  : {args.platform.upper()}")
    print(f"  Test CSV  : {test_csv}")
    print(f"  Model Dir : {model_dir}")
    print(f"{'=' * 65}\n")

    predictor = LotLPredictor(
        model_dir=model_dir,
        corpus_path=corpus_path if os.path.exists(corpus_path) else None,
        platform=args.platform,
        threshold=args.threshold,
    )
    print(f"Decision threshold: {predictor.threshold}\n")

    df = pd.read_csv(test_csv)
    col = "commands" if "commands" in df.columns else "command"
    tag_col = "tag" if "tag" in df.columns else "label"

    commands = df[col].tolist()
    true_labels = [1 if str(t).strip().lower() in ["bad", "1"] else 0 for t in df[tag_col]]

    print(f"Scanning and evaluating {len(commands)} commands...")
    results = predictor.predict_batch(commands)
    pred_labels = [1 if r["verdict"] == "BAD" else 0 for r in results]

    print("\n" + "=" * 55)
    print("  CLASSIFICATION REPORT")
    print("=" * 55)
    print(classification_report(true_labels, pred_labels, target_names=["Good/Neutral", "Bad"]))

    cm = confusion_matrix(true_labels, pred_labels)
    tn, fp, fn, tp = cm.ravel()
    print("=" * 55)
    print("  CONFUSION MATRIX")
    print("=" * 55)
    print(f"  True Negative  (TN) : {tn:>5}")
    print(f"  False Positive (FP) : {fp:>5}")
    print(f"  False Negative (FN) : {fn:>5}")
    print(f"  True Positive  (TP) : {tp:>5}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
