import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
df = pd.read_csv("gold_data.csv", delimiter=';')

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns:", df.columns)

# Convert date
df['date'] = pd.to_datetime(df['date'])

# Feature engineering
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Moving averages
df['ma_7'] = df['close'].rolling(7).mean()
df['ma_30'] = df['close'].rolling(30).mean()

# Remove null rows
df = df.dropna()

# ✅ DEFINE X and y (IMPORTANT)
X = df[['open','high','low','ma_7','ma_30','day','month','year']]
y = df['close']

# Train model
model = RandomForestRegressor(n_estimators=200)
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained successfully")