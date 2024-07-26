def get_full_prompt(name):
    return (f'Vou fornecer um padrão para a criação de um livro, e você deve seguir rigorosamente este padrão. '
            f'Preciso de um livro completo com base nas respostas de um formulário que será enviado abaixo e na área do assunto citado. '
            f'O livro deve ser extensivo e detalhado, com aproximadamente 20 páginas no total. A estrutura deve ser a seguinte: '
            f'1. **Capa**: - Título: "Título e subtítulo de sua escolha" - Autor: {name} '
            f'2. **Introdução**: - Na próxima página, apresente o propósito do livro e o que será coberto, fornecendo uma visão geral clara e detalhada sobre o assunto. '
            f'3. **Sumário**: - Na próxima página, liste os principais tópicos (10) que serão abordados. Não precisa detalhar, apenas forneça os tópicos. '
            f'4. **Conteúdo Principal**: - Para cada tópico, desenvolva o texto extensivamente. Cada tópico deve ter aproximadamente 3000-4000 palavras e ser estruturado da seguinte forma: '
            f' - **Introdução**: Apresente o tópico com uma visão geral completa, explicando seu significado e importância no contexto do assunto. '
            f' - **Análise Detalhada**: Explore profundamente o tópico, dissertando sobre ele e discutindo suas principais características, implicações e fundamentos teóricos com riqueza de detalhes. '
            f' - **Exemplos Práticos**: Forneça vários exemplos práticos, estudos de caso ou histórias relevantes que ilustrem o tópico em ação de maneira abrangente. '
            f' - **Tendências Futuras**: Analise as tendências emergentes, inovações e como o tópico pode evoluir no futuro, fornecendo uma visão detalhada. '
            f' - **Desafios e Soluções**: Identifique problemas comuns relacionados ao tópico e ofereça soluções ou estratégias para superá-los, com explicações detalhadas. '
            f' - **Impacto na Indústria**: Discuta como o tópico influencia a indústria ou setor relevante, incluindo benefícios e desafios, com uma análise profunda. '
            f' - **Recomendações Práticas**: Ofereça recomendações detalhadas e práticas para aplicar o conhecimento sobre o tópico de maneira eficaz, com exemplos e orientações precisas. '
            f' - **Conclusão**: Recapitule os pontos principais discutidos no tópico e forneça uma visão geral das conclusões, resumindo os principais aprendizados e implicações. '
            f'Cada seção deve ser desenvolvida de forma extensa e profunda, proporcionando um conteúdo rico e detalhado. O objetivo é garantir que o livro seja abrangente e informativo. '
            f'5. **Conclusão Geral**: - Na última página, resuma os principais pontos discutidos em todo o livro e forneça uma visão geral abrangente das conclusões finais, consolidando as principais ideias e aprendizados. Lembrando, preciso de aproximadamente de 20 folhas de livro. '
            f'Por favor, só responda quando o conteúdo completo tiver sido gerado e enviado, conforme o padrão detalhado acima.')

def get_responses_prompt(responses_text):
    return (f'Por favor, gere um texto extenso e detalhado baseado nas respostas a seguir, seguindo o padrão de livro descrito acima. '
            f'Responda em plaintext, como se fosse um código, com o botão de copiar código para facilitar. '
            f'O conteúdo deve ser tão extenso e detalhado quanto um livro, com aproximadamente 20 páginas, e deve seguir rigorosamente a estrutura especificada. \n\n'
            f'{responses_text}')
