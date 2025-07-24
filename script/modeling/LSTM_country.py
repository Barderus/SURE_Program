import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.callbacks import EarlyStopping
import os

# --- Load dataset ---
data_path = "../../data/datasets/panel_dataset_VIF_normalized.xlsx"
df = pd.read_excel(data_path)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

target_col = 'INF (%)'

for country, group in df.groupby("Country"):
    group = group.reset_index(drop=True)

    # Decide whether to use month_sin/cos
    if country in ['JAP', 'GER']:
        exclude_cols = ['date', 'Country', 'RECESS', 'RECESS_PERIOD', 'RECESS_OVER', 'month', target_col]
    else:
        exclude_cols = ['date', 'Country', 'RECESS', 'RECESS_PERIOD', 'RECESS_OVER', 'month',
                        target_col, 'month_sin', 'month_cos']  # drop seasonal features

    feature_cols = [col for col in group.columns if col not in exclude_cols]


# Make sure 'month_sin' and 'month_cos' are included

df.dropna(subset=feature_cols + [target_col], inplace=True)
df.sort_values(['Country', 'date'], inplace=True)


# Early stopping configuration
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)


# --- Create sequences for each country ---
def create_sequences(data, feature_cols, time_steps=12):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[feature_cols].iloc[i:i+time_steps].values)
        y.append(data[target_col].iloc[i + time_steps])
    return np.array(X), np.array(y)


# --- Define Model Builders ---
def build_lstm(input_shape):
    model = Sequential([
        LSTM(64, input_shape=input_shape, return_sequences=False),
        Dropout(0.3),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


def build_bilstm(input_shape):
    model = Sequential([
        Bidirectional(LSTM(64, return_sequences=False), input_shape=input_shape),
        Dropout(0.4),  # Slightly higher for more complex model
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


def build_stacked_lstm(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(32, return_sequences=False),
        Dropout(0.3),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


# --- Loop through countries and train all 3 models ---
results = []

for country, group in df.groupby("Country"):
    group = group.reset_index(drop=True)

    if len(group) < 24:
        print(f"Skipping {country}: insufficient data")
        continue

    X, y = create_sequences(group, feature_cols=feature_cols, time_steps=12)
    if len(X) < 30:
        print(f"Skipping {country}: too few sequences")
        continue

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    architectures = {
        "LSTM": build_lstm,
        "BiLSTM": build_bilstm,
        "StackedLSTM": build_stacked_lstm
    }

    for arch_name, build_fn in architectures.items():
        model = build_fn((X.shape[1], X.shape[2]))
        model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.1, verbose=0, callbacks=[early_stop])

        y_pred = model.predict(X_test).flatten()
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        print(f"📍 {country} | {arch_name} | MAE: {mae:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f}")
        results.append({
            'Country': country,
            'Architecture': arch_name,
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2
        })


# --- Save summary ---
results_df = pd.DataFrame(results)
results_df.to_csv("lstm_per_country_results.csv", index=False)
print("\n✅ Saved: lstm_per_country_results.csv")
