def get_full_prompt(name):
    return (f'Vou mandar um padrão de criação de eBook, mas não responda ainda! '
            f'Preciso de um eBook completo com base nas respostas de um formulário que será enviado '
            f'abaixo e da área do assunto citado. O eBook deve seguir a estrutura: '
            f'1. **Capa**: - Título: "Título e subtítulo de sua escolha" - Autor: {name} '
            f'2. **Introdução**: - Na próxima página, apresente o propósito do eBook e o que será coberto, explicando de forma abrangente e detalhada. '
            f'3. **Sumário**: - Na próxima página, liste os principais tópicos (10) que serão abordados, sem dissertar sobre, apenas um tópico. '
            f'4. **Conteúdo Principal**: - Para cada tópico, preencha o eBook com texto extenso e detalhado. Cada tópico deve ter aproximadamente 3000-4000 palavras, '
            f'com as seguintes seções detalhadas: '
            f' - **Introdução**: Apresente o tópico com uma visão geral completa, explicando seu significado e importância no contexto do assunto. '
            f' - **Análise Detalhada**: Explore profundamente o tópico, discutindo suas principais características, implicações e fundamentos teóricos. '
            f' - **Exemplos Práticos**: Forneça vários exemplos práticos, estudos de caso ou histórias relevantes que ilustrem o tópico em ação. '
            f' - **Tendências Futuras**: Analise as tendências emergentes, inovações e como o tópico pode evoluir no futuro. '
            f' - **Desafios e Soluções**: Identifique problemas comuns relacionados ao tópico e ofereça soluções ou estratégias para superá-los. '
            f' - **Impacto na Indústria**: Discuta como o tópico influencia a indústria ou setor relevante, incluindo benefícios e desafios. '
            f' - **Recomendações Práticas**: Ofereça recomendações detalhadas e práticas para aplicar o conhecimento sobre o tópico de maneira eficaz. '
            f' - **Conclusão**: Recapitule os pontos principais discutidos no tópico e forneça uma visão geral das conclusões. '
            f'Cada seção deve ser desenvolvida extensivamente, proporcionando um conteúdo rico e detalhado. O objetivo é garantir que o eBook tenha uma profundidade de conteúdo suficiente '
            f'para preencher cerca de 20 páginas. Certifique-se de que o conteúdo seja informativo, envolvente e bem estruturado. '
            f'5. **Conclusão Geral**: - Na última página, resuma os principais pontos discutidos em todo o eBook e forneça uma visão geral abrangente das conclusões finais. '
            f'Só responda na próxima mensagem, quando for enviado as respostas.')

def get_responses_prompt(responses_text):
    return f'Responda em plaintext, como se fosse um código, tendo o botão copiar código para facilitar. Disserto um livro sobre o conteúdo principal: \n{responses_text}'
