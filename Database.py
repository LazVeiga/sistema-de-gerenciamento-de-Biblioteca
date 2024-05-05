# Importação necessária
import sqlite3


class Database:
    def __init__(self, db_name):
        # Inicializa o objeto Database com o nome do banco de dados
        self.db_name = db_name
        # Conecta ao banco de dados
        self.connection = sqlite3.connect(self.db_name)
        # Cria um cursor para executar comandos SQL
        self.cursor = self.connection.cursor()

    def create_tables(self):
        try:
            # Cria a tabela de usuários se ela não existir
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    contact TEXT UNIQUE
                )
            ''')

            # Cria a tabela de livros se ela não existir
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    release_year INTEGER,
                    copies_available INTEGER,
                    borrowed BOOL DEFAULT false
                )
            ''')

            # Cria a tabela de empréstimos se ela não existir
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    book_id INTEGER,
                    date_issued DATE,
                    date_due DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                )
            ''')

            # Salva as alterações no banco de dados
            self.connection.commit()
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar salvar as tabelas:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)

    def close_connection(self):
        # Método para fechar a conexão com o banco de dados
        self.connection.close()


# Cria uma instância da classe Database com o nome do banco de dados
database = Database('library-portfolio.db')
# Cria as tabelas necessárias no banco de dados
database.create_tables()
# Fecha a conexão com o banco de dados
database.close_connection()
