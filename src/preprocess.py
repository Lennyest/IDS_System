import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"
]

CATEGORICAL_COLS = ["protocol_type", "service", "flag"]

# Map multi-class attack categories
ATTACK_MAP = {
    "normal": "normal",
    # DoS
    "back": "DoS", "land": "DoS", "neptune": "DoS", "pod": "DoS",
    "smurf": "DoS", "teardrop": "DoS", "mailbomb": "DoS", "apache2": "DoS",
    "processtable": "DoS", "udpstorm": "DoS",
    # Probe
    "ipsweep": "Probe", "nmap": "Probe", "portsweep": "Probe", "satan": "Probe",
    "mscan": "Probe", "saint": "Probe",
    # R2L
    "ftp_write": "R2L", "guess_passwd": "R2L", "imap": "R2L", "multihop": "R2L",
    "phf": "R2L", "spy": "R2L", "warezclient": "R2L", "warezmaster": "R2L",
    "sendmail": "R2L", "named": "R2L", "snmpgetattack": "R2L", "snmpguess": "R2L",
    "xlock": "R2L", "xsnoop": "R2L", "worm": "R2L",
    # U2R
    "buffer_overflow": "U2R", "loadmodule": "U2R", "perl": "U2R", "rootkit": "U2R",
    "httptunnel": "U2R", "ps": "U2R", "sqlattack": "U2R", "xterm": "U2R",
}


def load_data(train_path: str, test_path: str):
    train = pd.read_csv(train_path, header=None, names=COLUMNS)
    test = pd.read_csv(test_path, header=None, names=COLUMNS)
    return train, test


def encode_categoricals(df: pd.DataFrame, encoders: dict = None, fit: bool = True):
    df = df.copy()
    if encoders is None:
        encoders = {}
    for col in CATEGORICAL_COLS:
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
        else:
            le = encoders[col]
            df[col] = le.transform(df[col])
    return df, encoders


def add_labels(df: pd.DataFrame):
    df = df.copy()
    df["binary_label"] = (df["label"] != "normal").astype(int)
    df["attack_category"] = df["label"].map(ATTACK_MAP).fillna("other")
    return df


def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def preprocess(train_path: str, test_path: str):
    train, test = load_data(train_path, test_path)

    train = add_labels(train)
    test = add_labels(test)

    train, encoders = encode_categoricals(train, fit=True)
    test, _ = encode_categoricals(test, encoders=encoders, fit=False)

    feature_cols = [c for c in COLUMNS if c not in ("label", "difficulty")]
    X_train = train[feature_cols]
    X_test = test[feature_cols]
    y_train_bin = train["binary_label"]
    y_test_bin = test["binary_label"]
    y_train_multi = train["attack_category"]
    y_test_multi = test["attack_category"]

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    return {
        "X_train": X_train_scaled,
        "X_test": X_test_scaled,
        "y_train_bin": y_train_bin,
        "y_test_bin": y_test_bin,
        "y_train_multi": y_train_multi,
        "y_test_multi": y_test_multi,
        "feature_cols": feature_cols,
        "encoders": encoders,
        "scaler": scaler,
    }
