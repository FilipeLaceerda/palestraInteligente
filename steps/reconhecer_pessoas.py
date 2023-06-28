import cv2
import face_recognition
from behave import given, when, then
from main import reconhecer_pessoas, carregar_faces_conhecidas


@given('uma imagem')
def step_given_uma_imagem(context):
    # Carregue a imagem para teste
    context.imagem = cv2.imread(r'C:\Users\lipse\palestraInteligente\assets\brooklyn-nine-nine.jpg')


@given('faces conhecidas e inscritos')
def step_given_faces_conhecidas(context):
    # Crie uma lista de faces conhecidas (encodings)
    context.face_conhecidas, context.inscritos = carregar_faces_conhecidas()

@when('a função reconhecer_pessoas é chamada com a imagem, faces conhecidas e inscritos')
def step_when_funcao_reconhecer_pessoas_e_chamada(context):
    # Chame a função reconhecer_pessoas com os parâmetros fornecidos
    context.resultado = reconhecer_pessoas(context.imagem, context.face_conhecidas, context.inscritos)

@then('as pessoas reconhecidas são retornadas corretamente')
def step_then_pessoas_reconhecidas_retornadas_corretamente(context):
    assert context.resultado == [('Desconhecido', False, 0, ''), ('peralta', True, 2, 'peralta@email.com'), ('Desconhecido', False, 0, ''), ('Desconhecido', False, 0, ''), ('capitao', True, 1, 'capitao@email.com'), ('scully', True, 0, 'scully@email.com'), ('capitao', True, 1, 'capitao@email.com'), ('hitchcock', True, 0, 'hitchcock@email.com')]

