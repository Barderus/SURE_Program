import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib


# Load Data
df = pd.read_excel("../../data/summary_tables/panel_dataset_normalized.xlsx")

# Common Setup
drop_cols = ['date', 'Country']
targets = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
random_state = 42

def train_xgb_for_target(target):
    print(f"\nTraining XGBoost for: {target}")

    X = df.drop(columns=drop_cols + targets)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    xgb = XGBClassifier(n_estimators=100, eval_metric='logloss', random_state=random_state)
    xgb.fit(X_train, y_train)

    # Feature importance
    importances = pd.Series(xgb.feature_importances_, index=X_train.columns).sort_values(ascending=False)

    # Save importances to CSV
    importances.to_csv(f"../../data/feature_importance/XGBOOST_{target}_importance.csv")

    # Plot
    importances.head(20).plot(kind='barh')
    plt.title(f"Top 20 Features - XGBoost - {target}")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    # Save the model
    joblib.dump(xgb, f"../../models/XGB_model_{target}.pkl")


    return importances

# Run for All Targets
for target in targets:
    train_xgb_for_target(target)
