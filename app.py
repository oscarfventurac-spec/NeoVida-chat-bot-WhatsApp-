from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_123"

@app.route("/", methods=["GET"])
def home():
    return "Bot de WhatsApp funcionando", 200


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Token incorrecto", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("Mensaje recibido:", data)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
