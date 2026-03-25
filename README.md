# Network Intrusion Detection System (IDS) with Machine Learning

> Detecting malicious network traffic using classical ML models trained on the NSL-KDD dataset.

---

## Problem Statement

Network intrusion detection is a critical component of modern cybersecurity. Traditional rule-based systems struggle to adapt to novel attack patterns. This project applies supervised machine learning to classify network traffic as either **normal** or **malicious**, and further categorizes attack types (DoS, Probe, R2L, U2R).

---

## Dataset

**NSL-KDD** — an improved version of the KDD Cup 1999 dataset, widely used in IDS research.

- Source: [University of New Brunswick](https://www.unb.ca/cic/datasets/nsl.html)
- Training set: `KDDTrain+.txt`
- Test set: `KDDTest+.txt`
- Features: 41 network connection features (duration, protocol type, flag, bytes, etc.)
- Labels: Binary (normal / attack) and multi-class (DoS, Probe, R2L, U2R)

---

## Project Structure

```
IDS_System/
├── NSLKDD/
│   ├── KDDTrain+.txt
│   └── KDDTest+.txt
├── notebooks/
│   ├── 01_eda.ipynb          # Exploratory data analysis
│   ├── 02_preprocessing.ipynb
│   └── 03_modelling.ipynb
├── src/
│   ├── preprocess.py         # Data cleaning and feature engineering
│   ├── train.py              # Model training
│   └── evaluate.py           # Evaluation metrics and plots
├── models/
│   └── (saved .pkl model files)
├── requirements.txt
└── README.md
```

---

## Approach

### 1. Exploratory Data Analysis
- Class distribution analysis
- Feature correlation heatmap
- Attack type breakdown

### 2. Preprocessing
- Label encoding for categorical features (`protocol_type`, `service`, `flag`)
- Normalization with `StandardScaler`
- Binary and multi-class label mapping

### 3. Models

| Model | Type | Notes |
|---|---|---|
| Logistic Regression | Baseline | Fast, interpretable |
| Decision Tree | Baseline | Good for feature importance |
| Random Forest | Main | High accuracy, robust |
| XGBoost | Main | Best overall performance |
| MLP Classifier | Stretch | Neural network baseline |

---

## Results

### Binary Classification (Normal vs. Attack)

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.754 | 0.925 | 0.618 | 0.741 |
| Decision Tree | 0.788 | 0.965 | 0.651 | 0.777 |
| Random Forest | 0.770 | 0.966 | 0.618 | 0.753 |
| XGBoost | **0.801** | **0.968** | **0.673** | **0.794** |
| MLP | 0.795 | 0.972 | 0.660 | 0.786 |

### Multi-class Classification (DoS / Probe / R2L / U2R / Normal)

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.762 | 0.759 | 0.762 | 0.715 |
| Decision Tree | 0.769 | 0.810 | 0.769 | 0.736 |
| Random Forest | 0.751 | 0.814 | 0.751 | 0.709 |
| XGBoost | **0.772** | **0.823** | **0.772** | **0.733** |
| MLP | 0.754 | 0.798 | 0.754 | 0.710 |

XGBoost achieves the best performance on both tasks. Precision is consistently high (~96–97%) while recall is moderate (~65–67%), meaning the models are conservative — they rarely produce false alarms but miss some attacks. This reflects the inherent difficulty of the NSL-KDD test set, which is designed to be harder than the training set.

Confusion matrices and ROC curves are available in the `notebooks/` folder.

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/network-ids-ml.git
cd network-ids-ml
```

### 2. Set up the environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add the dataset
Place the NSL-KDD files in the `NSLKDD/` folder:
```
NSLKDD/
├── KDDTrain+.txt
└── KDDTest+.txt
```

### 4. Run the notebooks in order
```bash
jupyter notebook
```
Open `notebooks/01_eda.ipynb` and work through them in sequence.

---

## Requirements

See `requirements.txt`.

---

## Key Findings

- Most common attack type: **neptune** (DoS — SYN flood), making up the majority of attack traffic
- Best performing model: **XGBoost** — highest accuracy and F1 on both binary and multi-class tasks
- Precision is high (~96%) but recall is moderate (~67%), reflecting the challenge of the NSL-KDD test set
- Most informative features: `dst_host_same_src_port_rate`, `dst_host_srv_count`, `serror_rate`, `src_bytes`

---

## Capturing Your Own Network Data

The NSL-KDD dataset contains **connection-level features** (not raw packets). To apply this model to real traffic, you need two stages:

### Stage 1 — Capture Raw Packets

Use `tcpdump` or Wireshark to record traffic on your network interface:

```bash
# List available interfaces
ifconfig

# Capture traffic and save to a .pcap file
sudo tcpdump -i en0 -w capture.pcap
```

`en0` is typically the WiFi interface on macOS. Wireshark provides the same capability with a GUI.

### Stage 2 — Convert Packets to Connection Features

Raw packets must be aggregated into per-connection statistics matching the model's 41 input features. Use **CICFlowMeter** (developed by the same UNB lab behind NSL-KDD):

```bash
./cfm capture.pcap output_folder/
```

This produces a `.csv` where each row is one network flow with ~80 features (duration, byte counts, packet rates, flag counts, etc.). A mapping layer in `preprocess.py` would align these to the NSL-KDD feature set.

### Full Pipeline

```
Your network
    ↓
tcpdump / Wireshark  →  capture.pcap
    ↓
CICFlowMeter         →  flows.csv  (one row per connection)
    ↓
preprocess.py        →  scaled feature matrix
    ↓
trained model        →  "normal" / "attack"
```

### Legal Note

Only capture traffic on **your own network**. For safe testing, set up a local VM lab and generate synthetic attack traffic against your own machines using tools like `nmap` (port scanning → Probe) or `hping3` (DoS simulation). This is the same methodology used to build the CICIDS2017 dataset.

---

## Limitations & Future Work

- The NSL-KDD dataset is from 1999 — modern attack patterns differ significantly
- Future work: test on newer datasets (CICIDS2017, UNSW-NB15)
- Potential extension: deploy as a real-time packet classification API using FastAPI

---

## References

- Tavallaee et al. (2009) — *A Detailed Analysis of the KDD CUP 99 Data Set*
- Scikit-learn documentation: https://scikit-learn.org
- NSL-KDD dataset: https://www.unb.ca/cic/datasets/nsl.html

---

## Disclaimer

This project is developed for educational purposes as part of a Master's-level course in AI for Cyber Security at Kristiania University of Applied Sciences. It is not intended for use in production security environments.
