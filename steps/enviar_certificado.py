from behave import given, when, then
from main import enviar_certificado


@given('um destinatário')
def step_given_destinatario(context):
    context.destinatario = [
        ("destinatario1"),
        ("destinatario2"),
        ("destinatario3")]

@given('um certificado')
def step_given_certificado(context):
    context.certificado = [
        ("certificado1"),
        ("certificado2"),
        ("certificado3")
    ]

@when('a função enviar_certificado é chamada com o destinatário e o certificado')
def step_when_enviar_certificado_chamada(context):
    enviar_certificado(context.destinatario, context.certificado)

@then('o certificado é enviado para o destinatário')
def step_then_certificado_enviado(context):
    # Implemente a verificação ou ação necessária aqui
    print(f'O certificado {context.certificado} foi enviado para {context.destinatario}')
