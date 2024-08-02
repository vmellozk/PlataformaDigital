def get_initial_prompt():
    return (f'Olá! Você está prestes a criar um eBook para um cliente. Você receberá instruções para gerar um eBook completo e detalhado, seguindo um padrão específico. '
            f'Primeiro, você irá receber as respostas de um formulário. Com base nessas respostas, eu vou te pedir item por item e você deverá criar o eBook conforme o padrão fornecido. '
            f'O eBook será dividido nas seguintes partes: Capa, Sumário, Introdução, Conteúdo Principal e Conclusão. '
            f'Só responda quando eu te pedir um item por item, agora vou mandar as respostas, mas não responda nada ainda.')
            
def responses(responses_text):
    return (f"{responses_text}")

def get_cover_prompt(name):
    return (f'Responda para a capa da seguinte forma: "Título by {name}". Onde o título será de sua escolha. Apenas responda o que foi pedido, sem "esse foi o taltal, se precisar de mais..." não quero nada disso.')

def get_table_of_contents_prompt():
    return (f'Liste os principais tópicos (10) no sumário que serão abordados no eBook. Os tópicos serão de sua escolha, mas tem que ter relação as respostas. Apenas responda o que foi pedido, sem "esse foi o taltal, se precisar de mais..." não quero nada disso.')

def get_intro_prompt():
    return (f'Apresente o propósito do eBook e o que será coberto, fornecendo uma visão geral clara e detalhada sobre o assunto. Apenas responda o que foi pedido, sem "esse foi o taltal, se precisar de mais..." não quero nada disso.')

def get_content_prompt():
    return (f'Desenvolva um texto longo para cada tópico listado no Sumário, depois vá dissertando sobre. Baseie-se nas respostas fornecidas e crie textos longos e detalhados para cada tópico. Lembre-se de seguir a estrutura especificada e garantir que o conteúdo seja rico e informativo, com bastante informação. Apenas responda o que foi pedido, sem "esse foi o taltal, se precisar de mais..." não quero nada disso.')

def get_conclusion_prompt():
    return (f'Recapitule os principais pontos discutidos no conteúdo e forneça uma visão geral das conclusões, resumindo os principais aprendizados e implicações, tudo em um único texto, sem separar. Apenas responda o que foi pedido, sem "esse foi o taltal, se precisar de mais..." não quero nada disso.')
