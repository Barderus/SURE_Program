# Compare Feature Importances from RFC and XGBoost
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load All Feature Importances for All Targets
folder_path = "../../data/feature_importance"
targets = ["recess", "recess_over", "recess_period"]

for target in targets:
    # Build file paths
    rfc_path = os.path.join(folder_path, f"RFC_{target}_importance.csv")
    xgb_path = os.path.join(folder_path, f"XGBOOST_{target}_importance.csv")

    # Load CSVs
    rfc_importances = pd.read_csv(rfc_path, index_col=0, header=None, names=["Feature", "RFC_Importance"])
    xgb_importances = pd.read_csv(xgb_path, index_col=0, header=None, names=["Feature", "XGB_Importance"])

    # Merge and normalize
    merged = pd.merge(rfc_importances, xgb_importances, left_index=True, right_index=True, how="outer")
    merged.fillna(0, inplace=True)
    merged['RFC_Importance'] /= merged['RFC_Importance'].sum()
    merged['XGB_Importance'] /= merged['XGB_Importance'].sum()

    # Top N features
    top_n = 20
    top_features = merged.sort_values(by=["RFC_Importance", "XGB_Importance"], ascending=False).head(top_n)

    # Melt for plotting
    plot_df = top_features.reset_index().melt(id_vars="Feature",
                                              value_vars=["RFC_Importance", "XGB_Importance"],
                                              var_name="Model", value_name="Importance")

    # Plot
    plt.figure(figsize=(10, 8))
    sns.barplot(data=plot_df, y="Feature", x="Importance", hue="Model")
    plt.title(f"Top {top_n} Feature Importances: RFC vs XGBoost for {target.upper()}")
    plt.tight_layout()
    output_path = os.path.join("../../images/modeling", f"feature_importance_comparison_{target}.png")
    plt.savefig(output_path)
    plt.show()
