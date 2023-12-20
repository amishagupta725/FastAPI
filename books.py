from fastapi import Body, FastAPI

app = FastAPI()

books = [
    {'name': 'Harry Potter', 'author': 'J. K. Rowling', 'category': 'fantasy'},
    {'name': 'Lord of the Rings', 'author': 'J. R. R. Tolkien', 'category': 'fantasy'},
    {'name': 'The Alchemist', 'author': 'Paulo Coelho','category': 'adventure'},
    {'name': 'The Da Vinci Code', 'author': 'Dan Brown', 'category': 'thriller'},
    {'name' : 'Angels and Demons', 'author': 'Dan Brown', 'category': 'thriller'},    
    {'name': 'Ikigai', 'author': 'Francesc Miralles' ,'category': 'self-help'},     
]

#GET REQUEST
@app.get("/books")
async def read_all_books():
    return books

#PATH PARAMETER
@app.get("/books/{book_title}")
async def get_book_by_title(book_title : str):
    for book in books:
        if book.get('name').casefold() == book_title.casefold():
            return book
    return {'message': 'Book not found'}

#QUERY PARAMETER
#Filter by category : localhost:8080/books/?category=thriller
@app.get("/books/")
async def get_books_by_query_param(category : str):
    solution = []
    for book in books :
        if book.get("category").casefold() == category.casefold():
            solution.append(book)
    return solution

#Filter by category as query parameter and author as path parameter : localhost:8080/books/{author}?category=thriller
@app.get("/books/{author}/")
async def get_books_by_author_and_category(author : str, category : str):
    solution = []
    for book in books :
        if book.get("author").casefold() == author.casefold() and book.get("category").casefold() == category.casefold():
            solution.append(book)
    return solution

#POST REQUEST
@app.post("/books")
async def create_book(new_book=Body()):
    books.append(new_book)
    return books

#PUT REQUEST  
@app.put("/books")
async def edit_book_by_title(book_to_edit=Body()):
    for book in books :
        if book.get("name").casefold() == book_to_edit.get("name").casefold():
            book = book_to_edit
            return book
    return {'message': 'Book not found'}

#DELETE REQUEST
@app.delete("/books/{book_title}")
async def delete_book_by_title(book_title : str):
    for book in books :
        if book.get("name").casefold() == book_title.casefold():
            books.remove(book)
            return books
    return {'message': 'Book not found'}

#ASSIGNMENT : fetch all books from a specific author
@app.get("/books/author/{author}")
async def get_books_by_author(author: str):
    solution = []
    for book in books :
        if book.get("author").casefold() == author.casefold():
            solution.append(book)
    return solution