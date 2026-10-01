from pydantic import BaseModel

class AuthorCreate(BaseModel):
    name: str

class AuthorRead(BaseModel):
    id: int
    name: str