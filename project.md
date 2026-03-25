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
network-ids-ml/
├── data/
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
- Label encoding for categorical features (protocol_type, service, flag)
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

> *(Fill in after training)*

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | - | - | - | - |
| Decision Tree | - | - | - | - |
| Random Forest | - | - | - | - |
| XGBoost | - | - | - | - |

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
Download `KDDTrain+.txt` and `KDDTest+.txt` from [UNB](https://www.unb.ca/cic/datasets/nsl.html) and place them in the `data/` folder.

### 4. Run the notebooks in order
```bash
jupyter notebook
```
Open `notebooks/01_eda.ipynb` and work through them in sequence.

---

## Requirements

```
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
jupyter
```

---

## Key Findings

> *(Fill in after analysis)*

- Most common attack type in the dataset: ...
- Best performing model: ...
- Most important features: ...

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
