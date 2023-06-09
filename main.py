import face_recognition
import cv2
import simpy
import glob
from fpdf import FPDF


# Carregar as imagens das faces conhecidas
def carregar_faces_conhecidas():
    faces_conhecidas = []
    inscritos = []
    imagens_faces = glob.glob("assets/FacesReconhecidas/*.jpg")
    for imagem_face in imagens_faces:
        face = face_recognition.load_image_file(imagem_face)
        encoding = face_recognition.face_encodings(face)[0]
        faces_conhecidas.append(encoding)
        nome_inscrito = imagem_face.split("/")[-1].split("\\")[-1].split(".")[0]
        inscritos.append(nome_inscrito)
    return faces_conhecidas, inscritos

# Função para reconhecimento facial
def reconhecer_pessoas(imagem, faces_conhecidas, inscritos):
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(imagem_rgb)
    pessoas_reconhecidas = []

    for i, face in enumerate(faces):
        resultados = face_recognition.compare_faces(faces_conhecidas, face)
        nome_reconhecido = 'Desconhecido'
        inscrito = False
        peso = 0  # Definir peso inicialmente como 0
        email = ''

        if True in resultados:
            indice = resultados.index(True)
            nome_reconhecido = inscritos[indice]
            email = nome_reconhecido.lower().replace(" ", "") + "@email.com"
            if nome_reconhecido == "capitao":
                peso = 1
            elif nome_reconhecido == "peralta":
                peso = 2
            inscrito = True

        pessoas_reconhecidas.append((nome_reconhecido, inscrito, peso, email))

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

    return pessoas_reconhecidas

def enviar_certificado(destinatario, certificado):
    print(f'{certificado}  "enviado para: "  {destinatario}')

def gerar_certificado(resultados):
    certificados = []
    for nome, inscrito, peso, email in resultados:
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
            enviar_certificado(email, certificado)
            certificados.append(certificado)

    return certificados

# Função de simulação
def simulacao(env):
        # Carregar imagem da câmera ou de um arquivo
        faces_conhecidas, inscritos = carregar_faces_conhecidas()

        # Chamada da função reconhecer_pessoas()
        imagem = face_recognition.load_image_file("assets/brooklyn-nine-nine.jpg")
        resultados = reconhecer_pessoas(imagem, faces_conhecidas, inscritos)
        gerar_certificado(resultados)


        yield env.timeout(1)
# Função principal
def main():
    # Configuração do ambiente SimPy
    env = simpy.Environment()

    # Executar a simulação
    env.process(simulacao(env))

    # Iniciar a simulação
    env.run()

# Execução do programa
if __name__ == "__main__":
    main()
