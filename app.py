from flask import Flask, render_template, request, jsonify
import pickle
import requests
import os

app = Flask(__name__)

MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    import train_model

model = pickle.load(open(MODEL_PATH, "rb"))

alerts = []
last_price = 0


def check_alert(current_price):
    global alerts
    triggered = []

    for alert in alerts:
        if current_price >= alert:
            triggered.append(alert)

    for a in triggered:
        alerts.remove(a)

    return triggered


def get_live_gold_price():
    global last_price

    try:
        url = "https://api.gold-api.com/price/XAU"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return last_price if last_price else 65000

        data = res.json()
        usd_price = data.get("price", 0)

        if usd_price == 0:
            return last_price if last_price else 65000

        usd_to_inr = 83.5

        price_per_gram = (usd_price * usd_to_inr) / 31.103

        price_10g = price_per_gram * 10

        price_24k = price_10g * 1.15

        final_price = round(price_24k, 2)

        last_price = final_price

        return final_price

    except:
        return last_price if last_price else 65000


@app.route('/')
def home():
    live_price = get_live_gold_price()
    return render_template('index.html', live_price=live_price)


@app.route('/live-price')
def live_price():
    price = get_live_gold_price()
    triggered_alerts = check_alert(price)

    return jsonify({
        "price": price,
        "alerts": triggered_alerts
    })


@app.route('/predict', methods=['POST'])
def predict():
    try:
        Open = float(request.form['Open'])
        High = float(request.form['High'])
        Low = float(request.form['Low'])

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


@app.route('/set-alert', methods=['POST'])
def set_alert():
    try:
        price = float(request.form['price'])
        alerts.append(price)
        return jsonify({"message": f"Alert set for ₹{price}"})
    except:
        return jsonify({"error": "Invalid input"})


if __name__ == "__main__":
    app.run(debug=True)