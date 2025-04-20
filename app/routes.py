#Aqui se establecen los endpoints de la API que sostiende el proyecto web
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .db import init_db, get_user_id, create_user, create_conversation, save_message, get_conversations_by_user, get_messages_by_conversation
from chatbot_api import get_bot_response

main = Blueprint("main", __name__)

#Antes que nada, se debe hacer el proceso de inicializacion de la base de datos (explicado mas en detalle en db.py)
@main.before_app_request
def setup():
    init_db() 
