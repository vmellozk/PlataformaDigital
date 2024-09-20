#
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
from configuracoes_driver import ConfiguracoesDriver
from configuracoes_driver import ConfiguracoesDriver

#
configuracoes = ConfiguracoesDriver()

# Função para enviar o e-mail com o eBook
def send_email(user_email, ebook_path):
    try:
        #
        print(f"Enviando e-mail de {configuracoes.EMAIL_ADDRESS} para {user_email} através de {configuracoes.SMTP_SERVER}:{configuracoes.SMTP_PORT}")
        msg = MIMEMultipart()
        msg['From'] = configuracoes.EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = 'Seu eBook Gerado'
        
        #
        body = 'Prezado(a),\n\nSeu eBook gerado está anexado a este e-mail.\n\nAtenciosamente,\nEquipe'
        msg.attach(MIMEText(body, 'plain'))
        
        #
        with open(ebook_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(ebook_path)}')
            msg.attach(part)

        #
        if configuracoes.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(configuracoes.SMTP_SERVER, configuracoes.SMTP_PORT) as server:
                print(f"Realizando login com {configuracoes.EMAIL_ADDRESS}")
                server.login(configuracoes.EMAIL_ADDRESS, configuracoes.EMAIL_PASSWORD)
                text = msg.as_string()
                server.sendmail(configuracoes.EMAIL_ADDRESS, user_email, text)
                print(f"E-mail enviado com sucesso para {user_email}")
        #
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
