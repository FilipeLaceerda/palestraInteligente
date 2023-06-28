import face_recognition
import cv2
import simpy
import glob
from fpdf import FPDF

TEMPO_DE_DETECCAO_DE_FACE_CONHECIDAS = 50
TEMPO_DE_RECONHECER_PESSOAS = 60
TEMPO_DE_GERAR_CERTIFICADO = 60
TEMPO_DE_ENVIAR_CERTIFICADO = 60
TEMPO_DESCONHECIDOS = 60

face_conhecidas = []
inscritos = []
pessoas_reconhecidas = []
destinatarios = []
certificados = []


# Carregar as imagens das faces conhecidas
def carregar_faces_conhecidas():
    faces_conhecidas_resultado = []
    inscritos_resultado = []
    imagens_faces = glob.glob("assets/FacesReconhecidas/*.jpg")
    for imagem_face in imagens_faces:
        face = face_recognition.load_image_file(imagem_face)
        encoding = face_recognition.face_encodings(face)[0]
        faces_conhecidas_resultado.append(encoding)
        nome_inscrito = imagem_face.split("/")[-1].split("\\")[-1].split(".")[0]
        inscritos_resultado.append(nome_inscrito)

        # Regras do email
        email = nome_inscrito.lower().replace(" ", "") + "@email.com"
        if nome_inscrito == "capitao":
            peso = 1
        elif nome_inscrito == "peralta":
            peso = 2
        else:
            peso = 0

        # Adicionar à lista de pessoas reconhecidas
        pessoas_reconhecidas.append((nome_inscrito, True, peso, email))

    return faces_conhecidas_resultado, inscritos_resultado

def reconhecer_pessoas(imagem, face_conhecidas, inscritos):
    global pessoas_reconhecidas
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(imagem_rgb)
    pessoas_reconhecidas_resultado = []

    for i, face in enumerate(faces):
        resultados = face_recognition.compare_faces(face_conhecidas, face)
        nome_reconhecido = 'Desconhecido'
        inscrito = False
        peso = 0  # Definir peso inicialmente como 0
        email = ''

        if True in resultados:
            indice = resultados.index(True)
            nome_reconhecido = inscritos[indice]
            email = pessoas_reconhecidas[indice][3]  # Obter o email da lista de pessoas reconhecidas
            peso = pessoas_reconhecidas[indice][2]  # Obter o peso da lista de pessoas reconhecidas
            inscrito = True

        pessoas_reconhecidas_resultado.append((nome_reconhecido, inscrito, peso, email))

        # Desenhar retângulos verdes e vermelhos
        (top, right, bottom, left) = face_recognition.face_locations(imagem_rgb)[i]
        cor_retangulo = (0, 255, 0)  # Verde

        if nome_reconhecido == 'Desconhecido' and not inscrito:
            cor_retangulo = (0, 0, 255)  # Vermelho

        cv2.rectangle(imagem, (left, top), (right, bottom), cor_retangulo, 2)

    # Exibir imagem com retângulos verdes e vermelhos
    cv2.imshow('Faces Reconhecidas', imagem)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    pessoas_reconhecidas = pessoas_reconhecidas_resultado
    return pessoas_reconhecidas


def gerador_reconhecer_pessoas(imagem, face_conhecidas, inscritos, ambiente_de_simulacao):
    reconhecer_pessoas(imagem, face_conhecidas, inscritos)
    yield ambiente_de_simulacao.timeout(TEMPO_DE_RECONHECER_PESSOAS)


def enviar_certificado(destinatario, certificado):
    print(f'{certificado}  "enviado para: "  {destinatario}')

def gerador_enviar_certificado(destinatario, certificado, ambiente_de_simulacao):
    enviar_certificado(destinatario, certificado)
    yield ambiente_de_simulacao.timeout(TEMPO_DE_ENVIAR_CERTIFICADO)

def gerar_certificado(pessoas_reconhecidas):
    global destinatarios, certificados
    destinatarios_resultado = []
    certificados_resultado = []
    for nome, inscrito, peso, email in pessoas_reconhecidas:
        if inscrito:
            certificado = f"certificado_{nome}.pdf"
            pdf = FPDF(orientation='P', unit='mm', format='A4')

            # Configuração do certificado
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)

            if peso == 0:
                pdf.cell(0, 10, "Certificado de Participação", ln=True, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=16)
                pdf.multi_cell(0, 10, f"Este certifica que {nome} participou da palestra.", align="C")
            elif peso == 1:
                pdf.cell(0, 10, "Certificado de Participação do palestrante", ln=True, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=16)
                pdf.multi_cell(0, 10, f"Este certifica que {nome} ministrou a palestra.", align="C")
            elif peso == 2:
                pdf.cell(0, 10, "Certificado de Participação do monitor da turma", ln=True, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=16)
                pdf.multi_cell(0, 10, f"Este certifica que {nome} monitorou a palestra.", align="C")

            pdf.output(certificado)
            destinatarios_resultado.append(email)
            certificados_resultado.append(certificado)
    destinatarios = destinatarios_resultado
    certificados = certificados_resultado
    return certificados, destinatarios

def gerador_gerar_certificado(pessoas_reconhecidas, ambiente_de_simulacao):
    gerar_certificado(pessoas_reconhecidas)
    yield ambiente_de_simulacao.timeout(TEMPO_DE_GERAR_CERTIFICADO)

# Função de simulação

# Função principal
def mensagem_desconhecidos_telao(pessoas_reconhecidas):
    desconhecidos = [pessoa for pessoa in pessoas_reconhecidas if pessoa[0] == 'Desconhecido' and not pessoa[1]]
    if desconhecidos:
        print(f'pessoas não inscritas na palestra, não perca a proxima se increva no site, palestra.com')

def gerador_mensagem_desconhecidos_telao(pessoas_reconhecidas, env):
    mensagem_desconhecidos_telao(pessoas_reconhecidas)
    yield env.timeout(TEMPO_DESCONHECIDOS)


def main():
    # Configuração do ambiente SimPy
    imagem = face_recognition.load_image_file("assets/brooklyn-nine-nine.jpg")
    env = simpy.Environment()

    face_conhecidas, inscritos = carregar_faces_conhecidas()

    # Reconhecer pessoas
    pessoas_reconhecidas = reconhecer_pessoas(imagem, face_conhecidas, inscritos)
    env.process(gerador_reconhecer_pessoas(imagem, face_conhecidas, inscritos, env))

    # Gerar certificados
    env.process(gerador_gerar_certificado(pessoas_reconhecidas, env))

    destinatarios, certificados = gerar_certificado(pessoas_reconhecidas)
    # Enviar certificados
    env.process(gerador_enviar_certificado(destinatarios, certificados, env))
    env.process(gerador_mensagem_desconhecidos_telao(pessoas_reconhecidas, env))

    # Iniciar a simulação
    env.run(until=1000)

# Execução do programa
if __name__ == "__main__":
    main()