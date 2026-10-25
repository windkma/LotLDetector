#
# Copyright (c) 2026 LotLDetector Project. All rights reserved.
# Training CLI entrypoint.
#

import sys
import os
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.trainer import train


def parse_args():
    parser = argparse.ArgumentParser(description="Train LotLDetector detection model")
    parser.add_argument("--platform", choices=["windows", "linux"], default="windows", help="Target platform")
    parser.add_argument("--n-estimators", type=int, default=100, help="Number of trees in RandomForest")
    parser.add_argument("--train-csv", type=str, default=None, help="Custom train CSV path")
    parser.add_argument("--val-csv", type=str, default=None, help="Custom validation CSV path")
    return parser.parse_args()


def main():
    args = parse_args()
    data_dir = PROJECT_ROOT / "data"

    ext_dir = data_dir / "external"
    corpus_file = "cmd_known.corpus" if args.platform == "windows" else "bash_known.corpus"
    corpus_path = str(ext_dir / corpus_file)

    proc_dir = data_dir / "processed" / args.platform
    train_csv = args.train_csv or str(proc_dir / "train.csv")
    val_csv = args.val_csv or str(proc_dir / "val.csv")
    model_dir = str(PROJECT_ROOT / "models" / args.platform)

    print(f"\n{'=' * 60}")
    print(f"  LotLDetector Training Pipeline")
    print(f"  Platform     : {args.platform}")
    print(f"  Train CSV    : {train_csv}")
    print(f"  Val CSV      : {val_csv}")
    print(f"  Corpus Path  : {corpus_path}")
    print(f"  Output Dir   : {model_dir}")
    print(f"  N-Estimators : {args.n_estimators}")
    print(f"{'=' * 60}\n")

    metrics = train(
        train_csv=train_csv,
        val_csv=val_csv,
        corpus_path=corpus_path,
        output_dir=model_dir,
        platform=args.platform,
        n_estimators=args.n_estimators,
        n_jobs=-1,
    )

    print(f"\nTraining complete: F1={metrics['f1']}, Recall={metrics['recall']}, Accuracy={metrics['accuracy']}")


if __name__ == "__main__":
    main()
