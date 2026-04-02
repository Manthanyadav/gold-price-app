import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load dataset
df = pd.read_csv("gold_data.csv", sep=";")

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# Convert date
df['date'] = pd.to_datetime(df['date'])

# Feature engineering
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Moving averages
df['ma_7'] = df['close'].rolling(7).mean()
df['ma_30'] = df['close'].rolling(30).mean()

df = df.dropna()

# Features & target
X = df[['open','high','low','ma_7','ma_30','day','month','year']]
y = df['close']

# 🔥 OPTIMIZED MODEL (SMALL SIZE)
model = RandomForestRegressor(
    n_estimators=20,   # 🔽 reduce trees
    max_depth=10,      # 🔽 limit depth
    random_state=42
)

model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Small model trained successfully")