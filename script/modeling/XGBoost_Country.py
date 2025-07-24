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
importance_dir = "../../data/feature_importance/per_country"
model_dir = "../../models/per_country"
metrics_dir = "../../data/evaluation_metrics/per_country"
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

# === Loop Over Countries and Targets ===
for country in df['Country'].unique():
    df_country = df[df['Country'] == country].copy()
    print(f"\n==============================")
    print(f"[INFO] Processing country: {country}")

    for target in targets:
        print(f"\n[INFO] Training model for target: {target}")

        # Skip if not enough variation
        if df_country[target].nunique() < 2:
            print(f"[SKIP] Not enough variation for {target} in {country}")
            continue

        X = df_country.drop(columns=drop_cols + targets, errors='ignore')
        y = df_country[target]

        stratify = y if y.nunique() == 2 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=stratify
        )

        print(f"[INFO] Class balance (Train):\n{y_train.value_counts(normalize=True)}")
        print(f"[INFO] Class balance (Test):\n{y_test.value_counts(normalize=True)}")

        # === Train Model
        model = XGBClassifier(
            n_estimators=100,
            use_label_encoder=False,
            eval_metric='logloss',
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
            random_state=random_state
        )
        model.fit(X_train, y_train)

        # === Predict and Threshold Tuning
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

        print(f"\n🔍 Top features for {target} in {country}:")
        print(mean_shap.head(10))

        # === Save Outputs
        base_name = f"{target}_{country.upper()}_XGB"

        mean_shap.to_csv(f"{importance_dir}/SHAP_ranked_features_{base_name}.csv")
        shap.summary_plot(shap_values, X_test, max_display=17, show=False)
        plt.title(f"SHAP Summary - {base_name}")
        plt.tight_layout()
        plt.savefig(f"{metrics_dir}/SHAP_summary_{base_name}.png")
        plt.clf()

        shap.summary_plot(shap_values, X_test, plot_type="bar", max_display=17, show=False)
        plt.title(f"SHAP Importance - {base_name}")
        plt.tight_layout()
        plt.savefig(f"{metrics_dir}/SHAP_bar_{base_name}.png")
        plt.clf()

        importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
        importances.to_csv(f"{importance_dir}/XGB_importance_{base_name}.csv")

        pred_df = pd.DataFrame({
            "Actual": y_test.values,
            "Predicted": y_pred_final,
            "Probability": y_prob
        })
        pred_df.to_csv(f"{metrics_dir}/XGB_predictions_{base_name}.csv", index=False)

        joblib.dump(model, f"{model_dir}/XGB_model_{base_name}.pkl")

        all_results.append({
            "Country": country,
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
results_df.to_csv(f"{metrics_dir}/xgb_evaluation_per_country.csv", index=False)

print("\n[INFO] Per-country evaluation results saved.")
print(results_df)
