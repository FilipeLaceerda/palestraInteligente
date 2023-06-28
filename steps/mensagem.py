import simpy
from behave import given, when, then
from main import mensagem_desconhecidos_telao

@given('um desconhecido')
def step_given_um_desconhecido(context):
    context.desconhecido = [('Desconhecido', False, 0, ''), ('peralta', True, 2, 'peralta@email.com'), ('Desconhecido', False, 0, ''), ('Desconhecido', False, 0, ''), ('capitao', True, 1, 'capitao@email.com'), ('scully', True, 0, 'scully@email.com'), ('capitao', True, 1, 'capitao@email.com'), ('hitchcock', True, 0, 'hitchcock@email.com')]

@when('a função messagem_desconhecidos_telao é chamada com pelo menos um desconhecido')
def step_when_a_funcao_mensagem_desconhecido_telao_e_chamada(context):
    context.env = simpy.Environment
    context.resultado = mensagem_desconhecidos_telao(context.desconhecido)

@then('a mensagem é exibida')
def step_then_a_mensagem_e_exibida(context):
    print(f'{context.resultado}')
