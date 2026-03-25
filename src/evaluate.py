import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    RocCurveDisplay,
)
import pandas as pd


def compute_metrics(y_true, y_pred, average="binary"):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
        "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
        "f1": f1_score(y_true, y_pred, average=average, zero_division=0),
    }


def evaluate_all(models: dict, X_test, y_test, label_type: str = "binary", le=None):
    rows = []
    for name, model in models.items():
        if le is not None:
            y_pred_enc = model.predict(X_test)
            y_pred = le.inverse_transform(y_pred_enc)
            avg = "weighted"
        else:
            y_pred = model.predict(X_test)
            avg = "binary"
        metrics = compute_metrics(y_test, y_pred, average=avg)
        metrics["model"] = name
        rows.append(metrics)
        print(f"\n{name}:")
        print(classification_report(y_test, y_pred, zero_division=0))
    return pd.DataFrame(rows).set_index("model")[["accuracy", "precision", "recall", "f1"]]


def plot_confusion_matrix(y_true, y_pred, labels, title="Confusion Matrix", ax=None):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(title)
    return ax


def plot_roc_curves(models: dict, X_test, y_test):
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, model in models.items():
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, "decision_function"):
            y_proba = model.decision_function(X_test)
        else:
            continue
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, label=f"{name} (AUC={roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves")
    ax.legend(loc="lower right")
    plt.tight_layout()
    return fig


def plot_feature_importance(model, feature_names, top_n=20, title="Feature Importance"):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        raise ValueError("Model does not have feature_importances_")
    indices = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(top_n), importances[indices])
    ax.set_xticks(range(top_n))
    ax.set_xticklabels([feature_names[i] for i in indices], rotation=45, ha="right")
    ax.set_title(title)
    plt.tight_layout()
    return fig
