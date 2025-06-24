# 🤖 WhatsApp Bot com Z-API + OpenAI GPT-4o

Este projeto é um bot de atendimento automático para WhatsApp utilizando:

- 🧠 OpenAI GPT-4o
- 📱 Z-API
- 🌐 Flask (backend)
- 🚀 Hospedagem via Render
- 🔒 Variáveis de ambiente seguras

---

## 📁 Estrutura

- `main.py`: Código principal.
- `prompt.txt`: Prompt usado como base para as respostas da IA.
- `requirements.txt`: Dependências.
- `.gitignore`: Arquivos ignorados pelo Git.
- `README.md`: Este manual.

---

## 🚀 Deploy no Render

1. Crie um novo repositório no GitHub e envie todos os arquivos.
2. Vá até o [Render.com](https://render.com) e clique em "New Web Service".
3. Conecte seu GitHub e selecione o repositório.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Environment:** Python 3.x
   - **Port:** 5000
5. Em **Environment > Environment Variables**, crie as variáveis:
   - `OPENAI_API_KEY`: sua chave da OpenAI
   - `ZAPI_TOKEN`: seu token da Z-API
   - `ZAPI_INSTANCE_ID`: seu ID da Z-API

---

## 📥 Payload esperado no webhook

```json
{
  "message": "Olá, quero um banner.",
  "phone": "554499999999"
}
```

---

## 🧠 Exemplo de Resposta da IA

> "Olá! Para calcular seu banner, por favor me informe as medidas, quantidade e tipo de material desejado. 😊"

---

## ✏️ Editando o comportamento da IA

Basta alterar o conteúdo do arquivo `prompt.txt`.

---

## ✅ Pronto para produção
