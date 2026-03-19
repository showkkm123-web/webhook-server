import threading

def place_order_async(side, symbol, qty):
    try:
        session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )
    except Exception as e:
        print("ORDER ERROR:", e)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    print("RAW DATA:", data)

    side = data.get("side", "Buy")
    symbol = data.get("symbol", "BTCUSDT")
    qty = data.get("qty", "0.001")

    threading.Thread(
        target=place_order_async,
        args=(side, symbol, qty)
    ).start()

    return jsonify({"status": "received"}), 200
