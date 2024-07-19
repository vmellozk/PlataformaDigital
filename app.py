from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route('/')
@app.route('/home')
def home():
    print("Accessing home page")
    return render_template('home.html')

@app.route('/loja')
def loja():
    print("Accessing loja page")
    return render_template('loja.html')

@app.route('/user/visitante')
def visit_user():
    if 'user_id' in session:
        print("User is authenticated. Accessing perfil_visita page")
        return render_template('perfil_visita.html')
    else:
        print("User not authenticated. Redirecting to login")
        return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'user_id' in session:
        print("User is authenticated. Accessing perfil page")
        return render_template('perfil.html')
    else:
        print("User not authenticated. Redirecting to login")
        return redirect(url_for('login'))

@app.route('/premium')
def premium():
    if 'user_id' in session:
        print("User is authenticated. Accessing premium page")
        return render_template('premium.html')
    else:
        print("User not authenticated. Redirecting to login")
        return redirect(url_for('login'))

@app.route('/formulario', methods=['GET', 'POST'])
def vendas():
    if 'user_id' in session:
        print("User is authenticated. Accessing vendas page")
        return render_template('vendas.html')
    else:
        print("User not authenticated. Redirecting to login")
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        categoria = request.form['categoria']
        
        print(f"Registering user: Name={name}, Email={email}, Categoria={categoria}")

        try:
            insert_user(name, email, password, categoria)
            print("User registered successfully")
        except Exception as e:
            print(f"Error during user registration: {e}")

        return redirect(url_for('login'))
    
    print("Accessing register page")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_login']
        password = request.form['password_login']

        print(f"Attempting to login with email: {email}")

        user = get_user_by_email(email, password)
        if user:
            session['user_id'] = user[0]
            session['user_nome'] = user[1]
            session['user_categoria'] = user[2]
            print(f"User logged in: ID={user[0]}, Name={user[1]}")
            return redirect(url_for('home'))
        else:
            print("User not found or incorrect password")
    print("Accessing login page")
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' in session:
        user_id = session['user_id']
        print(f"Submitting form for user ID: {user_id}")

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

        try:
            insert_survey_response(data)
            generate_ebook(user_id)
            print("Form submitted successfully, and ebook generated")
        except Exception as e:
            print(f"Error during form submission or ebook generation: {e}")

        return redirect(url_for('home'))
    print("User not authenticated, redirecting to login")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("Initializing database")
    init_db()
    print("Starting Flask app")
    app.run(debug=True)
