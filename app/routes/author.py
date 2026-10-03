from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorRead
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/authors/", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
