import time
import threading
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from models import insert_user, get_user_by_email, insert_survey_response, get_email_by_user_id
from generate_Ebook import generate_ebook
from configuracoes_driver import ConfiguracoesDriver
from send_email import send_email
from kiwify import kiwify_automation
from selenium.common.exceptions import InvalidSessionIdException

#
app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Instancia a classe ConfiguracoesDriver
configuracoes = ConfiguracoesDriver()

# Função para processar cada usuário
def process_user(user_id):
    driver = configuracoes.create_driver()  # Usa o método da classe para criar o driver
    time.sleep(configuracoes.STARTUP_DELAY)
    # Use um lock para garantir que apenas uma aba seja aberta e posicionada por vez
    with configuracoes.position_lock:
        # Encontre a primeira posição livre
        free_position = configuracoes.find_free_position()
        if free_position is not None:
            # Define a posição e o tamanho da aba
            configuracoes.set_window_position_and_size(driver, free_position)
        else:
            # Caso não haja posição livre, fecha o driver
            if driver.session_id:
                try:
                    driver.close()
                except InvalidSessionIdException:
                    print("Sessão do driver já encerrada ao tentar fechar.")
            return

    try:
        # Gera o eBook e salva o caminho
        ebook_path = generate_ebook(user_id, driver)
        print(f"Caminho do eBook gerado: {ebook_path}")
        if ebook_path is None:
            raise ValueError("Caminho do eBook não retornado pela função generate_ebook.")
        
        # Cadastra o produto na plataforma do kiwify
        kiwify_automation(driver, user_id)

        # Envia o email para o usuário
        user_email = get_email_by_user_id(user_id)
        send_email(user_email, user_id)

    except Exception as e:
        print(f"Erro ao processar o usuário {user_id} no envio do eBook: {e}")

    finally:
        if driver.session_id:  # Verifica se a sessão ainda está ativa
            try:
                driver.close()
            except InvalidSessionIdException:
                print(f"Sessão do driver já encerrada ao tentar fechar no finally para o usuário {user_id}.")
        print(f"Processamento concluído para o usuário {user_id}. Fechando o navegador.")
        configuracoes.release_position(free_position)
        time.sleep(configuracoes.TASK_QUEUE_DELAY)
        release_tab_and_process_queue()

# Função para liberar vaga e chamar o próximo item da fila
def release_tab_and_process_queue():
    # Libera uma vaga no semáforo
    configuracoes.tab_semaphore.release()
    if not configuracoes.task_queue.empty():
        next_user_id = configuracoes.task_queue.get()
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
            if configuracoes.tab_semaphore.acquire(blocking=False):
                # Se uma vaga está disponível, processa imediatamente
                flash('Formulário enviado com sucesso! Aguarde o eBook gerado.', 'success')
                print(f'Aba aberta para o usuário {user_id}')
                
                def process():
                    with configuracoes.startup_lock:
                        time.sleep(configuracoes.STARTUP_DELAY)
                    threading.Thread(target=process_user, args=(user_id,)).start()

                threading.Thread(target=process).start()
            else:
                # Se todas as abas estão ocupadas, adiciona à fila
                flash('A fila de abas está cheia. Sua solicitação foi adicionada à fila de espera.', 'warning')
                print(f"Solicitação do usuário {user_id} adicionada à fila de espera.")
                configuracoes.task_queue.put(user_id)

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
