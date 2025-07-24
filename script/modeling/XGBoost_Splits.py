### This model tests the accuracy of K-fold, Rolling Window, Data range, sequential data range
from xgboost import XGBClassifier
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
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

def train_xgb_model(X_train, y_train, X_test, y_test, country, target, split_type, suffix=""):
    print(f"[INFO] Class balance (Train):\n{y_train.value_counts(normalize=True)}")
    print(f"[INFO] Class balance (Test):\n{y_test.value_counts(normalize=True)}")

    # === Skip if training set has only one class
    if len(np.unique(y_train)) < 2:
        print(f"[SKIP] Cannot train XGB model for {country} - {target} ({split_type}) — only one class in training data.")
        return

    model = XGBClassifier(
        n_estimators=100,
        use_label_encoder=False,
        eval_metric='logloss',
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum() if (y_train == 1).sum() != 0 else 1,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]

    best_thresh, best_f1 = 0.5, 0
    for t in np.arange(0.1, 0.9, 0.01):
        y_pred_thresh = (y_prob > t).astype(int)
        f1 = f1_score(y_test, y_pred_thresh)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t
    y_pred_final = (y_prob > best_thresh).astype(int)

    auc = roc_auc_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred_final)
    recall = recall_score(y_test, y_pred_final)
    accuracy = accuracy_score(y_test, y_pred_final)

    print(f"[TUNE] Best Threshold = {best_thresh:.2f}")
    print(f"[EVAL] AUC = {auc:.3f}, F1 = {best_f1:.3f}, Precision = {precision:.3f}, Recall = {recall:.3f}, Accuracy = {accuracy:.3f}")

    model_filename = f"{model_dir}/XGB_model_{target}_{country}_{suffix}.pkl"
    joblib.dump(model, model_filename)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap_to_plot = shap_values[1] if isinstance(shap_values, list) else shap_values
    shap_class_1 = shap_to_plot[:, :, 1] if shap_to_plot.ndim == 3 else shap_to_plot

    shap.summary_plot(shap_class_1, X_test, max_display=17, show=False)
    plt.title(f"SHAP Summary - XGB - {target} ({country})")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_summary_XGB_{target}_{country}_{suffix}.png")
    plt.close()

    shap.summary_plot(shap_class_1, X_test, plot_type="bar", max_display=17, show=False)
    plt.title(f"SHAP Importance - XGB - {target} ({country})")
    plt.tight_layout()
    plt.savefig(f"{metrics_dir}/SHAP_bar_XGB_{target}_{country}_{suffix}.png")
    plt.close()

    top_features = pd.Series(
        np.abs(shap_class_1).mean(axis=0),
        index=X_test.columns
    ).sort_values(ascending=False)
    top_features.to_csv(f"{importance_dir}/SHAP_top_XGB_{target}_{country}_{suffix}.csv")

    pred_df = pd.DataFrame({
        "Country": country,
        "Target": target,
        "Actual": y_test.values,
        "Predicted": y_pred_final,
        "Probability": y_prob
    })
    pred_df.to_csv(f"{metrics_dir}/XGB_predictions_{target}_{country}_{suffix}.csv", index=False)

    all_results.append({
        "Country": country,
        "Target": target,
        "Split_Type": f"{split_type}_XGB",
        "AUC": auc,
        "F1": best_f1,
        "Precision": precision,
        "Recall": recall,
        "Accuracy": accuracy,
        "Train_Size": len(y_train),
        "Test_Size": len(y_test),
        "Threshold": best_thresh
    })

def split_by_date_XGB(df, country, target, split_date='2010-01-01'):
    country_df = df[df['Country'] == country].copy()
    country_df = country_df.sort_values('date')

    if len(country_df[target].unique()) < 2:
        print(f"[SKIP] Not enough label variation in {country} - {target}")
        return

    train_df = country_df[country_df['date'] < split_date]
    test_df = country_df[country_df['date'] >= split_date]

    if len(train_df) < 30 or len(test_df) < 10:
        print(f"[SKIP] Not enough data in train/test sets for {country} - {target}")
        return

    X_train = train_df.drop(columns=drop_cols + targets)
    y_train = train_df[target]
    X_test = test_df.drop(columns=drop_cols + targets)
    y_test = test_df[target]

    print(f"\n[DATE SPLIT - XGB] {country} - {target} | Split at {split_date}")
    train_xgb_model(X_train, y_train, X_test, y_test, country, target,
                    split_type='sample_date', suffix='date')

