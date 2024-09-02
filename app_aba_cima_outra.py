import threading
import queue
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response
from generate_Ebook import generate_ebook
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
lock = threading.Lock()

def process_user(user_id):
    # Configurações do navegador
    MAX_TABS = 4
    window_width = 960
    window_height = 540
    offsets = [(0, 0), (960, 0), (0, 540), (960, 540)]

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    service = Service(ChromeDriverManager().install())

    with semaphore:
        position_index = None
        
        with threading.Lock():
            position_index = len([thread for thread in threading.enumerate() if thread.name.startswith('User_')]) % MAX_TABS

        position = offsets[position_index]

        # Configurar o navegador com a posição e tamanho corretos
        chrome_options.add_argument(f'--window-position={position[0]},{position[1]}')
        chrome_options.add_argument(f'--window-size={window_width},{window_height}')
        driver = uc.Chrome(service=service, options=chrome_options)
        
        # Garantir que o navegador seja carregado corretamente
        driver.get('about:blank')
        driver.set_window_size(window_width, window_height)
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
        thread = threading.Thread(target=process_user, args=(user_id,), name=f'User_{user_id}')
        thread.start()
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

            with lock:
                if not tab_queue.full():
                    if user_id not in tab_queue.queue:
                        tab_queue.put(user_id)
                        flash('Formulário enviado com sucesso! Iniciando automação.', 'success')
                        if semaphore.acquire(blocking=False):
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
