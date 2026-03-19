from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP
import threading
import os

app = Flask(__name__)

session = HTTP(
    testnet=False,
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

@app.route("/")
def home():
    return "RUNNING", 200

def place_order_async(data):
    try:
        side = data.get("side")
        symbol = data.get("symbol")
        qty = data.get("qty")

        print(f"[ORDER START] side={side}, symbol={symbol}, qty={qty}")

        result = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="IOC"
        )

        print("[ORDER SUCCESS]", result)

    except Exception as e:
        print("[ORDER ERROR]", str(e))

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("[WEBHOOK RECEIVED]", data)

        threading.Thread(target=place_order_async, args=(data,)).start()

        return jsonify({
            "status": "received",
            "message": "order is being processed"
        }), 200

    except Exception as e:
        print("[WEBHOOK ERROR]", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
