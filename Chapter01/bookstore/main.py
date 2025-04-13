from fastapi import FastAPI

app = FastAPI()


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "The Grat Gatsby",
        "author": "F. Scott Fitzgerald",
    }
