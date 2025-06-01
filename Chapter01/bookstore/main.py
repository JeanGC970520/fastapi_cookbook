from .router import router

import json

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse

app = FastAPI()

app.include_router(router)

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "The Grat Gatsby",
        "author": "F. Scott Fitzgerald",
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message" : "Oops! Something went wrong"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return PlainTextResponse(
        "This is a plain text response: " +
        f"\n{json.dumps(exc.errors(), indent=2)}",
        status_code= status.HTTP_400_BAD_REQUEST,
    )
# @app.get("/authors/{author_id}")
# async def read_author(author_id: int):
#     return {
#         "author_id" : author_id,
#         "name" : "Ernest Hemingway"
#     }

# @app.get("/books")
# async def read_books(year: int = None):
#     if year:
#         return {
#             "year" : year,
#             "books" : ["Book 1", "Book 2"]
#         }
#     return {"books": ["All books"]}
