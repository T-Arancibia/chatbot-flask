import anthropic
import os
from app.db import get_messages_by_conversation
#Aqui se establece la comunicacion hacia la API de Anthropic, con los parametros entregados en el documento respectivo
#IMPORTANTE: en este caso, se adjunta la variable de entorno .env.exampe en el directorio, aqui se debe adjuntar la llave de acceso respectiva, que se encuentra en el documento de instrucciones


api_access = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_bot_response(message, conversation_id):

    messages = get_messages_by_conversation(conversation_id)
    total_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    total_messages.append({"role": "user", "content": message})
    response = api_access.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens= 1024,
        messages= total_messages
    )
    return response.content[0].text.strip()
