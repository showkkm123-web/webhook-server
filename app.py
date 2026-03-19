from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "RUNNING", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    print("RAW DATA:", data, flush=True)
    return jsonify({
        "status": "ok",
        "received": data
    }), 200
