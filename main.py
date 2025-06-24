from flask import Flask, request, jsonify
import requests
import os
import traceback

app = Flask(__name__)

# Tenta ler o prompt (mas mesmo que falhe, segue)
try:
    with open("prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()
except Exception as e:
    SYSTEM_PROMPT = "Você é um atendente automático."
    print("⚠️ Falha ao ler prompt.txt:", str(e))

# Chaves de ambiente
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("📥 Dados recebidos:", data)

        message = data.get("message") or data.get("text") or ""
        phone = data.get("phone") or data.get("from") or ""

        message = message.strip()
        phone = phone.strip()

        if not message or not phone:
            print("⚠️ Campos ausentes:", {"message": message, "phone": phone})
            return jsonify({"error": "Campos ausentes"}), 400

        print(f"📩 Mensagem: {message}")
        print(f"📱 Telefone: {phone}")

        # Teste: simular resposta fixa (sem OpenAI)
        response_text = "Recebemos sua mensagem! Em instantes retornaremos. 😊"

        # Enviar resposta
        url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-messages"
        payload = {
            "phone": phone,
            "message": response_text
        }

        zapi_response = requests.post(url, json=payload)
        print("📤 Resposta da Z-API:", zapi_response.status_code, zapi_response.text)

        return jsonify({"status": "ok", "message": "Resposta enviada"}), 200

    except Exception as e:
        print("❌ Erro no webhook:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com debug ativo!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
