from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    if not data or "message" not in data or not data["message"]:
        return jsonify({"detail": "Message cannot be empty"}), 400

    # Reverse the string and respond
    reversed_message = data['message'][::-1]
    return jsonify({"response": reversed_message})

if __name__ == "__main__":
    app.run(debug=True)
