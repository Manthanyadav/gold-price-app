from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import requests
import os

app = Flask(__name__)

# =========================
# LOAD / AUTO TRAIN MODEL
# =========================

if not os.path.exists("model.pkl"):
    print("⚡ model.pkl not found → Training शुरू...")
    import train_model  # auto create model

model = pickle.load(open("model.pkl", "rb"))

# =========================
# ALERT SYSTEM
# =========================

alerts = []

def check_alert(current_price):
    for alert in alerts:
        if current_price >= alert:
            print(f"🚨 ALERT! Gold reached ₹{alert}")

# =========================
# LIVE GOLD API
# =========================

def get_live_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        data = requests.get(url).json()

        usd_price = data['price']
        usd_to_inr = 83

        # ounce → gram
        inr_price = (usd_price * usd_to_inr) / 31.103
        price = round(inr_price, 2)

        check_alert(price)
        return price

    except:
        return 0  # fallback if API fails

# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    live_price = get_live_gold_price()
    return render_template('index.html', live_price=live_price)

# LIVE API (for chart)
@app.route('/live-price')
def live_price():
    price = get_live_gold_price()
    return jsonify({"price": price})

# PREDICTION
@app.route('/predict', methods=['POST'])
def predict():
    try:
        Open = float(request.form['Open'])
        High = float(request.form['High'])
        Low = float(request.form['Low'])

        MA_7 = Open
        MA_30 = Open
        day = 1
        month = 1
        year = 2024

        features = [[Open, High, Low, MA_7, MA_30, day, month, year]]

        prediction = model.predict(features)[0]
        live_price = get_live_gold_price()

        return render_template(
            'result.html',
            prediction_text=f"Predicted Price: ₹{prediction:.2f}",
            live_price=live_price
        )

    except Exception as e:
        return f"Error: {e}"

# 🔔 SET ALERT
@app.route('/set-alert', methods=['POST'])
def set_alert():
    try:
        price = float(request.form['price'])
        alerts.append(price)
        return f"✅ Alert set for ₹{price}"
    except:
        return "❌ Invalid input"

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run()