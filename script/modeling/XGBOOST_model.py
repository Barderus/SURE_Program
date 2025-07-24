import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score,
    recall_score, accuracy_score
)
import shap
import joblib
import os

# === Paths ===
DATA_PATH = "../../data/datasets/panel_dataset_VIF_normalized.xlsx"
MODEL_DIR = "../../models"
IMPORTANCE_DIR = "../../data/feature_importance"
SHAP_DIR = "../../data/shap_values"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(IMPORTANCE_DIR, exist_ok=True)
os.makedirs(SHAP_DIR, exist_ok=True)

# === Config ===
DROP_COLS = ['date', 'Country']
TARGETS = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
RANDOM_STATE = 42
TEST_SIZE = 0.2

# === Load Data ===
df = pd.read_excel(DATA_PATH)

# === Results Container ===
all_results = []

def train_xgboost_with_shap(target):
    print(f"\n[INFO] Training XGBoost for target: {target}")

    X = df.drop(columns=DROP_COLS + TARGETS)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # === Train Model ===
    model = XGBClassifier(
        n_estimators=100,
        eval_metric='logloss',
        random_state=RANDOM_STATE,
        use_label_encoder=False
    )
    model.fit(X_train, y_train)

    # === Predict Probabilities
    y_prob = model.predict_proba(X_test)[:, 1]

    # === Find Best Threshold
    best_thresh, best_f1 = 0.5, 0
    for t in np.arange(0.1, 0.9, 0.01):
        y_pred = (y_prob > t).astype(int)
        f1 = f1_score(y_test, y_pred)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t

    # Final Predictions
    y_pred_final = (y_prob > best_thresh).astype(int)

    # === Evaluate
    auc = roc_auc_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred_final)
    recall = recall_score(y_test, y_pred_final)
    accuracy = accuracy_score(y_test, y_pred_final)

    print(f"[TUNE] Best Threshold = {best_thresh:.2f}")
    print(f"[EVAL] AUC = {auc:.3f}, Accuracy = {accuracy:.3f}, F1 = {best_f1:.3f}, Precision = {precision:.3f}, Recall = {recall:.3f}")

    # === Log Results
    all_results.append({
        "Target": target,
        "AUC": auc,
        "F1": best_f1,
        "Precision": precision,
        "Recall": recall,
        "Accuracy": accuracy,
        "Threshold": best_thresh
    })

    # === Feature Importance ===
    importances = pd.Series(
        model.feature_importances_, index=X_train.columns
    ).sort_values(ascending=False)

    importance_path = os.path.join(IMPORTANCE_DIR, f"XGB_{target}_importance.csv")
    importances.to_csv(importance_path)
    print(f"[INFO] Feature importance saved: {importance_path}")

    # === SHAP Explanation ===
    explainer = shap.Explainer(model)
    shap_values = explainer(X_train)

    shap_df = pd.DataFrame(shap_values.values, columns=X_train.columns)
    mean_shap = shap_df.abs().mean().sort_values(ascending=False)
    mean_shap.to_csv(os.path.join(SHAP_DIR, f"XGB_SHAP_{target}.csv"))
    print(f"[INFO] SHAP values saved for {target}")

    # === SHAP Summary Plot (Top 20)
    shap.plots.bar(shap_values[:, :20], show=True)

    # === Save Model
    model_path = os.path.join(MODEL_DIR, f"XGB_model_{target}.pkl")
    joblib.dump(model, model_path)
    print(f"[INFO] Model saved: {model_path}")

# === Run for All Targets
for target in TARGETS:
    train_xgboost_with_shap(target)

# === Print Summary Table
summary_df = pd.DataFrame(all_results)
print("\n========== XGBoost Model Summary ==========")
print(summary_df.round(3).to_string(index=False))
