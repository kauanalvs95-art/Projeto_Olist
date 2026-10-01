from pydantic import BaseModel, ConfigDict
from .author import AuthorRead

class BookCreate(BaseModel):
    name: str
    edition: str
    publication_year: int
    authors_ids: list[int]

class BookRead(BaseModel):
    id: int
    name: str
    edition: str
    publication_year: int
    authors: list[AuthorRead] = []

    model_config = ConfigDict(from_attributes=True)