from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def chatgpt_response(responses_file, response_file, name):
    driver = webdriver.Edge()
    driver.get('https://chat.openai.com')

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
    - Disserte também sobre a área comentada na resposta e abranja falando do mercado atual e futuro, contando as evoluções e afins.

    5. **Conclusão**: 
    - Resuma os principais pontos discutidos e forneça uma visão geral das conclusões.

    Use o texto a seguir para compor o conteúdo do eBook:

    {responses_text}

    Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha o conteúdo relevante e focado nos insights extraídos das respostas do formulário.
    """

    input_box = driver.find_element(By.TAG_NAME, 'textarea')
    input_box.send_keys(full_prompt)
    input_box.send_keys(Keys.RETURN)
    sleep(10)

    response = driver.find_element(By.CSS_SELECTOR, 'div-response-class').text
    with open(response_file, 'w') as file:
        file.writelines(response)

    driver.quit()
