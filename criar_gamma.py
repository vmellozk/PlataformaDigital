import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.common.keys import Keys

resposta = '''Explorando Novos Horizontes
Victor Hugo de Souza Mello
Prática Sênior
Introdução
Neste eBook, convido você a embarcar em uma jornada de descobertas e reflexões sobre temas
que, embora possam parecer simples à primeira vista, são fundamentais para nosso crescimento
pessoal e profissional. Ao longo dos capítulos, exploraremos conceitos que nos ajudam a entender
melhor nosso papel no mundo, a importância de cada escolha que fazemos e como podemos, de
fato, moldar nosso próprio destino. Acredito que cada um de nós tem o potencial de transformar
sua realidade, e este material foi criado com o intuito de inspirar e motivar essa transformação.
Você encontrará, nas próximas páginas, uma série de tópicos que foram cuidadosamente
selecionados com base em reflexões e experiências que muitos de nós compartilhamos. Cada
seção é uma oportunidade para se aprofundar em ideias e práticas que podem ser aplicadas em
nossa vida cotidiana. Estou animado para compartilhar esses insights e espero que eles ressoem
com você, assim como ressoaram em minha própria jornada.
Prática Sênior
Sumário
1. A Importância do Autoconhecimento
2. Como Definir Objetivos Claros
3. Estratégias para Gerenciamento do Tempo
4. O Papel das Relações Interpessoais
5. Superando Desafios e Adversidades
6. A Influência do Pensamento Positivo
7. O Valor da Resiliência
8. Aprendendo com o Fracasso
9. Práticas de BemEstar e Saúde Mental
Prática Sênior
Conteúdo
1. A Importância do Autoconhecimento
O autoconhecimento é a base de qualquer transformação pessoal. Sem entender quem somos, é
difícil tomar decisões que reflitam nossos verdadeiros desejos e valores. Ao longo deste capítulo,
abordaremos técnicas para se conhecer melhor, como a prática da autoreflexão e a importância de
feedbacks honestos de pessoas próximas. Aprender a ouvir nossas próprias emoções e reconhecer
nossas habilidades e fraquezas pode ser um divisor de águas. Por exemplo, ao me aprofundar em
minhas próprias motivações, percebi padrões que antes me escapavam, permitindome fazer
escolhas mais alinhadas com meu verdadeiro eu.
2. Como Definir Objetivos Claros
Definir objetivos claros é essencial para direcionar nossos esforços. Neste tópico, discutiremos a
importância de estabelecer metas SMART (específicas, mensuráveis, atingíveis, relevantes e
temporais). Compartilharei algumas de minhas experiências na formulação de objetivos e como o
fato de ter clareza sobre o que quero me ajudou a traçar um caminho mais eficaz. Além disso,
veremos como a visualização e o acompanhamento do progresso são ferramentas poderosas para
Prática Sênior
manter a motivação.
3. Estratégias para Gerenciamento do Tempo
Gerenciar o tempo é um desafio que muitos enfrentam, e é fundamental para alcançar nossos
objetivos. Aqui, exploraremos diversas técnicas, como a matriz de Eisenhower e a técnica
Pomodoro. Vou compartilhar algumas das estratégias que adotei ao longo dos anos e como elas
me ajudaram a aumentar minha produtividade sem comprometer meu bemestar. O gerenciamento
do tempo não é apenas sobre eficiência; é também sobre priorizar o que realmente importa em
nossas vidas.
4. O Papel das Relações Interpessoais
Nossas relações interpessoais moldam nossas experiências e nos ajudam a crescer. Neste
capítulo, discutiremos a importância de construir uma rede de apoio e como as interações humanas
podem influenciar nosso estado emocional e sucesso. Através de histórias pessoais e exemplos
práticos, veremos como cultivar relacionamentos saudáveis pode enriquecer nossas vidas e
Prática Sênior
oferecer suporte em momentos difíceis.
5. Superando Desafios e Adversidades
Desafios são inevitáveis, mas como respondemos a eles pode fazer toda a diferença. Aqui,
abordaremos estratégias para enfrentar dificuldades e transformar obstáculos em oportunidades de
aprendizado. Compartilharei momentos em que enfrentei adversidades e como esses episódios me
ensinaram lições valiosas sobre perseverança e adaptabilidade. O foco será em desenvolver uma
mentalidade que veja os desafios como parte do processo de crescimento.
6. A Influência do Pensamento Positivo
O pensamento positivo pode parecer um conceito simples, mas sua influência em nossa vida é
profunda. Neste capítulo, exploraremos como cultivar uma mentalidade positiva pode impactar
nossa saúde mental e nossas interações. Discutiremos práticas como a gratidão e a visualização
positiva, que têm me ajudado a manter uma perspectiva otimista, mesmo diante de dificuldades.
Prática Sênior
7. O Valor da Resiliência
A resiliência é a capacidade de se recuperar rapidamente de desafios. Discutiremos a importância
de desenvolver essa habilidade e como ela nos permite enfrentar as adversidades com coragem e
determinação. Compartilharei histórias de pessoas que admiramos por sua resiliência e o que
podemos aprender com elas. Aprender a se adaptar e continuar avançando é fundamental em um
mundo em constante mudança.
8. Aprendendo com o Fracasso
O fracasso é frequentemente visto como algo negativo, mas é, na verdade, uma oportunidade de
aprendizado. Neste tópico, vamos explorar como podemos reconfigurar nossa visão sobre o
fracasso e utilizálo como uma ferramenta de crescimento. Contarei experiências pessoais em que
fracassei, mas que resultaram em lições valiosas que moldaram meu caminho.
Prática Sênior
9. Práticas de BemEstar e Saúde Mental
A saúde mental é um componente essencial de nossa qualidade de vida. Aqui, discutiremos
práticas que podem ajudar a manter um estado mental saudável, como meditação, exercícios
físicos e cuidados com a alimentação. Compartilharei minha própria rotina de bemestar e como
pequenas mudanças podem ter um grande impacto em nossa vida diária.
Prática Sênior
Conclusão
Ao encerrarmos este eBook, é essencial recapitular os principais pontos discutidos. O
autoconhecimento, a definição de objetivos claros, o gerenciamento do tempo e as relações
interpessoais são todos fundamentais para nosso desenvolvimento. Cada um de nós tem o
potencial de enfrentar desafios e se transformar em versões melhores de si mesmos. Espero que
este material tenha oferecido insights valiosos e que você se sinta inspirado a aplicar esses
conceitos em sua vida. O caminho à frente é cheio de oportunidades, e estou animado para ver
como você pode transformar suas experiências em aprendizados significativos.
Neste eBook, cobrimos uma variedade de temas que estão interligados e que podem enriquecer
nossa jornada pessoal e profissional. Desde a importância do autoconhecimento até as práticas
que promovem o bemestar, cada um desses tópicos é uma peça fundamental do quebracabeça
que é a vida. Espero que você tenha encontrado valor nas reflexões e que elas o inspirem a
continuar em sua própria jornada de crescimento. Lembrese, o caminho pode ser desafiador, mas é
também repleto de oportunidades. Ao aplicar o que discutimos, você estará um passo mais perto de
alcançar seus objetivos e viver uma vida plena e significativa.
Prática Sênior'''

