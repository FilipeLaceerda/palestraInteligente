Feature: Reconhecer pessoas

  Scenario: Reconhecimento de pessoas em uma imagem
    Given uma imagem
    And faces conhecidas e inscritos
    When a função reconhecer_pessoas é chamada com a imagem, faces conhecidas e inscritos
    Then as pessoas reconhecidas são retornadas corretamente
