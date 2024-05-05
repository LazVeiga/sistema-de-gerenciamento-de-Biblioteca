# Importações necessárias
import sqlite3
from Library import Library
from Database import Database
from UserManager import UserManager
from ContactTreat import ContactTreat
from os import system as sys
from time import sleep
from datetime import datetime, timedelta


# Função para limpar a tela do console
def clear():
    sys('cls')


# Função para limpar a tela do console após três segundos
def clearAfterThreeSeconds():
    sleep(3)
    clear()


# Função para exibir o menu principal
def mainMenu():
    print("\n===== Bem vindo! =====")
    print("1. Menu de usuários")
    print("2. Menu de biblioteca")
    print("3. Sair")


# Função para exibir o menu de usuários
def userMenu():
    print("\n===== Usuários =====")
    print("1. Cadastrar usuários")
    print("2. Consultar usuários cadastrados")
    print("3. Voltar")


# Função para exibir o menu da biblioteca
def libraryMenu():
    print("\n===== Biblioteca =====")
    print("1. Adicionar Livro")
    print("2. Listar Livros Disponíveis")
    print("3. Realizar Empréstimo")
    print("4. Devolver Livros")
    print("5. Consultar Livros")
    print("6. Voltar")


# Função principal
def main():
    try:
        # Instanciando objetos necessários
        library = Library()
        userManager = UserManager()
        database = Database('library-portfolio.db')

        while True:
            # Exibindo o menu principal e recebendo a opção do usuário
            mainMenu()
            option = int(input("Escolha uma opção: "))

            # Opção para o menu de usuários
            if option == 1:
                clear()
                userMenu()
                userOption = int(input("Escolha uma opção: "))

                # Opção para cadastrar usuários
                if userOption == 1:
                    clear()
                    name = input("Nome: ")
                    contact = input("Contato: ")
                    user = {
                        'name': name,
                        'contact': contact
                    }
                    # Validação do contato usando a classe ContactValidator
                    if not ContactTreat.validate(user['contact']):
                        print("Erro: O formato do contato é inválido.")
                        input('Digite 0 para voltar para o menu inicial ')
                    else:
                        userManager.save_user(user)
                        print('Usuário registrado com sucesso.')
                    clearAfterThreeSeconds()

                # Opção para consultar usuários cadastrados
                elif userOption == 2:
                    clear()
                    userManager.user_query()
                    clearAfterThreeSeconds()

                # Opção para voltar ao menu principal
                elif userOption == 3:
                    clear()
                    print('Voltando...')
                    clearAfterThreeSeconds()

                else:
                    print("Opção inválida. Tente novamente.")
                clear()

            # Opção para o menu da biblioteca
            elif option == 2:
                clear()
                libraryMenu()
                libraryOption = input("Escolha uma opção: ")

                # Opção para adicionar livro
                if libraryOption == '1':
                    clear()
                    title = input('Título do livro: ')
                    author = input('Autor do livro: ')
                    release_year = int(input('Ano de publicação: '))
                    copies_available = int(input('Copias disponíveis: '))
                    book = {
                        'title': title,
                        'author': author,
                        'release_year': release_year,
                        'copies_available': copies_available
                    }
                    library.save_book(book)
                    print('Livro registrado com sucesso.')
                    clearAfterThreeSeconds()

                # Opção para listar livros disponíveis
                elif libraryOption == '2':
                    clear()
                    library.getAvailableBooks()
                    loanOption = int(
                        input('0. Voltar ao menu inicial\n1. Fazer empréstimo de um livro\nEscolha sua opção: '))
                    if loanOption == 1:
                        clear()
                        user_id = input('Insira o ID do usuário que vai alugar: ')
                        if not user_id:
                            print('Usuário não encontrado.')
                            break

                        book_id = input('Insira o ID do livro que será alugado: ')
                        if not book_id:
                            print('Livro não encontrado.')
                            break

                        loan = {
                            'user_id': user_id,
                            'book_id': book_id
                        }
                        library.borrow_book(loan)
                        clearAfterThreeSeconds()
                    elif loanOption == 0:
                        clear()
                        print('Voltando...')
                        clearAfterThreeSeconds()
                    else:
                        print('Não há livros disponíveis.')
                        loanOption = int(input('Digite 0 para voltar para o menu inicial '))
                        if loanOption == 0:
                            clear()
                            print('Voltando...')
                            clearAfterThreeSeconds()

                # Opção para realizar empréstimo
                elif libraryOption == '3':
                    clear()
                    library.getAvailableBooks()
                    user_id = input('Insira o ID do usuário que vai alugar: ')
                    book_id = input('Insira o ID do livro que será alugado: ')
                    loan = {
                        'user_id': user_id,
                        'book_id': book_id
                    }
                    library.borrow_book(loan)
                    clearAfterThreeSeconds()

                # Opção para devolver livros
                elif libraryOption == '4':
                    clear()
                    loan_id = int(input('Insira o ID do empréstimo para devolver: '))
                    library.return_book(loan_id)
                    clearAfterThreeSeconds()

                # Opção para consultar livros
                elif libraryOption == '5':
                    clear()
                    query_type = int(
                        input("Tipos de consulta:\n1. Titulo\n2. Autor\n3. Ano\n4. Disponíveis\n5. Emprestados\nEscolha uma opção: "))
                    if query_type == 4:
                        library.getAvailableBooks()
                    elif query_type == 5:
                        library.getBorrowedBooks()
                    else:
                        query_term = input("Termo de busca: ")
                        clear()
                        library.book_queries(query_type, query_term)
                    int(input('Digite 0 para voltar para o menu inicial '))
                    clearAfterThreeSeconds()

                # Opção para voltar ao menu principal
                elif libraryOption == '6':
                    clear()
                    print('Voltando...')
                    clearAfterThreeSeconds()

                else:
                    clear()
                    print("Opção inválida. Tente novamente.")
                    clearAfterThreeSeconds()

            # Opção para sair do programa
            elif option == 3:
                clear()
                database.close_connection()
                print("Saindo...")
                clearAfterThreeSeconds()
                break

            else:
                clear()
                print("Opção inválida. Tente novamente.")
                clearAfterThreeSeconds()
    except sqlite3.Error as e:
        print("Ocorreu um erro ao tentar com o console de operações:", e)
    except Exception as ex:
        print("Ocorreu um erro não esperado:", ex)


# Executando a função principal
if __name__ == "__main__":
    main()
