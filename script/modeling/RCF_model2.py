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

# === Paths & Setup ===
data_path = "../../data/datasets/panel_dataset_VIF_normalized.xlsx"
importance_dir = "../../data/feature_importance/full_dataset"
model_dir = "../../models/full_dataset"
metrics_dir = "../../data/evaluation_metrics/full_dataset"
drop_cols = ['date', 'Country']
targets = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
random_state = 42
test_size = 0.2

# === Ensure Output Folders Exist ===
os.makedirs(importance_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)
os.makedirs(metrics_dir, exist_ok=True)

# === Load Data ===
df = pd.read_excel(data_path)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Country', 'date'])

# === Results Container ===
all_results = []

# === Loop Over Targets ===
for target in targets:
    print(f"\n[INFO] Training model for target: {target}")

    if df[target].nunique() < 2:
        print(f"[SKIP] Not enough variation for {target}")
        continue

    X = df.drop(columns=drop_cols + targets, errors='ignore')
    y = df[target]

    stratify = y if y.nunique() == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )

    print(f"[INFO] Class balance (Train):\n{y_train.value_counts(normalize=True)}")
    print(f"[INFO] Class balance (Test):\n{y_test.value_counts(normalize=True)}")

    # === Train XGBoost Model
    model = XGBClassifier(
        n_estimators=100,
        use_label_encoder=False,
        eval_metric='logloss',
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
        random_state=random_state
    )
    model.fit(X_train, y_train)

    # === Predict Probabilities & Tune Threshold
    y_prob = model.predict_proba(X_test)[:, 1]
    best_thresh, best_f1 = 0.5, 0
    for t in np.arange(0.1, 0.9, 0.01):
        y_pred_thresh = (y_prob > t).astype(int)
        f1 = f1_score(y_test, y_pred_thresh)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t

    y_pred_final = (y_prob > best_thresh).astype(int)

    # === Evaluation
    auc = roc_auc_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred_final)
    recall = recall_score(y_test, y_pred_final)
    accuracy = accuracy_score(y_test, y_pred_final)

    print(f"[TUNE] Best Threshold = {best_thresh:.2f}")
    print(f"[EVAL] AUC = {auc:.3f}, Accuracy = {accuracy:.3f}, F1 = {best_f1:.3f}, Precision = {precision:.3f}, Recall = {recall:.3f}")

    # === SHAP
    explainer = shap.Explainer(model)
    shap_values = explainer(X_test)

    shap_df = pd.DataFrame(shap_values.values, columns=X_test.columns)
    mean_shap = shap_df.abs().mean().sort_values(ascending=False)

    print(f"\n🔍 Top features for {target} (XGBoost full dataset):")
    print(mean_shap.head(10))

    # === Save SHAP CSV
    mean_shap.to_csv(f"{importance_dir}/SHAP_ranked_features_{target}_ALL_XGB.csv")

    # === SHAP Summary Plots
    shap.summary_plot(shap_values, X_test, max_display=17, show=False)
    plt.title(f"SHAP Summary - {target}")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_summary_{target}_ALL_XGB.png")
    plt.clf()

    shap.summary_plot(shap_values, X_test, plot_type="bar", max_display=17, show=False)
    plt.title(f"SHAP Importance - {target}")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_bar_{target}_ALL_XGB.png")
    plt.clf()

    # === Save Feature Importance (XGBoost built-in)
    importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    importances.to_csv(f"{importance_dir}/XGB_importance_{target}_ALL.csv")

    # === Save Predictions
    pred_df = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": y_pred_final,
        "Probability": y_prob
    })
    pred_df.to_csv(f"{metrics_dir}/XGB_predictions_{target}_ALL.csv", index=False)

    # === Save Model
    joblib.dump(model, f"{model_dir}/XGB_model_{target}_ALL.pkl")

    # === Log Results
    all_results.append({
        "Target": target,
        "AUC": auc,
        "F1": best_f1,
        "Precision": precision,
        "Recall": recall,
        "Accuracy": accuracy,
        "Train_Size": len(y_train),
        "Test_Size": len(y_test),
        "Threshold": best_thresh
    })

# === Save Evaluation Summary
results_df = pd.DataFrame(all_results)
results_df.to_csv(f"{metrics_dir}/xgb_evaluation_full_dataset.csv", index=False)

print("\n[INFO] Full dataset evaluation results saved.")
print(results_df)
