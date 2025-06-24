from flask import Flask, request, jsonify
import requests
import os
import traceback
import json

app = Flask(__name__)

# Tenta carregar o prompt
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

        # Mostra o JSON completo recebido da Z-API
        print("📥 JSON COMPLETO:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Para debug apenas — não processa, só retorna
        return jsonify({"status": "debug"}), 200

    except Exception as e:
        print("❌ Erro ao processar JSON:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com debug ativo!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
