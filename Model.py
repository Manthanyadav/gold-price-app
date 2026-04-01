import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Simple dataset (temporary)
data = pd.DataFrame({
    'Open': [100, 200, 300, 400],
    'High': [110, 210, 310, 410],
    'Low': [90, 190, 290, 390],
    'Volume': [1000, 2000, 3000, 4000],
    'Close': [105, 205, 305, 405]
})

X = data[['Open', 'High', 'Low', 'Volume']]
y = data['Close']

model = RandomForestRegressor()
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("✅ model.pkl created successfully")