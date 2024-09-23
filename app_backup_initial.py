import time
import threading
import queue
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, request, redirect, url_for, session, flash
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response, get_email_by_user_id
from generate_Ebook import generate_ebook
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

#
app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Configurações
MAX_TABS = 4
TASK_QUEUE_DELAY = 3  # Tempo em segundos para aguardar antes de processar a próxima aba
STARTUP_DELAY = 3    # Tempo em segundos para aguardar antes de iniciar o processamento de qualquer aba
task_queue = queue.Queue()
tab_semaphore = threading.Semaphore(MAX_TABS)
position_lock = threading.Lock()
startup_lock = threading.Lock()  # Lock para controlar o atraso global

# Posições da janela do navegador (grade 2x2)
positions = [
    (0, 0),        # Canto superior esquerdo
    (960, 0),      # Canto superior direito
    (0, 540),      # Inferior esquerdo
    (960, 540)     # Inferior direito
]

# Lista para rastrear quais posições estão ocupadas (False = livre, True = ocupada)
occupied_positions = [False, False, False, False]

# Tamanho da janela do navegador
window_width = 960
window_height = 540

# Obter e carrega as variáveis de ambiente / Configurações de email
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

# Função para encontrar a primeira posição livre
def find_free_position():
    for index, occupied in enumerate(occupied_positions):
        if not occupied:
            return index
    return None  # Se todas as posições estiverem ocupadas

# Função que ajusta a posição e o tamanho da janela
def set_window_position_and_size(driver, position_index):
    x, y = positions[position_index]
    driver.set_window_size(window_width, window_height)
    driver.set_window_position(x, y)
    # Marcar a posição como ocupada
    occupied_positions[position_index] = True

# Função para liberar a posição quando a aba é fechada
def release_position(position_index):
    occupied_positions[position_index] = False

# Função para enviar o e-mail com o eBook
def send_email(user_email, ebook_path):
    try:
        print(f"Enviando e-mail de {EMAIL_ADDRESS} para {user_email} através de {SMTP_SERVER}:{SMTP_PORT}")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = 'Seu eBook Gerado'
        
        body = 'Prezado(a),\n\nSeu eBook gerado está anexado a este e-mail.\n\nAtenciosamente,\nEquipe'
        msg.attach(MIMEText(body, 'plain'))
        
        with open(ebook_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(ebook_path)}')
            msg.attach(part)

        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                print(f"Realizando login com {EMAIL_ADDRESS}")
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(EMAIL_ADDRESS, user_email, text)
                print(f"E-mail enviado com sucesso para {user_email}")
        else:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                print(f"Realizando login com {EMAIL_ADDRESS}")
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(EMAIL_ADDRESS, user_email, text)
                print(f"E-mail enviado com sucesso para {user_email}")

    except Exception as e:
        print(f"Erro ao enviar o e-mail para {user_email}: {e}")

# Função para processar cada usuário
def process_user(user_id):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    service = Service(ChromeDriverManager().install())

    driver = uc.Chrome(service=service, options=chrome_options)
    
    # Aguarda um curto período para garantir que a janela esteja pronta
    time.sleep(2)

    # Use um lock para garantir que apenas uma aba seja aberta e posicionada por vez
    with position_lock:
        # Encontre a primeira posição livre
        free_position = find_free_position()
        
        if free_position is not None:
            # Define a posição e o tamanho da aba
            set_window_position_and_size(driver, free_position)
        else:
            # Caso não haja posição livre, fecha o driver
            driver.quit()
            return

    try:
        # Gera o eBook e salva o caminho
        ebook_path = generate_ebook(user_id, driver)
        # Adicione um log para verificar o caminho retornado
        print(f"Caminho do eBook gerado: {ebook_path}")

        if ebook_path is None:
            raise ValueError("Caminho do eBook não retornado pela função generate_ebook.")

        # Recupera o e-mail do usuário
        user_email = get_email_by_user_id(user_id)
        # Envia o eBook para o e-mail do usuário
        send_email(user_email, ebook_path)
    except Exception as e:
        print(f"Erro ao processar o usuário {user_id} no envio do eBook: {e}")

    finally:
        driver.quit()
        print(f"Processamento concluído para o usuário {user_id}. Fechando o navegador.")
        # Libera a vaga e chama o próximo item da fila com um atraso
        release_position(free_position)
        time.sleep(TASK_QUEUE_DELAY)  # Aguarda um tempo antes de processar o próximo
        release_tab_and_process_queue()

# Função para liberar vaga e chamar o próximo item da fila
def release_tab_and_process_queue():
    # Libera uma vaga no semáforo
    tab_semaphore.release()
    
    if not task_queue.empty():
        next_user_id = task_queue.get()
        print(f"Chamando a fila para processar o usuário {next_user_id}")
        # Inicia um novo thread para processar o próximo usuário
        threading.Thread(target=process_user, args=(next_user_id,)).start()

#
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#
@app.route('/loja')
def loja():
    return render_template('loja.html')

#
@app.route('/user/visitante')
def visit_user():
    if 'user_id' in session:
        return render_template('perfil_visita.html')
    else:
        return redirect(url_for('login'))

#
@app.route('/user')
def user():
    if 'user_id' in session:
        return render_template('perfil.html')
    else:
        return redirect(url_for('login'))

#
@app.route('/premium')
def premium():
    if 'user_id' in session:
        return render_template('premium.html')
    else:
        return redirect(url_for('login'))

#
@app.route('/formulario', methods=['GET', 'POST'])
def vendas():
    if 'user_id' in session:
        return render_template('vendas.html')
    else:
        return redirect(url_for('login'))

#
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

#
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

#
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

            # Verifica se há uma vaga disponível
            if tab_semaphore.acquire(blocking=False):
                # Se uma vaga está disponível, processa imediatamente
                flash('Formulário enviado com sucesso! Aguarde o eBook gerado.', 'success')
                print(f'Aba aberta para o usuário {user_id}')
                
                def process():
                    with startup_lock:
                        time.sleep(STARTUP_DELAY)
                    threading.Thread(target=process_user, args=(user_id,)).start()

                threading.Thread(target=process).start()
            else:
                # Se todas as abas estão ocupadas, adiciona à fila
                flash('A fila de abas está cheia. Sua solicitação foi adicionada à fila de espera.', 'warning')
                print(f"Solicitação do usuário {user_id} adicionada à fila de espera.")
                task_queue.put(user_id)

        except Exception as e:
            print(f"Erro durante a submissão do formulário ou geração do eBook: {e}")
            flash('Houve um erro ao enviar o formulário. Tente novamente ou entre em contato.', 'warning')
        
        return redirect(url_for('home'))

    return redirect(url_for('login'))

#
@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))

#
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
