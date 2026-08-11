from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")


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
        data = request.get_json()

        print("========== WEBHOOK RECIBIDO ==========")
        print(data)
        print("=======================================")

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]

            if message["type"] == "text":
                numero = message["from"]
                texto = message["text"]["body"].lower()

                if texto in ["hola", "buenas", "buenas tardes", "buenos dias"]:
                    respuesta = "¡Hola! ¿En qué podemos ayudarte?"
                else:
                    respuesta = "¡Hola! Gracias por escribirnos. ¿En qué podemos ayudarte?"

                enviar_mensaje(numero, respuesta)

        except Exception as e:
            print("ERROR:", e)

        return "EVENT_RECEIVED", 200


def enviar_mensaje(numero, texto):

    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    datos = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    respuesta = requests.post(
        url,
        headers=headers,
        json=datos
    )

    print("RESPUESTA DE WHATSAPP:", respuesta.status_code)
    print(respuesta.text)


@app.route("/")
def inicio():
    return "Bot de WhatsApp funcionando"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
