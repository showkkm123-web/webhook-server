from flask import Flask, request, jsonify
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret
)

@app.route("/")
def home():
    return "RUNNING", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    print("RAW DATA:", data)

    side = "Buy"
    symbol = "BTCUSDT"
    qty = "0.001"

    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )
        return jsonify({"status": "success", "order": order}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200
