Feature: Mensagem desconhecidos

  Scenario: Exibir mensagem para desconhecidos
    Given um desconhecido
    When a função messagem_desconhecidos_telao é chamada com pelo menos um desconhecido
    Then a mensagem é exibida
