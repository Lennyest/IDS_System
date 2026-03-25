import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

BINARY_MODELS = {
    "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
    "decision_tree": DecisionTreeClassifier(random_state=42),
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "xgboost": XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss", n_jobs=-1),
    "mlp": MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=200, random_state=42),
}


def train_all(X_train, y_train, label_type: str = "binary", save: bool = True):
    os.makedirs(MODELS_DIR, exist_ok=True)
    results = {}

    # XGBoost needs integer labels for multi-class
    if label_type == "multi":
        le = LabelEncoder()
        y_encoded = le.fit_transform(y_train)
    else:
        y_encoded = y_train
        le = None

    for name, model in BINARY_MODELS.items():
        print(f"Training {name} ({label_type})...")
        if name == "xgboost" and label_type == "multi":
            model.set_params(objective="multi:softprob", num_class=len(le.classes_))
        model.fit(X_train, y_encoded)
        results[name] = model
        if save:
            path = os.path.join(MODELS_DIR, f"{name}_{label_type}.pkl")
            joblib.dump(model, path)
            print(f"  Saved to {path}")

    if le is not None:
        joblib.dump(le, os.path.join(MODELS_DIR, f"label_encoder_{label_type}.pkl"))

    return results, le


def load_model(name: str, label_type: str = "binary"):
    path = os.path.join(MODELS_DIR, f"{name}_{label_type}.pkl")
    return joblib.load(path)
