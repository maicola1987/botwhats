# 🤖 Bot WhatsApp com OpenAI GPT-4o e Z-API

Este projeto implementa um atendimento automático para WhatsApp via Z-API, utilizando OpenAI GPT-4o e hospedado no Render.

## ⚙️ Arquivos
- `main.py`: Código principal do bot
- `prompt.txt`: Prompt base para controle do tom das respostas da IA
- `requirements.txt`: Dependências
- `.gitignore`: Exclusão de arquivos sensíveis
- `README.md`: Este guia

## 🚀 Deploy no Render
1. Suba os arquivos no GitHub
2. Crie um Web Service no Render
3. Configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
   - Variáveis de ambiente:
     - `OPENAI_API_KEY`
     - `ZAPI_TOKEN`
     - `ZAPI_INSTANCE_ID`

## ✅ Pronto para produção
Ao mandar mensagem no WhatsApp, a IA responde automaticamente via GPT-4o.
