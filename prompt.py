def get_initial_prompt():
    return (f'Olá! Você está prestes a criar um eBook para um cliente. Você receberá instruções para gerar um eBook completo e detalhado, seguindo um padrão específico. '
            f'Primeiro, você irá receber os prompts, e depois vou mandar as respostas. Com base nessas respostas, eu vou te pedir para criar o ebook no padrão fornecido. Enquanto não houver pedido de prompt sobre o ebook responda "OK" para tudo que vier, ou seja; responda OK nessa mensagem e na próxima, onde virá as respostas. '
            f'O eBook será dividido nas seguintes partes: Capa, Sumário, Introdução, Conteúdo Principal e Conclusão. '
            f'Agora eu vou te passar os prompts, e depois vou passar as respostas. '
            f'####Capa: (vou pedir de forma separada)'
            f'####Introdução: apresente o propósito do eBook e o que será coberto, fornecendo uma visão geral, clara e breve sobre o assunto.'
            f' ####Sumário: serão 10 tópicos onde serão listados os assuntos que serão abordados ao longo do ebook. Os tópicos serão de sua escolha, mas tem que ter relação com as respostas.'
            f'E, chegando na parte mais importante, desenvolva o ####Conteúdo: será composto por textos longos para cada tópico listado no sumário, depois vá dissertando sobre. Baseie-se nas respostas fornecidas e crie textos longos e detalhados para cada tópico. '
            f'####Conclusão: por fim, recapitule os principais pontos discutidos no conteúdo e forneça uma visão geral, resumindo os principais aprendizados e implicações, e um pouco mais do ponto de vista relacionando ao assunto, tudo em um único texto, sem separar. '
            f'Lembre-se de seguir a estrutura especificada e garantir que o conteúdo seja rico e informativo, com bastante informação. '
            f'Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. '
            f'Primeiro eu vou passar as respostas, mas NÃO RESPONDA! Vou te pedir o título separado do conteúdo. Espere o pedido. Responda somente OK agora e quando eu enviar as respostas você responda OK também e aguarde as instruções.')

def responses(responses_text):
    return (f"{responses_text}")

def tittle(name):
    return(f'Para começar, me forneça a capa da seguinte forma: ####Capa, com Título e junto com o nome do autor que é: {name}". O título será de sua escolha. Lembre-se de utilizar 4 hash antes da palavra capa. Apenas responda o que foi pedido, sem essa foi a resposta, se precisar de mais..." não quero nada disso. ')