def rolling_window_split_XGB(df, country, target,
                             initial_train_frac=0.6,
                             test_size=12,
                             step=3):
    country_df = df[df['Country'] == country].copy()
    country_df = country_df.sort_values('date')

    if len(country_df[target].unique()) < 2:
        print(f"[SKIP] Not enough label variation in {country} - {target}")
        return

    total_len = len(country_df)
    initial_train_len = int(total_len * initial_train_frac)

    start = 0
    iteration = 0
    while start + initial_train_len + test_size <= total_len:
        train_end = start + initial_train_len
        test_end = train_end + test_size

        train_df = country_df.iloc[start:train_end]
        test_df = country_df.iloc[train_end:test_end]

        X_train = train_df.drop(columns=drop_cols + targets)
        y_train = train_df[target]
        X_test = test_df.drop(columns=drop_cols + targets)
        y_test = test_df[target]

        print(f"\n[ROLLING - XGB] {country} - {target} | Window {iteration + 1}")
        train_xgb_model(X_train, y_train, X_test, y_test, country, target,
                        split_type='rolling_XGB', suffix=f'roll{iteration+1}')
        iteration += 1
        start += step

def get_sequential_split_XGB(df, country, target, split_date='2010-01-01'):
    country_df = df[df['Country'] == country].copy()
    country_df = country_df.sort_values('date')

    if len(country_df[target].unique()) < 2:
        print(f"[SKIP] Not enough variation in {country} - {target}")
        return

    X = country_df.drop(columns=drop_cols + targets)
    y = country_df[target]

    X_train = X[country_df['date'] < split_date]
    X_test = X[country_df['date'] >= split_date]
    y_train = y[country_df['date'] < split_date]
    y_test = y[country_df['date'] >= split_date]

    if len(y_train) < 30 or len(y_test) < 10:
        print(f"[SKIP] Not enough data for sequential split {country} - {target}")
        return

    print(f"\n[SEQUENTIAL SPLIT - XGB] {country} - {target} | Split at {split_date}")
    train_xgb_model(X_train, y_train, X_test, y_test, country, target,
                    split_type='sequential_XGB', suffix='seq')

def kfold_timeseries_split_XGB(df, country, target, k=5):
    country_df = df[df['Country'] == country].copy()
    country_df = country_df.sort_values('date')

    if len(country_df[target].unique()) < 2:
        print(f"[SKIP] Not enough label variation in {country} - {target}")
        return

    X = country_df.drop(columns=drop_cols + targets)
    y = country_df[target]

    tscv = TimeSeriesSplit(n_splits=k)
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        print(f"\n[K-FOLD - XGB] {country} - {target} | Fold {fold + 1}/{k}")
        train_xgb_model(X_train, y_train, X_test, y_test, country, target,
                        split_type='kfold_XGB', suffix=f'kfold{fold+1}')


print("\n----------------------ROLLING WINDOW (XGB) ---------------------")
for country in df['Country'].unique():
    for target in targets:
        rolling_window_split_XGB(df, country, target)

print("\n -------------------- SEQUENTIAL SPLIT (XGB) -------------------------")
for country in df['Country'].unique():
    for target in targets:
        get_sequential_split_XGB(df, country, target)

print("\n----------------------K-FOLD (XGB, k=5) ---------------------")
for country in df['Country'].unique():
    for target in targets:
        kfold_timeseries_split_XGB(df, country, target, k=5)

print("\n-------------- SPLIT BY DATE (XGBoost) --------------------")
for country in df['Country'].unique():
    for target in targets:
        split_by_date_XGB(df, country, target)  # duplicate that calls train_xgb_model

results_df = pd.DataFrame(all_results)
results_df.to_csv(f"{metrics_dir}/xgb_model_evaluation_all_splits.csv", index=False)

summary = (
    results_df
    .groupby("Split_Type")[["AUC", "F1", "Precision", "Recall", "Accuracy", "Threshold"]]
    .mean()
    .round(3)
    .reset_index()
)

print("\n\n📊 Average Model Performance by XGBoost Splitting Strategy:")
print(summary.to_string(index=False))