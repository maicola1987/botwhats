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
    print("📥 Dados recebidos no webhook:", data)

    try:
        # Aceita diferentes nomes de campos usados pela Z-API
        message = data.get("message") or data.get("text") or ""
        phone = data.get("phone") or data.get("from") or ""

        message = message.strip()
        phone = phone.strip()

        if not message or not phone:
            print("⚠️ Dados incompletos: 'message' ou 'phone' ausentes")
            return jsonify({"error": "Dados incompletos"}), 400

        print(f"📩 Mensagem recebida: {message}")
        print(f"📱 Número do cliente: {phone}")

        # Consultar a OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        response_text = completion.choices[0].message["content"]
        print("🤖 Resposta da IA:", response_text)

        # Enviar resposta ao WhatsApp via Z-API
        url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-messages"
        payload = {
            "phone": phone,
            "message": response_text
        }

        zapi_response = requests.post(url, json=payload)
        print("📤 Resposta da Z-API:", zapi_response.text)

        return jsonify({"status": "ok", "message": "Resposta enviada com sucesso"}), 200

    except Exception as e:
        print("❌ Erro no webhook:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com OpenAI online!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
