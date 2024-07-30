def get_cover_prompt(name):
    return (f'1. **Capa**: - Título: (Título e subtítulo de sua escolha) - Autor: {name}')

def get_intro_prompt():
    return (f'2. **Introdução**: - Nessa página, apresente o propósito do eBook e o que será coberto, fornecendo uma visão geral clara e detalhada sobre o assunto.')

def get_table_of_contents_prompt():
    return (f'3. **Sumário**: - Aqui liste os principais tópicos (10) que serão abordados. Não precisa detalhar, apenas forneça os tópicos.')

def get_content_prompt(responses_text):
    return (f'4. **Conteúdo Principal**: - Para cada tópico do sumário, desenvolva aproximadamente 15.000 palavras. Faça com que de acordo com o sumário, tenha textos longos até finalizar o assunto e pular para o próximo. Seja interativo com o leitor e disserte tudo sobre aquele determinado tópico, citando também o geral da área de atuação em relação aquilo citado, fazendo assim com que cada seção de assunto seja a mais completa possível! Quero um ebook grande! Lembrando que deve seguir rigorosamente a estrutura especificada. \n\n{responses_text}')

def get_conclusion_prompt():
    return (f'5. **Conclusão**: - Recapitule os pontos principais discutidos no tópico e forneça uma visão geral das conclusões, resumindo os principais aprendizados e implicações.')

def get_final_conclusion_prompt():
    return (f'6. **Conclusão Geral**: - Na última página, resuma os principais pontos discutidos em todo o eBook e forneça uma visão geral abrangente das conclusões finais, consolidando as principais ideias e aprendizados.')
