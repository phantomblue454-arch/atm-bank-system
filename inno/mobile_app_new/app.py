from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ATM_SERVER = "http://172.20.10.3:5000"

@app.route("/")
def home():
    return render_template("mobile.html")

@app.route("/connect")
def connect():
    return render_template("mobile.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    session_id = data.get("session_id")

    payload = {
        "account": data.get("account"),
        "amount": data.get("amount"),
        "denominations": data.get("denominations")
    }

    r = requests.post(f"{ATM_SERVER}/receive/{session_id}", json=payload)

    return jsonify({"status": "sent", "atm_response": r.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
