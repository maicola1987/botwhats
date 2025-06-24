from flask import Flask, request, jsonify
import requests
import os
import openai
import traceback

app = Flask(__name__)

# Carregar prompt base
try:
    with open("prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()
except Exception as e:
    SYSTEM_PROMPT = "Você é um atendente automático."
    print("⚠️ Falha ao ler prompt.txt:", str(e))

# Variáveis de ambiente
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")

openai.api_key = OPENAI_API_KEY

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("📥 JSON recebido:", data)

        # Extrair mensagem e número do cliente
        phone = data.get("phone")
        message = data.get("text", {}).get("message", "")

        if not phone or not message:
            print("❌ Mensagem ou telefone ausente.")
            return jsonify({"error": "Mensagem ou telefone ausente"}), 400

        print(f"📱 Número: {phone}")
        print(f"💬 Mensagem: {message}")

        # Enviar para o ChatGPT
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        response_text = completion.choices[0].message["content"]
        print("🤖 Resposta da IA:", response_text)

        # Enviar para o WhatsApp via Z-API
        zapi_url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-messages"
        payload = {
            "phone": phone,
            "message": response_text
        }

        zapi_response = requests.post(zapi_url, json=payload)
        print("📤 Z-API:", zapi_response.status_code, zapi_response.text)

        return jsonify({"status": "ok", "resposta": response_text}), 200

    except Exception as e:
        print("❌ Erro ao processar webhook:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com IA está ativo ✅', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
