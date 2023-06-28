Feature: Enviar Certificado

  Scenario Outline: Enviar certificado para destinatário
    Given um destinatário
    And um certificado
    When a função enviar_certificado é chamada com o destinatário e o certificado
    Then o certificado é enviado para o destinatário

    Examples:
      | destinatario       | certificado       |
      | email1@example.com | certificado_1.pdf |
      | email2@example.com | certificado_2.pdf |
      | email3@example.com | certificado_3.pdf |
