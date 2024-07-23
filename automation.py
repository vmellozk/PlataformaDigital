from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def chatgpt_response(responses_file, response_file, name):
    # Reinicie o WebDriver para garantir uma nova sessão
    driver = webdriver.Chrome()
    driver.get('https://chat.openai.com')

    # Aguarde até o campo de entrada de texto estar presente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'textarea'))
    )

    # Limpe o campo de entrada de texto
    input_box = driver.find_element(By.TAG_NAME, 'textarea')
    input_box.clear()

    # Lê o texto do arquivo de respostas
    with open(responses_file, 'r') as file:
        responses_text = file.read()

    full_prompt = f"""
    Crie um eBook com base nas respostas do formulário abaixo. O eBook deve seguir a estrutura abaixo:

    1. **Capa**: 
    - Título: "Insights do Formulário"
    - Autor: {name}

    2. **Introdução**: 
    - Apresente o propósito do eBook e o que será coberto.

    3. **Sumário**: 
    - Liste as principais seções e tópicos que serão abordados.

    4. **Conteúdo Principal**:
    - Divida o conteúdo em 5 seções, com base nas respostas do formulário.
    - Cada seção deve cobrir um conjunto específico de respostas e ser apresentada de forma clara e concisa.
    - Disserte também sobre a área comentada na resposta e abrança falando do mercado atual e futuro, contando as evoluções e afins.

    5. **Conclusão**: 
    - Resuma os principais pontos discutidos e forneça uma visão geral das conclusões.

    Use o texto a seguir para compor o conteúdo do eBook:

    {responses_text}

    Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha o conteúdo relevante e focado nos insights extraídos das respostas do formulário.
    """

    # Envia o texto do prompt
    input_box.send_keys(full_prompt)
    
    # Adiciona um print para verificar o texto enviado
    print("Texto do prompt enviado:")
    print(full_prompt)

    # Aguarde até o botão de envio estar disponível e clicável
    try:
        print("Aguardando o botão de envio...")
        send_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="send-button"]'))
        )
        send_button.click()
        print("Botão de envio clicado.")
    except Exception as e:
        print("Erro ao encontrar ou clicar no botão de envio:", e)
        driver.quit()
        return

    # Aguarde a resposta ser gerada e localize o botão de copiar
    print("Aguardando resposta...")
    try:
        # Aguarde até que o botão de copiar esteja clicável
        copy_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.rounded-lg'))
        )
        copy_button.click()
        print("Botão de copiar clicado.")

        # Aguarde um pouco para garantir que o texto tenha sido copiado
        sleep(5)
        
        # Obtém o texto copiado da área de transferência
        response_text = driver.execute_script("return navigator.clipboard.readText();")
        
        print("Resposta recebida:")
        print(response_text)
        
        # Salva o texto copiado em um arquivo
        with open(response_file, 'w') as file:
            file.write(response_text)
    except Exception as e:
        print("Erro ao capturar a resposta:", e)
    finally:
        # Fecha o WebDriver
        driver.quit()
