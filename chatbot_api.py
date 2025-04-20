import anthropic
import os

#Aqui se establece la comunicacion hacia la API de Anthropic, con los parametros entregados en el documento respectivo
#IMPORTANTE: en este caso, se adjunta la variable de entorno .env.exampe en el directorio, aqui se debe adjuntar la llave de acceso respectiva, que se encuentra en el documento de instrucciones


api_access = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_bot_response(message):
    response = api_access.messages.create(
        model = "claude-3-haiku-20240307",
        max_tokens= 1024,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.content[0].text.strip()
