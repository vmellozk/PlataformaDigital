import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from configuracoes_driver import ConfiguracoesDriver

# Instância das configurações
configuracoes = ConfiguracoesDriver()

# Função para enviar o e-mail com o eBook
def send_email(user_email, user_id):
    try:
        print(f"Enviando e-mail de {configuracoes.EMAIL_ADDRESS} para {user_email} através de {configuracoes.SMTP_SERVER}:{configuracoes.SMTP_PORT}")
        
        # Criando a mensagem do e-mail
        msg = MIMEMultipart()
        msg['From'] = configuracoes.EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = 'Seu eBook Gerado'
        
        # Lê o link do arquivo .txt
        user_folder_link = os.path.join("users", str(user_id))
        file_path_link = os.path.join(user_folder_link, "botao_copiar_link_afiliado.txt")
        
        # Imprime o caminho do arquivo para depuração
        print(f"Caminho do arquivo: {file_path_link}")
        
        # Verifica se o arquivo existe
        if not os.path.isfile(file_path_link):
            print(f"Erro: O arquivo não foi encontrado: {file_path_link}")
            return
        
        with open(file_path_link, "r", encoding="utf-8") as file:
            link = file.read().strip()

        # Atualiza o corpo do e-mail para incluir o link
        body = f'Prezado(a),\n\nSeu eBook gerado está disponível no seguinte link: {link}\n\nAtenciosamente,\nEquipe'
        msg.attach(MIMEText(body, 'plain'))

        # Enviando o e-mail
        if configuracoes.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(configuracoes.SMTP_SERVER, configuracoes.SMTP_PORT) as server:
                print(f"Realizando login com {configuracoes.EMAIL_ADDRESS}")
                server.login(configuracoes.EMAIL_ADDRESS, configuracoes.EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(configuracoes.EMAIL_ADDRESS, user_email, text)
                print(f"E-mail enviado com sucesso para {user_email}")
        else:
            with smtplib.SMTP(configuracoes.SMTP_SERVER, configuracoes.SMTP_PORT) as server:
                server.starttls()
                print(f"Realizando login com {configuracoes.EMAIL_ADDRESS}")
                server.login(configuracoes.EMAIL_ADDRESS, configuracoes.EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(configuracoes.EMAIL_ADDRESS, user_email, text)
                print(f"E-mail enviado com sucesso para {user_email}")

    except Exception as e:
        print(f"Erro ao enviar o e-mail para {user_email}: {e}")

#if __name__ == "__main__":
    #send_email(user_email='contato.devictormello@gmail.com', user_id=1)