def  criar_gamma(driver, user_id):
    # Define a pasta de downloads específica para cada usuário
    user_folder_downloads = os.path.join("users", str(user_id), "downloads")
    os.makedirs(user_folder_downloads, exist_ok=True)  # Cria a pasta se não existir

    # Verifica e interage com o botão de 'Criar Novo'
    while True:
        try:
            criar_novo_ia = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/button[1]'))
            )
            if criar_novo_ia:
                print("criar_novo_ia encontrado")
                time.sleep(2)
                criar_novo_ia.click()
                time.sleep(1)
                break
            else:
                print("criar_novo_ia não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de criar_novo_ia")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de criar_novo_ia: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'Colar no texto'
    while True:
        try:
            colar_texto = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div/div[1]'))
            )
            if colar_texto:
                print("colar_texto encontrado")
                time.sleep(2)
                colar_texto.click()
                time.sleep(1)
                break
            else:
                print("colar_texto não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de colar_texto")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de colar_texto: {e}")
            time.sleep(1)

    # Verifica e interage com o input de 'cole_aqui' e Envia o texto com quebras de linha
    while True:
        try:
            cole_aqui = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/p'))
            )
            if cole_aqui:
                print("cole_aqui encontrado")
                time.sleep(2)
                cole_aqui.click()
                time.sleep(1)
                for chunk in resposta.split('\n'):
                    cole_aqui.send_keys(chunk)
                    cole_aqui.send_keys(Keys.SHIFT + Keys.ENTER)
                cole_aqui.send_keys(Keys.ENTER)
                time.sleep(3)
                break
            else:
                print("cole_aqui não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de cole_aqui")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de cole_aqui: {e}")
            time.sleep(1)

    # Verifica e interage com a div de 'documento'
    while True:
        try:
            documento = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]'))
            )
            if documento:
                print("documento encontrado")
                time.sleep(2)
                documento.click()
                time.sleep(1)
                break
            else:
                print("documento não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada a div de documento")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar a div de documento: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'continuar'
    while True:
        try:
            continuar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[3]'))
            )
            if continuar:
                print("continuar encontrado")
                time.sleep(2)
                continuar.click()
                time.sleep(1)
                break
            else:
                print("continuar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de continuar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de continuar: {e}")
            time.sleep(1)

    # Verifica e interage com o input de 'texto_detalhado'
    while True:
        try:
            texto_detalhado = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="accordion-panel-:rd3:"]/div/div[2]/div/button[3]'))
            )
            if texto_detalhado:
                print("texto_detalhado encontrado")
                time.sleep(2)
                texto_detalhado.click()
                time.sleep(1)
                break
            else:
                print("texto_detalhado não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de texto_detalhado")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de texto_detalhado: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'adicionar_cartoes'
    while True:
        try:
            adicionar_cartoes = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div/div[1]/button[3]'))
            )
            if adicionar_cartoes:
                print("adicionar_cartoes encontrado")
                time.sleep(2)
                adicionar_cartoes.click()
                time.sleep(1)
                adicionar_cartoes.click()
                break
            else:
                print("adicionar_cartoes não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de adicionar_cartoes")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de adicionar_cartoes: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'continuar_e_gerar'
    while True:
        try:
            continuar_e_gerar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div[2]'))
            )
            if continuar_e_gerar:
                print("continuar_e_gerar encontrado")
                time.sleep(2)
                continuar_e_gerar.click()
                time.sleep(1)
                break
            else:
                print("continuar_e_gerar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de continuar_e_gerar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de continuar_e_gerar: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'embaralhar'
    while True:
        try:
            embaralhar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/button[2]'))
            )
            if embaralhar:
                print("embaralhar encontrado")
                time.sleep(2)
                embaralhar.click()
                time.sleep(1)
                break
            else:
                print("embaralhar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de embaralhar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de embaralhar: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'gerar'
    while True:
        try:
            gerar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/button[1]'))
            )
            if gerar:
                print("gerar encontrado")
                time.sleep(2)
                gerar.click()
                time.sleep(1)
                break
            else:
                print("gerar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de gerar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de gerar: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'compartilhar'
    while True:
        try:
            compartilhar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/div[2]/span/button'))
            )
            if compartilhar:
                print("compartilhar encontrado")
                time.sleep(2)
                compartilhar.click()
                time.sleep(1)
                break
            else:
                print("compartilhar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de compartilhar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de compartilhar: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'exportar'
    while True:
        try:
            exportar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="chakra-modal--body-:r3d3:"]/div[1]/div[1]/ul/li[3]'))
            )
            if exportar:
                print("exportar encontrado")
                time.sleep(2)
                exportar.click()
                time.sleep(1)
                break
            else:
                print("exportar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de exportar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de exportar: {e}")
            time.sleep(1)

    # Verifica e interage com o botão de 'exportar_pdf'
    '''while True:
        try:
            exportar_pdf = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="chakra-modal--body-:r3d3:"]/div[2]/div[1]/button[1]'))
            )
            if exportar_pdf:
                print("exportar_pdf encontrado")
                time.sleep(2)
                exportar_pdf.click()
                time.sleep(1)
                break
            else:
                print("exportar_pdf não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de exportar_pdf")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de exportar_pdf: {e}")
            time.sleep(1)'''

    #
    while True:
        try:
            # Localiza o botão 'Exportar para PDF' e clica para iniciar o download
            exportar_botao = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-104fw47'))
            )
            if exportar_botao:
                print("exportar_botao encontrado")
                time.sleep(2)
                exportar_botao.click()
                time.sleep(10)
                break
            else:
                print("exportar_botao não encontrado")

            # Verifica se algum arquivo foi baixado na pasta
            arquivos_baixados = os.listdir(user_folder_downloads)
            if arquivos_baixados:
                print(f"Download concluído: {arquivos_baixados[0]}")
            else:
                print(f"Nenhum arquivo encontrado para o user_id {user_id}")

        except Exception as e:
            print(f"Erro ao baixar PDF: {e}")
