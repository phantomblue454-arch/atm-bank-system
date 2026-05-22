from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

sessions = {}

@app.route("/")
def home():
    return render_template("atm.html")

@app.route("/atm")
def atm():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"status": "waiting", "data": None}
    return render_template("atm.html", session_id=session_id)

@app.route("/session/<session_id>")
def get_session(session_id):
    return jsonify(sessions.get(session_id, {}))

@app.route("/receive/<session_id>", methods=["POST"])
def receive(session_id):
    if session_id in sessions:
        sessions[session_id]["status"] = "received"
        sessions[session_id]["data"] = request.json
        return jsonify({"message": "received"})
    return jsonify({"error": "invalid session"}), 404

@app.route("/action/<session_id>/<action>", methods=["POST"])
def action(session_id, action):
    if session_id in sessions:
        sessions[session_id]["status"] = action
        return jsonify({"message": action})
    return jsonify({"error": "invalid session"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
