class ContactTreat:
    @staticmethod
    def validate(contact):
        try:
            # Verifica se o comprimento do contato está dentro de limites aceitáveis
            if len(contact) < 9 or len(contact) > 15:
                # Retorna False se estiver fora dos limites
                return False

            # Retorna True se estiver dentro dos limites
            return True
        except Exception as ex:
            # Captura e imprime qualquer exceção inesperada que ocorra durante a validação do contato
            print("Ocorreu um erro não esperado:", ex)
