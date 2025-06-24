from flask import Flask, request, jsonify
import requests
import os
import traceback

app = Flask(__name__)

# Tentativa de leitura do prompt
try:
    with open("prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()
except Exception as e:
    SYSTEM_PROMPT = "Você é um atendente automático."
    print("⚠️ Falha ao ler prompt.txt:", str(e))

# Carregar variáveis do ambiente
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Captura o corpo bruto da requisição (debug total)
        data_raw = request.get_data()
        print("📥 RAW DATA RECEBIDA (bruta):")
        print(data_raw.decode('utf-8'))

        # Só responder OK para testar o recebimento
        return jsonify({"status": "debug"}), 200

    except Exception as e:
        print("❌ Erro ao processar webhook:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return 'Bot WhatsApp com debug de payload ativado!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
