import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pyperclip

def chatgpt_response(responses_file, output_file, name):
    driver = uc.Chrome(version_main=126)

    try:
        driver.get('https://chat.openai.com')
        time.sleep(2)

        #Achando o elemento para 
        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(1)

        # Definir o foco no campo de entrada manualmente
        input_field.click()
        time.sleep(2)

        # Lê o texto do arquivo de respostas
        with open(responses_file, 'r') as file:
            responses_text = file.read()

        # Prompt
        full_prompt = (f'Vou mandar um padrão de criação de ebook, mas não responda! '
                       f'Preciso de um eBook com base nas respostas de um formulário que será enviado '
                       f'abaixo. O eBook deve seguir a estrutura: 1. **Capa**: - Título: "Insights '
                       f'do Formulário" - Autor: {name} 2. **Introdução**: - Apresente o propósito do eBook e o que será '
                       f'coberto. 3. **Sumário**: - Liste as principais seções e tópicos que serão abordados. 4. **Conteúdo '
                       f'Principal**: - Divida o conteúdo em 5 seções, com base nas respostas do formulário. - Cada seção '
                       f'deve cobrir um conjunto específico de respostas e ser apresentada de forma clara e concisa. - '
                       f'Disserte também sobre a área comentada na resposta e abrança falando do mercado atual e futuro, '
                       f'contando as evoluções e afins 5. **Conclusão**: - Resuma os principais pontos discutidos e forneça '
                       f'uma visão geral das conclusões. '
                       f'Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação '
                       f'limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha '
                       f'o conteúdo relevante e focado nos insights extraídos das respostas do formulário. '
                       f'Só responda na próxima mensagem, quando for enviado as respostas')

        # Inserir o prompt em partes menores
        for i in range(0, len(full_prompt), 5000):
            input_field.send_keys(full_prompt[i:i + 5000])
            time.sleep(3)

        # Pressionar Enter para enviar o prompt
        input_field.send_keys(Keys.ENTER)
        time.sleep(5)

        # Segundo prompt com a mensagem para resposta em plaintext
        responses_prompt = f'Responda em plaintext, como se fosse um código, tendo o botão copiar código para facilitar. Aqui estão as respostas: \n{responses_text}'

        # Enviar o segundo prompt
        input_field.send_keys(responses_prompt)
        time.sleep(2)
        input_field.send_keys(Keys.ENTER)

        #
        time.sleep(60)

        # Aguarda a resposta ser gerada e o botão de copiar estar disponível
        WebDriverWait(driver, 240).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copiar código')]"))
        )

        # Localiza o botão de copiar e clica nele
        try:
            print("Tentando localizar o botão de copiar.")
            copy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Copiar código')]")
            copy_button.click()
            time.sleep(2)

            copied_text = pyperclip.paste()
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(copied_text)

            print(f"Texto copiado e salvo como '{output_file}'.")

        except Exception as e:
            print(f"Erro durante a automação: {e}")

    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")