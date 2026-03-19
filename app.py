@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.data.decode("utf-8")

    print("RAW DATA:", data)

    # 강제로 Buy 처리 (테스트용)
    side = "Buy"
    symbol = "BTCUSDT"
    qty = 0.001

    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=qty,
            timeInForce="GoodTillCancel"
        )
        return {"status": "success", "order": order}

    except Exception as e:
        return {"status": "error", "message": str(e)}
