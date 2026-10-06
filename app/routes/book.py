from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/books/{book_id}", response_model=BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/books/", response_model=list[BookRead])
def read_books(
    name: str = None,
    edition: str = None,
    publication_year: int = None,
    authors_name: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
    ):
    db_books = db.query(Book)
    if name:
        db_books = db_books.filter(Book.name.ilike(f"%{name}%"))
    if edition:
        db_books = db_books.filter(Book.edition.ilike(f"%{edition}%"))
    if publication_year:
        db_books = db_books.filter(Book.publication_year == publication_year)
    if authors_name:
        db_books = db_books.filter(Book.authors.any(Author.name.ilike(f"%{authors_name}%")))
    return db_books.offset(skip).limit(limit).all()