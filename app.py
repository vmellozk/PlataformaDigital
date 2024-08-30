from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
import threading
import queue
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

app = Flask(__name__)
app.secret_key = 'chave_secreta'
MAX_QUEUE_SIZE = 100
MAX_TABS = 4
task_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)
tab_queue = queue.Queue(maxsize=MAX_TABS)
semaphore = threading.Semaphore(MAX_TABS)

# Função para processar cada usuário
def process_user(user_id):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    service = Service(ChromeDriverManager().install())

    # Inicia o navegador
    driver = uc.Chrome(service=service, options=chrome_options)

    # Configura o tamanho e a posição da janela após o navegador ser iniciado
    driver.set_window_size(960, 540)
    offsets = [(0, 0), (960, 0), (0, 540), (960, 540)]
    position = offsets[len(tab_queue.queue) % 4]
    driver.set_window_position(position[0], position[1])

    try:
        generate_ebook(user_id, driver)
    except Exception as e:
        print(f"Erro ao processar o usuário {user_id}: {e}")
    finally:
        driver.quit()
        print(f"Processamento concluído para o usuário {user_id}. Fechando o navegador.")
        tab_queue.task_done()

# Função para processar a fila de abas
def process_tabs():
    while True:
        user_id = tab_queue.get()
        if user_id is None:
            break
        with semaphore:
            print(f"Processando eBook para o usuário_id: {user_id}")
            process_user(user_id)

            # Verificar se há novas solicitações na fila de tarefas
            if not task_queue.empty():
                next_user_id = task_queue.get()
                if not tab_queue.full():
                    tab_queue.put(next_user_id)
                    flash('Nova solicitação adicionada à fila de abas.', 'info')
                else:
                    task_queue.put(next_user_id)
                      
        tab_queue.task_done()

# Inicia o thread para processar abas
tab_processor_thread = threading.Thread(target=process_tabs, daemon=True)
tab_processor_thread.start()

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
            print(f"Inserindo resposta do formulário: {data}")
            insert_survey_response(data)

            if not tab_queue.full():
                if user_id not in tab_queue.queue:
                    tab_queue.put(user_id)
                    flash('Formulário enviado com sucesso! Iniciando automação.', 'success')
                    # Verifica se há espaço na fila de abas e inicia a automação
                    if semaphore.acquire(blocking=False):  # Tenta adquirir o semáforo
                        threading.Thread(target=process_user, args=(user_id,)).start()
                else:
                    flash('Sua solicitação já está na fila de abas.', 'info')
            else:
                if user_id not in task_queue.queue:
                    task_queue.put(user_id)
                    flash('A fila de abas está cheia. Sua solicitação foi adicionada à fila de espera.', 'warning')
                else:
                    flash('Sua solicitação já está na fila de espera.', 'info')

        except Exception as e:
            print(f"Erro durante a submissão do formulário ou geração do eBook: {e}")
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
