# Importações necessárias
import sqlite3  # Importa o módulo sqlite3 para trabalhar com o banco de dados SQLite
from datetime import datetime, timedelta  # Importa as classes datetime e timedelta do módulo datetime

from Database import Database  # Importa a classe Database do arquivo Database.py


class Library:
    def __init__(self):
        # Inicializa a conexão com o banco de dados e cria as tabelas se ainda não existirem
        self.db = Database('library-portfolio.db')  # Cria uma instância da classe Database com o nome do banco de dados
        self.db.create_tables()  # Cria as tabelas necessárias no banco de dados se ainda não existirem

    def save_book(self, book_dict):
        try:
            # Abre a conexão com o banco de dados
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Insere um novo livro na tabela
            self.db.cursor.execute(
                'INSERT INTO books (title, author, release_year, copies_available) VALUES (?, ?, ?, ?)',
                (book_dict['title'], book_dict['author'], book_dict['release_year'], book_dict['copies_available'])
            )

            # Salva no banco de dados
            self.db.connection.commit()
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar registrar livro:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)
        finally:
            # Fecha a conexão com o banco de dados
            if self.db.connection:
                self.db.connection.close()

    def book_queries(self, query_type, query_term):
        try:
            query = None

            # Define a consulta com base no tipo de consulta fornecido
            if query_type == 1:
                query = 'SELECT * FROM books WHERE title LIKE ?'
            elif query_type == 2:
                query = 'SELECT * FROM books WHERE author LIKE ?'
            elif query_type == 3:
                query = 'SELECT * FROM books WHERE release_year LIKE ?'

            # Verifica se a consulta é válida
            if query is None:
                print("Tipo de consulta inválido.")
                return

            # Executa a consulta e recupera os resultados
            self.db.cursor.execute(query, ('%' + query_term + '%',))
            books = self.db.cursor.fetchall()
            if not books:
                print("Não tem livros.")

            for book in books:
                print(
                    f'ID: {book[0]}\n'
                    f'Título: {book[1]}\n'
                    f'Autor: {book[2]}\n'
                    f'Ano de Lançamento: {book[3]}\n'
                    f'Cópias Disponíveis: {book[4]}\n')
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar fazer consultas:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)

    def getAvailableBooks(self):
        try:
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Recupera os livros disponíveis na biblioteca
            self.db.cursor.execute('SELECT * FROM books WHERE copies_available > 0')
            available_books = self.db.cursor.fetchall()
            if not available_books:
                print("Não tem livros disponíveis.")

            for book in available_books:
                # Mostra os livros disponíveis
                print('Livros disponíveis:')
                print(
                    f'ID: {book[0]}\n'
                    f'Título: {book[1]}\n'
                    f'Autor: {book[2]}\n'
                    f'Ano de Lançamento: {book[3]}\n'
                    f'Cópias Disponíveis: {book[4]}\n')
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar procurar livros disponíveis:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)

    def getBorrowedBooks(self):
        try:
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Consulta para recuperar informações dos empréstimos e dos livros associados
            self.db.cursor.execute(
                'SELECT loans.id, loans.user_id, loans.date_issued, loans.date_due, books.title, books.author '
                'FROM loans '
                'INNER JOIN books ON loans.book_id = books.id '
                'WHERE books.borrowed = 1'
            )
            borrowed_books = self.db.cursor.fetchall()
            if not borrowed_books:
                print("Não há empréstimos.")

            for loan in borrowed_books:
                print('Empréstimos:')
                print(
                    f'ID do Empréstimo: {loan[0]}\n'
                    f'ID do Usuário: {loan[1]}\n'
                    f'Data de Emissão: {loan[2]}\n'
                    f'Data de Devolução: {loan[3]}\n'
                    f'Título do Livro: {loan[4]}\n'
                    f'Autor do Livro: {loan[5]}\n'
                )
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar encontrar empréstimos:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)

    def borrow_book(self, loan_dict):
        try:
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Consulta o empréstimo correspondente ao ID fornecido
            self.db.cursor.execute('SELECT * FROM books WHERE id = ?', (loan_dict['book_id'],))
            book = self.db.cursor.fetchone()
            if not book:
                print('Nenhum livro com esse ID foi encontrado.')
                return

            # Verifica livros disponíveis para empréstimo
            self.db.cursor.execute('SELECT * FROM books WHERE copies_available > 0')
            available = self.db.cursor.fetchall()

            if available:
                # Obtém a data atual
                today_date = datetime.today().date()

                # Calcula a data de devolução (7 dias a partir da data atual)
                due_date = today_date + timedelta(days=7)

                # Insere um novo registro de empréstimo na tabela loans
                self.db.cursor.execute(
                    'INSERT INTO loans (user_id, book_id, date_issued, date_due) VALUES (?, ?, ?, ?)',
                    (loan_dict['user_id'], loan_dict['book_id'], today_date, due_date)
                )

                # Atualiza o status do livro (cópias disponíveis e status de empréstimo)
                self.db.cursor.execute(
                    'UPDATE books SET copies_available = copies_available - 1, borrowed = 1 WHERE id = ?',
                    (loan_dict['book_id'],)
                )

                # Confirma as alterações no banco de dados
                self.db.connection.commit()

                print(f'Livro alugado com sucesso, data de devolução: {due_date}')
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar fazer o empréstimo:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)

    def return_book(self, loan_id):
        try:
            self.db.connection = sqlite3.connect(self.db.db_name)
            self.db.cursor = self.db.connection.cursor()

            # Consulta o empréstimo correspondente ao ID fornecido
            self.db.cursor.execute('SELECT * FROM loans WHERE id = ?', (loan_id,))
            loan = self.db.cursor.fetchone()

            # Verifica se o empréstimo foi encontrado
            if loan is None:
                print("Empréstimo não encontrado.")
                return

            # Remove o registro de empréstimo da tabela loans
            self.db.cursor.execute('DELETE FROM loans WHERE id = ?', (loan_id,))
            self.db.connection.commit()

            # Verifica se há outros empréstimos pendentes para o livro devolvido
            self.db.cursor.execute('SELECT * FROM loans WHERE book_id = ?', (loan[2],))
            remaining_loans = self.db.cursor.fetchall()

            # Se não houver mais empréstimos pendentes, atualiza o status do livro
            if not remaining_loans:
                self.db.cursor.execute('UPDATE books SET borrowed = 0 WHERE id = ?', (loan[2],))
                self.db.connection.commit()

            # Incrementa o número de cópias disponíveis do livro devolvido
            self.db.cursor.execute('UPDATE books SET copies_available = copies_available + 1 WHERE id = ?', (loan[2],))
            self.db.connection.commit()

            print("Livro devolvido com sucesso.")
        except sqlite3.Error as e:
            print("Ocorreu um erro ao tentar fazer a devolução:", e)
        except Exception as ex:
            print("Ocorreu um erro não esperado:", ex)
