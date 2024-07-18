#Arquivo Principal do Flask

from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/loja')
def loja():
    return render_template('loja.html')

@app.route('/user/visitante')
def visit_user():
    return render_template('perfil_visita.html')

@app.route('/user')
def user():
    return render_template('perfil.html')

@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/formulario', methods=['GET', 'POST'])
def vendas():
    if request.method == 'POST':
        pass
    return render_template('vendas.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        categoria = request.form['categoria']
        
        insert_user(name, email, password, categoria)
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_login']
        password = request.form['password_login']

        user = get_user_by_email(email, password)
        if user:
            session['user_id'] = user[0]
            session['user_nome'] = user[1]
            session['user_categoria'] = user[2]
            return redirect(url_for('home'))
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

        insert_survey_response(data)
        generate_ebook(user_id)

        return redirect(url_for('vendas'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
