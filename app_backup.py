from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
import threading

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
    if 'user_id' in session:
        return render_template('perfil_visita.html')
    else:
        return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'user_id' in session:
        return render_template('perfil.html')
    else:
        return redirect(url_for('login'))

@app.route('/premium')
def premium():
    if 'user_id' in session:
        return render_template('premium.html')
    else:
        return redirect(url_for('login'))

@app.route('/formulario', methods=['GET', 'POST'])
def vendas():
    if 'user_id' in session:
        return render_template('vendas.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        categoria = request.form['categoria']

        try:
            insert_user(name, email, password, categoria)
        except Exception as e:
            print(f"Error during user registration: {e}")
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
            print("User not found or incorrect password")

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

        try:
            print(f"Inserindo resposta do formulário: {data}")  # Print para verificar os dados
            insert_survey_response(data)

            # Iniciando uma thread para gerar o ebook em segundo plano
            def generate_ebook_in_thread(user_id):
                print(f"Gerando eBook para o usuário_id: {user_id}")
                generate_ebook(user_id)
            thread = threading.Thread(target=generate_ebook_in_thread, args=(user_id,))
            thread.start()
            flash('Formulário enviado com sucesso! Aguarde o eBook gerado.', 'success')

        except Exception as e:
            print(f"Erro durante a submissão do formulário ou geração do eBook: {e}")  # Print para erro
            flash('Houve um erro ao enviar o formulário. Tente novamente ou entre em contato.', 'warning')

        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
