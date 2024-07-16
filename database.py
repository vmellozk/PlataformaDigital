#Inicialização do Banco de Dados

import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY,
                       email TEXT UNIQUE,
                       password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses
                      (id INTEGER PRIMARY KEY,
                       user_id INTEGER,
                       question1 TEXT,
                       question2 TEXT,
                       question3 TEXT,
                       question4 TEXT,
                       question5 TEXT,
                       question6 TEXT,
                       question7 TEXT,
                       question8 TEXT,
                       question9 TEXT,
                       question10 TEXT,
                       FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()
