import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


# Load Data
df = pd.read_excel("../../data/summary_tables/panel_dataset_normalized.xlsx")

# Common Setup
drop_cols = ['date', 'Country']
targets = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
random_state = 42

def train_rf_for_target(target):
    print(f"\nTraining Random Forest for: {target}")

    X = df.drop(columns=drop_cols + targets)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    rf = RandomForestClassifier(n_estimators=100, random_state=random_state)
    rf.fit(X_train, y_train)

    # Feature importance
    importances = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)

    # Save importances to CSV
    importances.to_csv(f"../../data/feature_importance/RFC_{target}_importance.csv")


    # Plot
    importances.head(20).plot(kind='barh')
    plt.title(f"Top 20 Features - RFC - {target}")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    # Save the model
    joblib.dump(rf, f"../../models/RFC_model_{target}.pkl")


    return importances

# Run for All Targets
for target in targets:
    train_rf_for_target(target)
