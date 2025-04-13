from pydantic import BaseModel, Field


class Book(BaseModel):
    """
    Class to handle data validation from client
    """
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=50)
    year: int = Field(gt=1900, lt=2100)


class BookResponse(BaseModel):
    """
    Class to response a specific data structure
    """
    title: str
    author: str
