Feature: Gerar Certificado

  Scenario Outline: Gerar certificado para pessoas reconhecidas
    Given uma lista de pessoas reconhecidas
    When a função gerar_certificado é chamada com a lista de pessoas reconhecidas
    Then os certificados e destinatários são gerados corretamente

    Examples:
      | pessoas_reconhecidas                    |
      | Nome1, Inscrito1, 0, email1@example.com |
      | Nome2, Inscrito2, 1, email2@example.com |
      | Nome3, Inscrito3, 2, email3@example.com |
      | Nome4, Inscrito4, 0, email4@example.com |
      | Nome5, Inscrito5, 1, email5@example.com |
