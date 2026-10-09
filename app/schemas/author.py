from pydantic import BaseModel, ConfigDict

class AuthorCreate(BaseModel):
    name: str

class AuthorRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)