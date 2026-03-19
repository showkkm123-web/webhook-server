from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    print("받은 데이터:", data)
    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "Webhook server is running", 200
