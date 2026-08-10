from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "mi_token_123"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge

        return "Token incorrecto", 403

    if request.method == "POST":
        data = request.get_json()

        print("Mensaje recibido:")
        print(data)

        return "EVENT_RECEIVED", 200


@app.route("/")
def inicio():
    return "Bot de WhatsApp funcionando"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
