#Aqui se crea la base de datos SQLite

import sqlite3
from datetime import datetime

DB_NAME = "chat_bot.db"
#Primeramente, se crea la base de datos completa (o las partes que no existan), realizando los CREATE respectivos de SQLite
def init_db():
    connection = sqlite3.connect(DB_NAME)
    c = connection.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE
              )
              ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS Conversaciones (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              start_time TEXT,
              FOREIGN KEY (user_id) REFERENCES Usuarios(id)
              )
              ''')
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS Mensajes (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              conversation_id INTEGER,
              role TEXT,
              content TEXT,
              timestamp TEXT,
              FOREIGN KEY (conversation_id) REFERENCES Conversaciones(id)
              )
              ''')
    
    connection.commit()
    connection.close()
#Se establece conexion con la DB (utilizado en todas las consultas posteriores)
def get_db():
    return sqlite3.connect(DB_NAME)
    
#En primera instancia, se extrae el id del usuario en base a su username registrado en la DB y se retorna
def get_user_id(username):
    connection = get_db()
    c = connection.cursor()
    c.execute("SELECT id FROM Usuarios WHERE username = ?", (username,))
    result = c.fetchone()
    connection.close()
    return result[0] if result else None

def create_user(username):
    #Para crear correctamente un usuario nuevo, se hace el insert respectivo. Notar que si esta duplicado (ya que la TABLE Usuarios no permite duplicados) no se retorna nada
    connection = get_db()
    c = connection.cursor()

    try:
        c.execute("INSERT INTO Usuarios (username) VALUES (?)", (username,))
        user_id = c.lastrowid
        connection.commit()

    except sqlite3.IntegrityError:
        user_id = None

    connection.close()
    return user_id
    

#Para crear una nueva conversacion, simplemente se agrega en la TABLE Conversaciones el usuario que la inicia y la fecha (ya que el id es autoincremental)
def create_conversation(user_id):
    connection = get_db()
    c = connection.cursor()
    start_time = datetime.utcnow().isoformat()
    c.execute("INSERT INTO Conversaciones (user_id, start_time) VALUES (?, ?)", (user_id, start_time))
    conversation_id = c.lastrowid
    connection.commit()
    connection.close()
    return conversation_id
#Para agregar el mensaje, ademas del id de la conversacion asociada, es necesario definir el rol (lo cual de hace en routes.py) y el texto de dicho mensaje
def save_message(conversation_id, role, content):
    connection = get_db()
    c = connection.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute("INSERT INTO Mensajes (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)", (conversation_id, role, content, timestamp))
    connection.commit()
    connection.close()
#Para extraer las conversaciones del usuario, se hace una query simple con el id del propio usuario
def get_conversations_by_user(user_id):
    connection = get_db()
    c = connection.cursor()
    c.execute("SELECT id, start_time FROM Conversaciones WHERE user_id = ? ORDER BY start_time DESC", (user_id,))
    rows = c.fetchall()
    connection.close()
    return [{"id": row[0], "start_time": row[1]} for row in rows]
#Logica similar a la query anterior, solo que se usa el id de la conversacion para extraer sus mensajes asociados
def get_messages_by_conversation(conversation_id):
    connection = get_db()
    c = connection.cursor()
    c.execute("SELECT role, content, timestamp FROM Mensajes WHERE conversation_id = ? ORDER BY timestamp ASC", (conversation_id,))
    rows = c.fetchall()
    connection.close()
    return [{"role": row[0], "content": row[1], "timestamp": row[2]} for row in rows]    
