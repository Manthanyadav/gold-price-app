from flask import Flask, render_template, request, jsonify
import pickle
import requests
import os

app = Flask(__name__)

# =========================
# LOAD / AUTO TRAIN MODEL
# =========================

MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    print("⚡ model.pkl not found → Training...")
    import train_model

model = pickle.load(open(MODEL_PATH, "rb"))

# =========================
# ALERT SYSTEM
# =========================

alerts = []

def check_alert(current_price):
    triggered = []
    for alert in alerts:
        if current_price >= alert:
            triggered.append(alert)
    
    for a in triggered:
        alerts.remove(a)
        print(f"🚨 ALERT TRIGGERED: ₹{a}")

# =========================
# LIVE GOLD API
# =========================

def get_live_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return 0

        data = response.json()

        usd_price = data.get('price', 0)
        usd_to_inr = 83

        price = (usd_price * usd_to_inr) / 31.103
        price = round(price, 2)

        check_alert(price)
        return price

    except Exception as e:
        print("API Error:", e)
        return 0

# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    live_price = get_live_gold_price()
    return render_template('index.html', live_price=live_price)

@app.route('/live-price')
def live_price():
    return jsonify({"price": get_live_gold_price()})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        Open = float(request.form['Open'])
        High = float(request.form['High'])
        Low = float(request.form['Low'])

        # simple feature logic
        features = [[Open, High, Low, Open, Open, 1, 1, 2024]]

        prediction = model.predict(features)[0]
        live_price = get_live_gold_price()

        return render_template(
            'result.html',
            prediction_text=f"Predicted Price: ₹{prediction:.2f}",
            live_price=live_price
        )

    except Exception as e:
        return f"❌ Error: {e}"

# 🔔 SET ALERT
@app.route('/set-alert', methods=['POST'])
def set_alert():
    try:
        price = float(request.form['price'])
        alerts.append(price)
        return jsonify({"message": f"Alert set for ₹{price}"})
    except:
        return jsonify({"error": "Invalid input"})

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run()