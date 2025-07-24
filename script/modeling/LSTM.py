import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
import matplotlib.pyplot as plt
from tensorflow.python.keras.callbacks import EarlyStopping

# --- Load and Prepare Data ---
data_path = "../../data/datasets/panel_dataset_VIF_normalized.xlsx"
df = pd.read_excel(data_path)
df['date'] = pd.to_datetime(df['date'])

target_col = 'RECESS'
exclude_cols = ['date', 'Country', 'RECESS', 'RECESS_PERIOD', 'RECESS_OVER', target_col]
feature_cols = [col for col in df.columns if col not in exclude_cols]

df.dropna(subset=feature_cols + [target_col], inplace=True)
df['country_id'] = LabelEncoder().fit_transform(df['Country'])
feature_cols.append('country_id')
df.sort_values(['Country', 'date'], inplace=True)

# Early stopping configuration
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

# --- Create LSTM Sequences ---
def create_lstm_sequences(data, time_steps=24):
    X, y = [], []
    for _, group in data.groupby('Country'):
        group = group.reset_index(drop=True)
        for i in range(len(group) - time_steps):
            X.append(group.loc[i:i+time_steps-1, feature_cols].values)
            y.append(group.loc[i + time_steps, target_col])
    return np.array(X), np.array(y)

X, y = create_lstm_sequences(df)
split = int(len(X) * 0.8)
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

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



# --- Train and Evaluate Helper ---
def train_and_evaluate(model, name, X_train, y_train, X_test, y_test):
    print(f"\n🔧 Training {name} model...")
    model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.1, verbose=0, callbacks=[early_stop])

    y_pred = model.predict(X_test).flatten()
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\n📊 {name} Model Performance")
    print("---------------------------------------")
    print(f"MAE:        {mae:.4f}")
    print(f"RMSE:       {rmse:.4f}")
    print(f"R² Score:   {r2:.4f}")
    print("---------------------------------------")

    return y_pred, {'mae': mae, 'rmse': rmse, 'r2': r2}

# --- Train Both Models ---
lstm_model = build_lstm((X.shape[1], X.shape[2]))
bilstm_model = build_bilstm((X.shape[1], X.shape[2]))

y_pred_lstm, metrics_lstm = train_and_evaluate(lstm_model, "Standard LSTM", X_train, y_train, X_test, y_test)
y_pred_bilstm, metrics_bilstm = train_and_evaluate(bilstm_model, "Bidirectional LSTM", X_train, y_train, X_test, y_test)

stacked_lstm_model = build_stacked_lstm((X.shape[1], X.shape[2]))
y_pred_stacked, metrics_stacked = train_and_evaluate(
    stacked_lstm_model, "Stacked LSTM", X_train, y_train, X_test, y_test
)

# --- Plot Comparison ---
plt.figure(figsize=(12, 5))
plt.plot(y_test, label='Actual', alpha=0.6)
plt.plot(y_pred_lstm, label='LSTM', linestyle='--')
plt.plot(y_pred_bilstm, label='BiLSTM', linestyle=':')
plt.plot(y_pred_stacked, label='Stacked LSTM', linestyle='-.')
plt.title("Inflation Prediction: LSTM Model Comparison")
plt.xlabel("Test Samples")
plt.ylabel("Normalized Inflation")
plt.legend()
plt.tight_layout()
plt.show()

