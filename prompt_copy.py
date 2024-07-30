#teste

def get_initial_prompt(name):
    return (f'Olá! Você está prestes a criar um eBook para um CEO. Você receberá instruções para gerar um eBook completo e detalhado, seguindo um padrão específico. '
            f'Primeiro, você irá receber as respostas de um formulário. Com base nessas respostas, você deverá criar o eBook conforme o padrão fornecido. '
            f'O eBook será dividido nas seguintes partes: Capa, Sumário, Introdução, Conteúdo Principal e Conclusão. '
            f'Irei pedir parte por parte, um por um.'
            f'Na parte da capa, por favor, forneça um título e subtítulo (se desejar) e o nome do autor que é {name}.'
            f'Após isso, pedirei o Sumário, onde irá fornecer 10 capítulos e depois a Introdução, que deverá abordar um pouco de cada assunto. '
            f'Já no Conteúdo Principal, seja extenso e detalhista, abordando as respostas do formulário e abrangendo para falar da área e '
            f'assuntos recorrentes, seja extenso. Já na conclusão, aborde o geral, o futuro e dicas sobre.'
            f'Aguarde para a próxima etapa, não responda!')
            
def responses(responses_text):
    return (f"Essas são as respostas do formulário: \n\n{responses_text}\n\n Mas ainda não responda! Espere a próxima mensagem.")

def get_cover_prompt(name):
    return (f'Capa: Título: (Título de sua escolha) - Autor: {name}')

def get_table_of_contents_prompt():
    return (f'2. **Sumário**: - Liste os principais tópicos (10) que serão abordados no eBook. Não precisa detalhar, apenas forneça os tópicos.')

def get_intro_prompt():
    return (f'3. **Introdução**: - Apresente o propósito do eBook e o que será coberto, fornecendo uma visão geral clara e detalhada sobre o assunto.')

def get_content_prompt():
    return (f'4. **Conteúdo Principal**: - Desenvolva aproximadamente 15.000 palavras para cada tópico listado no Sumário. Baseie-se nas respostas fornecidas e crie textos longos e detalhados para cada tópico. Lembre-se de seguir a estrutura especificada e garantir que o conteúdo seja rico e informativo.')

def get_conclusion_prompt():
    return (f'5. **Conclusão**: - Recapitule os principais pontos discutidos no conteúdo e forneça uma visão geral das conclusões, resumindo os principais aprendizados e implicações.')
