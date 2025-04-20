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
