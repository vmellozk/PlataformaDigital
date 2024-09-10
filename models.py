#Definição dos Modelos do Banco de Dados

import sqlite3

def insert_user(name, email, password, categoria):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, password, categoria) VALUES (?, ?, ?, ?)', (name, email, password, categoria))
    conn.commit()
    conn.close()

def get_user_by_email(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, categoria FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_email_by_user_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM users WHERE id = ?', (user_id,))
    user_email = cursor.fetchone()
    conn.close()
    return user_email[0] if user_email else None

def insert_survey_response(data):
    global response_number 

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO survey_responses (user_id, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
