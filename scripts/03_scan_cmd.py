#
# Copyright (c) 2026 LotLDetector Project. All rights reserved.
# Command scanning CLI utility.
#

import sys
import os
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.predictor import LotLPredictor


def parse_args():
    parser = argparse.ArgumentParser(description="Scan command lines for LotL attack patterns")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--cmd", type=str, help="Single command string to analyze")
    group.add_argument("--file", type=str, help="Text file with commands (one per line)")
    parser.add_argument("--platform", choices=["windows", "linux"], default="windows", help="Target platform")
    parser.add_argument("--threshold", type=float, default=None, help="Custom detection probability threshold")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose feature inspection")
    return parser.parse_args()


def print_result(result: dict, verbose: bool = False) -> None:
    features = " ".join(result["labels"]) if result["labels"] else "(none)"
    print("=" * 60)
    print(f"Command     : {result['command']}")
    print(f"Verdict     : {result['verdict']}")
    print(f"Probability : {result['probability']:.4f}")
    print(f"Features    : {features}")
    print("=" * 60)


def main():
    args = parse_args()
    model_dir = str(PROJECT_ROOT / "models" / args.platform)
    ext_dir = PROJECT_ROOT / "data" / "external"

    corpus_file = "cmd_known.corpus" if args.platform == "windows" else "bash_known.corpus"
    corpus_path = str(ext_dir / corpus_file)

    try:
        predictor = LotLPredictor(
            model_dir=model_dir,
            corpus_path=corpus_path if os.path.exists(corpus_path) else None,
            platform=args.platform,
            threshold=args.threshold,
        )
    except Exception as e:
        print(f"Error loading model from {model_dir}: {e}")
        print("Please train a model first using scripts/02_train.py")
        sys.exit(1)

    if args.cmd:
        result = predictor.predict(args.cmd)
        print_result(result, verbose=args.verbose)
    elif args.file:
        cmd_file = Path(args.file)
        if not cmd_file.exists():
            print(f"File not found: {cmd_file}")
            sys.exit(1)

        with open(cmd_file, "r", encoding="utf-8", errors="ignore") as f:
            commands = [l.strip() for l in f if l.strip()]

        print(f"Scanning {len(commands)} commands...")
        results = predictor.predict_batch(commands)
        bad_count = sum(1 for r in results if r["verdict"] == "BAD")
        for res in results:
            if res["verdict"] == "BAD" or args.verbose:
                print_result(res, verbose=args.verbose)

        print(f"\nSummary: {len(commands)} scanned | {bad_count} BAD | {len(commands) - bad_count} GOOD/NEUTRAL")
    else:
        # Interactive REPL mode matching libLOL conventions
        print(f"LotLDetector interactive mode [{args.platform}]")
        print("Type a command and press Enter to scan. Type 'exit' to quit.\n")
        while True:
            try:
                sys.stdout.write(">>> ")
                sys.stdout.flush()
                cmd_line = input()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            cmd_line = cmd_line.strip()
            if cmd_line in ("exit", "quit"):
                break
            if not cmd_line:
                continue

            result = predictor.predict(cmd_line)
            print_result(result, verbose=args.verbose)
            print()


if __name__ == "__main__":
    main()
