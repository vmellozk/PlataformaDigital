#Definição dos Modelos do Banco de Dados

import sqlite3

def insert_user(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    conn.commit()
    conn.close()

def get_user_by_email(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_survey_response(data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO survey_responses (user_id, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
