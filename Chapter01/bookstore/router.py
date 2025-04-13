from models import Book, BookResponse

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/authors/{author_id}")
async def read_author(author_id: int):
    return {
        "author_id" : author_id,
        "name" : "Ernest Hemingway"
    }

@router.get("/books")
async def read_books(year: int = None):
    if year:
        return {
            "year" : year,
            "books" : ["Book 1", "Book 2"] 
        }
    return {"books": ["All books"]}

@router.post("/book")
async def create_book(book: Book):
    return book

@router.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {
            "id" : 1,
            "title" : "1984",
            "author" : "George Orwell",
        },
        {
            "id" : 1,
            "title" : "The Great Gatsby",
            "author" : "F. Scott Fitzgerald",
        },
    ]

@router.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)