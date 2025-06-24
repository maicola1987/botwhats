from flask import Flask, request, jsonify
import requests
import os
import traceback
from openai import OpenAI

app = Flask(__name__)

# Carregar prompt
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

# Cliente da OpenAI (nova API)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("📥 JSON recebido:", data)

        phone = data.get("phone")
        message = data.get("text", {}).get("message", "")

        if not phone or not message:
            print("❌ Mensagem ou telefone ausente.")
            return jsonify({"error": "Mensagem ou telefone ausente"}), 400

        print(f"📱 Número: {phone}")
        print(f"💬 Mensagem: {message}")

        # ✅ Usando nova sintaxe da biblioteca openai>=1.0.0
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        response_text = response.choices[0].message.content
        print("🤖 Resposta da IA:", response_text)

        # Enviar resposta via Z-API
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
    return 'Bot WhatsApp com IA usando nova OpenAI API ✅', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
