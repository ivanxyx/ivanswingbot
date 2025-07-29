import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

@app.route('/api/trade-signal', methods=['POST'])
def receive_signal():
    data = request.get_json()

    # Basic validation
    if not data.get("macd") or data.get("win_probability", 0) < 0.70:
        send_telegram_alert(f"❌ Setup rejected for {data.get('ticker')}. System rules not met.")
        return jsonify({"status": "rejected"}), 200

    entry = data.get("price")
    stop_loss = round(entry * 0.985, 2)
    msg = (
        f"📊 Swing Trade Signal\n"
        f"Ticker: {data.get('ticker')}\n"
        f"Entry: {entry}\n"
        f"SL: {stop_loss}\n"
        f"Win Prob: {data.get('win_probability') * 100:.0f}%"
    )
    send_telegram_alert(msg)
    return jsonify({"status": "ok"}), 200

@app.route('/')
def root():
    return "Swing bot online!", 200
