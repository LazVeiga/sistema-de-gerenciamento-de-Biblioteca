class Book:
    # Inicializa um objeto Book com os atributos id, title, author, release_year, copies_available e borrowed
    def __init__(self, id, title, author, release_year, copies_available, borrowed):
        self.id = id
        self.title = title
        self.author = author
        self.release_year = release_year
        self.copies_available = copies_available
        self.borrowed = borrowed
