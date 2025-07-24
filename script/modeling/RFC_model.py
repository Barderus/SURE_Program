### RCF PER COUNTRY
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split
import shap
import numpy as np
import joblib
import os

# === Paths & Setup ===
data_path = "../../data/datasets/panel_dataset_VIF_normalized.xlsx"
importance_dir = "../../data/feature_importance"
model_dir = "../../models"
metrics_dir = "../../data/evaluation_metrics"
drop_cols = ['date', 'Country']
targets = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
random_state = 42
test_size = 0.2

# === Ensure Output Directories Exist ===
os.makedirs(importance_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)
os.makedirs(metrics_dir, exist_ok=True)

# === Load Data ===
df = pd.read_excel(data_path)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Country', 'date'])

# === Evaluation Results Container ===
all_results = []



def train_rf_random_split(df, country, target):
    print(f"\n[INFO] Training {target} model for {country}...")

    country_df = df[df['Country'] == country].copy()

    # Skip if not enough variation
    if len(country_df[target].unique()) < 2:
        print(f"[SKIP] Not enough label variation in {country} - {target}")
        return

    X = country_df.drop(columns=drop_cols + targets, errors='ignore')
    print("Features used in model:", X.columns.tolist())
    y = country_df[target]

    # Train-test split
    stratify = y if y.nunique() == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )

    # Log class balance
    print(f"[INFO] Class balance (Train):\n{y_train.value_counts(normalize=True)}")
    print(f"[INFO] Class balance (Test):\n{y_test.value_counts(normalize=True)}")

    # Train model with class_weight
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=random_state)
    model.fit(X_train, y_train)

    # Predict probabilities
    y_prob = model.predict_proba(X_test)[:, 1]

    # Tune threshold
    best_thresh, best_f1 = 0.5, 0
    for t in np.arange(0.1, 0.9, 0.01):
        y_pred_thresh = (y_prob > t).astype(int)
        f1 = f1_score(y_test, y_pred_thresh)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t
    y_pred_final = (y_prob > best_thresh).astype(int)

    # Evaluate
    auc = roc_auc_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred_final)
    recall = recall_score(y_test, y_pred_final)
    accuracy = accuracy_score(y_test, y_pred_final)

    print(f"[TUNE] Best Threshold = {best_thresh:.2f}")
    print(f"[EVAL] AUC = {auc:.3f}, F1 = {best_f1:.3f}, Precision = {precision:.3f}, Recall = {recall:.3f}, Accuracy = {accuracy:.3f}")

    # Save model
    joblib.dump(model, f"{model_dir}/RFC_model_{target}_{country}_weighted.pkl")

    # SHAP explainability
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap_to_plot = shap_values[1] if isinstance(shap_values, list) and len(shap_values) == 2 else shap_values

    # Save SHAP plots
    shap.summary_plot(shap_to_plot, X_test, max_display=17, show=False)
    plt.title(f"SHAP Summary - {target} ({country})")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_summary_{target}_{country}_weighted.png")
    plt.close()

    shap.summary_plot(shap_to_plot, X_test, plot_type="bar" ,max_display=17, show=False)
    plt.title(f"SHAP Importance - {target} ({country})")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_bar_{target}_{country}_weighted.png")
    plt.close()

    # Save top SHAP features
    # If shap_to_plot has shape (n_samples, n_features, 2), slice class 1 before mean
    if shap_to_plot.ndim == 3:
        shap_class_1 = shap_to_plot[:, :, 1]
    else:
        shap_class_1 = shap_to_plot  # Already 2D (n_samples, n_features)

    shap_mean_importance = np.abs(shap_class_1).mean(axis=0)
    top_features = pd.Series(shap_mean_importance, index=X_test.columns).sort_values(ascending=False)
    top_features = pd.Series(shap_mean_importance, index=X_test.columns).sort_values(ascending=False)
    top_features.to_csv(f"{importance_dir}/SHAP_top_{target}_{country}_weighted.csv")

    # Save predictions
    pred_df = pd.DataFrame({
        "Country": country,
        "Target": target,
        "Actual": y_test.values,
        "Predicted": y_pred_final,
        "Probability": y_prob
    })
    pred_df.to_csv(f"{metrics_dir}/RFC_predictions_{target}_{country}_weighted.csv", index=False)

    # Log results
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

# === Loop Through All Countries and Targets ===
for country in df['Country'].unique():
    for target in targets:
        train_rf_random_split(df, country, target)

# === Save Summary ===
results_df = pd.DataFrame(all_results)
results_df.to_csv(f"{metrics_dir}/rfc_evaluation_by_country.csv", index=False)

print("\nEvaluation results saved.")
print(results_df)
