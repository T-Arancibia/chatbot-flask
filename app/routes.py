#Aqui se establecen los endpoints de la API que sostiende el proyecto web
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .db import init_db, get_user_id, create_user, create_conversation, save_message, get_conversations_by_user, get_messages_by_conversation
from chatbot_api import get_bot_response

main = Blueprint("main", __name__)

#Antes que nada, se debe hacer el proceso de inicializacion de la base de datos (explicado mas en detalle en db.py)
@main.before_app_request
def setup():
    init_db() 

#Logica simple donde se procesa index.html en el directorio principal ("/")
@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login", methods=["POST"])
#Este endpoint tiene como fin el realizar un pseudo-login del usuario en la app en funcion de su username
def login():
    data = request.json
    username = data.get("username", "").strip().lower()
    #Se obliga al usuario a ingresar un username
    if not username:
        return jsonify({"error": "Nombre de usuario requerido"}), 400

    user_id = get_user_id(username)
    #En caso de no existir el usuario previamente, se crea uno nuevo en la DB
    if not user_id:
        user_id = create_user(username)
        if not user_id:
            return jsonify({"error": "No se pudo crear el usuario"}), 500

    return jsonify({"user_id": user_id})

#Endpoint de chat (probablemente la funcionalidad mas importante y compleja a la vez), aqui se busca almacenar de manera ordenada el mensaje escrito, para posteriormente ser enviado al chatbot
@main.route("/chat", methods = ["POST"])
def chat():
    #Se procesan los parametros del mensaje que se desea enviar
    data = request.json
    username = data.get("username").strip().lower()
    message = data.get("message")
    conversation_id = data.get("conversation_id")
    #En este apartado, se busca evitar problemas en el envio de la informacion (que no haya mensaje y/o usuario que lo envia)
    if not username or not message:
        return jsonify({"error":"Fatlan datos para su solicitud"}), 400
    #Se extrae el id del usuario en funcion de su propio username 
    user_id = get_user_id(username)
    #Llegados a este punto, ya se han validado correctamente los datos de usuario y del mensaje a enviar
    #Si es que no se asocia un id de conversacion, quiere decir que la conversacion es nueva, de modo que se debe validar el requerimiento de la limitante de 10 conversaciones mencionado en el documento
    if not conversation_id:
        #Se parte por sacar la cantidad de conversaciones del usuario que intenta iniciar un nuevo chat
        conversations = get_conversations_by_user(user_id)
        if len(conversations) >= 10:
            #Se realiza la validacion del requerimiento antes mencionado, en caso de no cumplirse se notifica al usuario que se alcanzo el limite
            return jsonify({"error": "Limite de conversaciones (10) alcanzado!"}), 400
        #Caso contrario, se crea una nueva conversacion para el usuario
        conversation_id = create_conversation(user_id)
    #Se realiza la insercion en la DB, tanto del mensaje enviado, como la respuesta recibida por el chatbot
    save_message(conversation_id, "user", message)
    response = get_bot_response(message)
    save_message(conversation_id, "assistant", response)
    return jsonify({"response": response, "conversation_id": conversation_id, "user_id": user_id})

@main.route("/history/<user_id>")
#Logica simple para acceder al historial de conversaciones del usuario (importante para ser mostrado posteriormente en el historial en index.html)
def history(user_id):
    conversations = get_conversations_by_user(user_id)
    return jsonify(conversations)

@main.route("/conversation/<conversation_id>")
#Logica simple para acceder a una conversacion especifica en funcion de su id
def conversation(conversation_id):
    messages = get_messages_by_conversation(conversation_id)
    return jsonify(messages)
