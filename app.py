from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_123")


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verificación de Meta
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge, 200

        return "Token incorrecto", 403

    # Mensajes que llegan desde WhatsApp
    if request.method == "POST":
        print("========== WEBHOOK RECIBIDO ==========")
        print(request.get_json())
        print("=======================================")

        return "EVENT_RECEIVED", 200


@app.route("/")
def inicio():
    return "Bot de WhatsApp funcionando"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)