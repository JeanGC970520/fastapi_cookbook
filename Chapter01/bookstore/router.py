from fastapi import APIRouter

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