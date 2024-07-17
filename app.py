#Arquivo Principal do Flask

from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route('/')
def vendas():
    return render_template('vendas.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Registering user with email: {email}")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Trying to login with email: {email}")

        user = get_user_by_email(email, password)
        if user:
            print(f"User found: {user}")

            session['user_id'] = user[0]
            return redirect(url_for('vendas'))
        else:
            print(f"User not found or incorrect password")
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' in session:
        user_id = session['user_id']
        data = (
            user_id,
            request.form['question1'],
            request.form['question2'],
            request.form['question3'],
            request.form['question4'],
            request.form['question5'],
            request.form['question6'],
            request.form['question7'],
            request.form['question8'],
            request.form['question9'],
            request.form['question10']
        )

        print(f"Insert survey response for user_id: {user_id}")

        insert_survey_response(data)
        generate_ebook(user_id)

        return redirect(url_for('vendas'))
    print(f"User not logged in, redirecting to login")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
