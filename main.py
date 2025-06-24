from flask import Flask, request, jsonify
import requests
import os
import openai

app = Flask(__name__)

# Ler o prompt base do arquivo
with open("prompt.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

# Carregar chaves do ambiente (Render)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")

openai.api_key = OPENAI_API_KEY

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        message = data["message"]
        phone = data["phone"]

        # Consultar a OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        response_text = completion.choices[0].message["content"]

        # Enviar resposta pelo WhatsApp via Z-API
        url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-messages"
        payload = {
            "phone": phone,
            "message": response_text
        }

        requests.post(url, json=payload)

        return jsonify({"status": "ok", "message": "Resposta enviada"}), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro no processamento"}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com OpenAI online!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
