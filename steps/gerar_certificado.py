from behave import given, when, then
from main import gerar_certificado

@given('uma lista de pessoas reconhecidas')
def step_given_lista_pessoas_reconhecidas(context):
    context.pessoas_reconhecidas = [
        ("Nome1", True, 0, "email1@example.com"),
        ("Nome2", True, 1, "email2@example.com"),
        ("Nome3", True, 2, "email3@example.com"),
        ("Nome4", True, 0, "email4@example.com"),
        ("Nome5", True, 1, "email5@example.com")
    ]

@when('a função gerar_certificado é chamada com a lista de pessoas reconhecidas')
def step_when_gerar_certificado_chamada(context):
    context.certificados, context.destinatarios = gerar_certificado(context.pessoas_reconhecidas)

@then('os certificados e destinatários são gerados corretamente')
def step_then_certificados_destinatarios_gerados_corretamente(context):
    assert len(context.certificados) == len(context.pessoas_reconhecidas)
    assert len(context.destinatarios) == len(context.pessoas_reconhecidas)
    # Outras asserções e verificações podem ser adicionadas aqui, dependendo dos critérios de sucesso do teste
