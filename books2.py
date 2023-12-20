from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field #Base Modelhelps to do validations on the request body

app = FastAPI()

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id : Optional[int] = Field(title="ID is not required")
    title : str = Field(min_length=3)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=0, lt=6)
    published_date : int = Field(gt=0, lt=2022)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Ikigai",
                "author": "Francesc Miralles",
                "description": "The Japanese secret to a long and happy life",
                "rating": 4,
                "published_date": 2017
            }
        }


books = [
    Book(1, "Ikigai", "Francesc Miralles", "The Japanese secret to a long and happy life", 4, 2021),
    Book(2, "The Alchemist", "Paulo Coelho", "A quest for finding treasure", 5, 2022),
    Book(3, "Lord of the Rings", "J. R. R. Tolkien", "A hobbit's adventure", 5, 2022),
    Book(4, "Harry Potter", "J. K. Rowling", "A wizard's adventure", 5, 2023),
    Book(5, "The Da Vinci Code", "Dan Brown", "A quest for finding the Holy Grail", 4, 2023),
    Book(6, "Angels and Demons", "Dan Brown", "A quest for finding the Illuminati", 4, 2023)
]

@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/")
async def get_book_by_rating(rating : int = Query(gt=0, lt=6)): #Adding validation to query parameters
    solution = []
    for book in books:
        if book.rating == rating:
            solution.append(book)
    return solution

#Filter books by publish date
# @app.get("/books/{published_date}")
# async def get_books_by_publish_date(published_date : int = Path(gt=0, lt=2022)):
#     solution = []
#     for book in books :
#         if book.published_date == published_date:
#             solution.append(book)
#     return solution

@app.get("/books/{book_id}")
async def read_book(book_id : int = Path(gt=0)): #Way to validate path parameters
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
async def create_book(book_request : BookRequest): #book_request has a type of BookRequest, so whatever is in the body is named as book_request which essentially has a type BookRequest
    #model_dump() returns a dictionary of the model's fields and values
    new_book = Book(**book_request.model_dump()) #** is used to unpack the dictionary, it's used to convert the BookRequest object to a Book object
    books.append(find_book_id(new_book)) #First it'll assign the ID to book and then append it to books
    return books

@app.put("/books/{book_title}")
async def update_book_by_title(title:str, book_request : BookRequest):
    book_changed = False
    for book in books:
        if book.title == title:
            book_changed = True
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            return book
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id : int = Path(gt=0)):
    book_changed = False
    for i in range(len(books)):
        if books[i].id == book_id:
            del books[i]
            book_changed = True
            return {'message': 'Book deleted'}
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")    

def find_book_id(book : Book):
    if len(books) > 0:
        book.id = books[-1].id + 1 #grabs the last book in books list and adds 1 to its ID
    else:
        book.id = 1
    return book