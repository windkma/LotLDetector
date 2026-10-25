#
# Copyright (c) 2026 LotLDetector Project. All rights reserved.
# Dataset cleaning and stratified train/val/test splitting pipeline.
#

import sys
import argparse
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

COMMAND_COLS = ["commands", "cmd", "command", "line", "commandline"]
TAG_COLS = ["tag", "label", "target", "is_bad", "class"]


def parse_args():
    parser = argparse.ArgumentParser(description="Clean raw command dataset and perform stratified split")
    parser.add_argument(
        "--platform",
        choices=["windows", "linux"],
        default="windows",
        help="Platform target ('windows' or 'linux'). Sets default input/output paths.",
    )
    parser.add_argument("--raw-file", type=str, default=None, help="Custom path to raw CSV file")
    parser.add_argument("--output-dir", type=str, default=None, help="Custom output directory for processed CSVs")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train ratio (default: 0.8)")
    parser.add_argument("--val-ratio", type=float, default=0.1, help="Validation ratio (default: 0.1)")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Test ratio (default: 0.1)")
    parser.add_argument("--random-state", type=int, default=42, help="Random state seed (default: 42)")
    return parser.parse_args()


def clean_and_split():
    args = parse_args()

    # Determine default paths based on platform
    if args.raw_file:
        raw_path = Path(args.raw_file)
        if not raw_path.is_absolute():
            raw_path = RAW_DIR / args.raw_file
    else:
        raw_path = RAW_DIR / f"{args.platform}.csv"

    if args.output_dir:
        target_processed_dir = Path(args.output_dir)
    else:
        target_processed_dir = PROCESSED_DIR / args.platform

    target_processed_dir.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        print(f"Error: Raw CSV file not found: {raw_path}")
        sys.exit(1)

    print(f"Reading raw dataset: {raw_path}")
    try:
        df = pd.read_csv(raw_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    col_map = {col.lower(): col for col in df.columns}
    cmd_col = next((col_map[c] for c in COMMAND_COLS if c in col_map), None)
    tag_col = next((col_map[c] for c in TAG_COLS if c in col_map), None)

    if not cmd_col or not tag_col:
        print(f"Error: Unable to identify command and label columns. Available columns: {list(df.columns)}")
        sys.exit(1)

    print(f"Detected command column: '{cmd_col}' | label column: '{tag_col}'")
    df = df[[cmd_col, tag_col]].rename(columns={cmd_col: "commands", tag_col: "tag"})

    total_raw = len(df)
    df = df.dropna(subset=["commands", "tag"])
    df["commands"] = df["commands"].astype(str).str.strip()

    def normalize_tag(val):
        val_str = str(val).strip().lower()
        if val_str in ["1", "bad", "malicious", "true"]:
            return "bad"
        elif val_str in ["0", "good", "benign", "false"]:
            return "good"
        return None

    df["tag"] = df["tag"].apply(normalize_tag)
    df = df.dropna(subset=["tag"])
    df = df[df["commands"] != ""]
    df = df.drop_duplicates(subset=["commands"])

    cleaned_count = len(df)
    bad_count = sum(df["tag"] == "bad")
    good_count = sum(df["tag"] == "good")
    print(f"Cleaned samples: {cleaned_count} (filtered {total_raw - cleaned_count} duplicates/invalid)")
    print(f"Class distribution: {good_count} Good | {bad_count} Bad")

    val_test_ratio = args.val_ratio + args.test_ratio
    train_df, val_test_df = train_test_split(
        df,
        test_size=val_test_ratio,
        stratify=df["tag"],
        random_state=args.random_state,
    )

    relative_test_ratio = args.test_ratio / val_test_ratio
    val_df, test_df = train_test_split(
        val_test_df,
        test_size=relative_test_ratio,
        stratify=val_test_df["tag"],
        random_state=args.random_state,
    )

    train_path = target_processed_dir / "train.csv"
    val_path = target_processed_dir / "val.csv"
    test_path = target_processed_dir / "test.csv"

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print("\n" + "=" * 50)
    print(f"Dataset preparation complete [{args.platform}]:")
    print(f"  Train : {len(train_df):>5} samples -> {train_path}")
    print(f"  Val   : {len(val_df):>5} samples -> {val_path}")
    print(f"  Test  : {len(test_df):>5} samples -> {test_path}")
    print("=" * 50)


if __name__ == "__main__":
    clean_and_split()
