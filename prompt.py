def get_full_prompt(name):
    return (f'Vamos brincar! Você trabalha numa livraria, e recebe uma demanda de um CEO para gerar um novo livro. Você recebe a seguinte mensagem dele.'
            f'Vou fornecer um padrão para a criação de um eBook, e você deve seguir rigorosamente este padrão. Mas ele irá se basear em respostas que virá de um formulário, '
            f'então só responda quando for enviado as resposta desse formulário.'
            f'Preciso de um eBook completo com base nas respostas do formulário que será enviado abaixo e na área do assunto citado. '
            f'O eBook deve ser extensivo e detalhado, com aproximadamente 50000 palavras no total. A estrutura deve ser a seguinte: '
            f'1. **Capa**: - Título: (Título e subtítulo de sua escolha) - Autor: {name} '
            f'2. **Introdução**: - Nessa página, apresente o propósito do eBook e o que será coberto, fornecendo uma visão geral clara e detalhada sobre o assunto. '
            f'3. **Sumário**: - Aqui liste os principais tópicos (10) que serão abordados. Não precisa detalhar, apenas forneça os tópicos. '
            f'4. **Conteúdo Principal**: - Para cada tópico do sumário, desenvolva aproximadamente 15.000 palavras. '
            f'Faça com que de acordo com o sumário, tenha textos longos até finalizar o assunto e pular para o próximo. '
            f'Seja interativo com o leitor e disserte tudo sobre aquele determinado tópico, citando também o geral da área de atuação em relação aquilo citado, '
            f'fazendo assim com que cada seção de assunto seja a mais completa possível! Quero um ebook grande! '
            f' - **Conclusão**: Recapitule os pontos principais discutidos no tópico e forneça uma visão geral das conclusões, resumindo os principais aprendizados e implicações. '
            f'Cada seção do conteúdo principal deve ser desenvolvida de forma extensa e profunda, proporcionando um conteúdo rico e detalhado. O objetivo é garantir que o eBook seja abrangente e informativo. Tenha em média de 5000 palavras por tópico. '
            f'5. **Conclusão Geral**: - Na última página, resuma os principais pontos discutidos em todo o eBook e forneça uma visão geral abrangente das conclusões finais, consolidando as principais ideias e aprendizados. Lembrando, preciso de aproximadamente de 12 folhas de eBook. '
            f'SÓ RESPONDA QUANDO O CONTEÚDO DAS RESPOSTAS TIVER SIDO ENVIADO!')

def get_responses_prompt(responses_text):
    return (f'Por favor, gere um texto extenso e detalhado BASEADO NAS RESPOSTAS A SEGUIR, seguindo o padrão de eBook descrito acima. '
            f'O conteúdo deve ser tão extenso e detalhado quanto um eBook, com aproximadamente 50.000 palavras no total, e um texto extenso por tópico. Lembrando que deve seguir rigorosamente a estrutura especificada. \n\n'
            f'{responses_text}')