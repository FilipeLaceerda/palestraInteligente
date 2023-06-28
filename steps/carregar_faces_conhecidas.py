from behave import given, when, then
from main import carregar_faces_conhecidas

@given('uma pasta com imagens de faces conhecidas')
def step_given_uma_pasta_com_imagens_de_faces_conhecidas(context):
    context.faces_conhecidas, context.inscritos = carregar_faces_conhecidas()

@then('as faces conhecidas e os inscritos são carregados corretamente')
def step_then_as_faces_conhecidas_e_os_inscritos_sao_carregados_corretamente(context):
    assert len(context.faces_conhecidas) > 0
    assert len(context.inscritos) > 0
