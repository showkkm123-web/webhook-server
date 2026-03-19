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

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    side = data.get("side")  # "Buy" or "Sell"
    symbol = data.get("symbol", "BTCUSDT")
    qty = float(data.get("qty", 0.001))

    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )
        return jsonify({"status": "success", "order": order})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/")
def home():
    return "RUNNING"
