# Model Summaries: Logistic Regression, Random Forest, XGBoost, and LSTM

---

## Logistic Regression


- A linear model used for **binary classification**, modeling the probability that a given input belongs to a certain class using the **logistic (sigmoid) function**.
- The output is a probability between 0 and 1, which is thresholded to make a classification.
- It assumes a **linear relationship** between the features and the log-odds of the target.
- Works well on linearly separable datasets; regularization (L1 or L2) can help prevent overfitting.
  - Requires **feature scaling** to perform well.


*Reference:*  
- Müller & Guido, Ch. 2, Supervised Learning, pp. 45–50  
- Deitel & Deitel, Ch. 19, Scikit-learn for Machine Learning, pp. 733–736  

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
```

---

## Random Forest


- An **ensemble learning method** that builds many decision trees using **bootstrap samples** and averages their predictions.
- Introduces randomness through:
  - Bootstrap sampling of the data.
  - Random subset of features considered at each split.
- Great for handling overfitting compared to single trees.
- Supports both classification and regression tasks.
- Doesn’t require much preprocessing; robust to outliers and feature scaling.

 *Reference:*  
- Müller & Guido, Ch. 2, Supervised Learning, pp. 69–72  
- Deitel & Deitel, Ch. 19, Ensemble Learning, pp. 752–754  

**Import example (Scikit-learn):**
```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
```
---

## XGBoost


- A high-performance implementation of **gradient boosting**, where models are built sequentially and each tries to correct the errors of the previous.
- Regularized to prevent overfitting and optimized for speed with parallelization.
- Known for strong performance on structured/tabular data, especially in competitions.
- Automatically handles missing values and supports early stopping and custom loss functions.

*Reference:*  
- Géron, Ch. 7, Ensemble Learning and Random Forests, pp. 241–247  

**Import example (XGBoost):**
```python
import xgboost as xgb
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
```


---

## LSTM (Long Short-Term Memory)


- A specialized type of **Recurrent Neural Network (RNN)** designed to capture long-term dependencies in sequential data.
- Avoids the **vanishing gradient problem** through memory cells and gating mechanisms (input, forget, and output gates).
- Well-suited for tasks like time series forecasting, NLP, speech recognition, and more.
- Typically requires more training time and data but captures complex patterns over time.

 *Reference:*  
- Géron, Ch. 15, Recurrent Neural Networks, pp. 459–471  

**Import example (Keras via TensorFlow):**
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
model.add(LSTM(50, input_shape=(timesteps, features)))
model.add(Dense(1, activation='sigmoid'))  # For binary classification
```



