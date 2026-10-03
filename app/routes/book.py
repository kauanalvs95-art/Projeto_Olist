from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookRead
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/books/", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    authors_wanted = db.query(Author).filter(Author.id.in_(book.authors_ids)).all()
    db_book =Book(
        name=book.name,
        edition=book.edition,
        publication_year=book.publication_year,
        authors=authors_wanted
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book