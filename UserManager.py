# Importações necessárias
import sqlite3  # Importa o módulo sqlite3 para trabalhar com o banco de dados SQLite
from Database import Database  # Importa a classe Database do arquivo Database.py
from ContactTreat import ContactTreat  # Importa a classe ContactTreat do arquivo ContactTreat.py


class UserManager:
    def __init__(self):
        # Inicializa o objeto de conexão com o banco de dados e cria as tabelas se ainda não existirem
        self.db = Database('library-portfolio.db')  # Cria uma instância da classe Database com o nome do banco de dados
        self.db.create_tables()  # Cria as tabelas necessárias no banco de dados se ainda não existirem

    # Método para salvar ou atualizar um usuário no banco de dados
    def save_user(self, user_dict):
        try:
            # Abre uma conexão com o banco de dados
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Valida o contato usando a classe ContactValidator
            if not ContactTreat.validate(user_dict['contact']):
                # Se o contato não for válido, aborta a operação
                return

            # Insere um novo usuário na tabela users
            self.db.cursor.execute(
                'INSERT INTO users (name, contact) VALUES (?, ?)',
                (user_dict['name'], user_dict['contact']))

            # Realiza o commit para confirmar as alterações no banco de dados
            self.db.connection.commit()
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar registrar usuário:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)
        finally:
            # Garante que a conexão seja fechada, mesmo se ocorrer uma exceção
            if self.db.connection:
                self.db.connection.close()

    # Método para consultar e exibir todos os usuários cadastrados
    def user_query(self):
        try:
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Executa a consulta SQL para recuperar todos os usuários
            self.db.cursor.execute('SELECT * FROM users')
            users = self.db.cursor.fetchall()

            # Verifica se existem usuários cadastrados
            if not users:
                print('Não existe usuários cadastrados.')
                input('Digite 0 para voltar ao menu inicial ')
            else:
                # Exibe os detalhes de cada usuário
                for user in users:
                    print(
                        f'ID: {user[0]}\n'
                        f'Nome: {user[1]}\n'
                        f'Contato: {user[2]}')
                input('Digite 0 para voltar ao menu inicial ')
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar consultar usuários:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)
