@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw = request.get_data(as_text=True)
        print("[WEBHOOK RAW]", raw)

        data = request.get_json(silent=True)

        # JSON 아니면 무조건 무시 (기본 전략 메시지)
        if not isinstance(data, dict):
            print("[SKIP] not json")
            return jsonify({"status": "ignored"}), 200

        # 우리가 만든 형식만 통과
        if "side" not in data or "symbol" not in data or "qty" not in data:
            print("[SKIP] not our format:", data)
            return jsonify({"status": "ignored"}), 200

        print("[VALID SIGNAL]", data)

        threading.Thread(target=place_order_async, args=(data,)).start()

        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"status": "ignored"}), 200
