from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/authors/{author_id}", response_model=AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.get("/authors/", response_model=list[AuthorRead])
def read_authors(author_name: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_authors = db.query(Author)
    if author_name:
        db_authors = db_authors.filter(Author.name.ilike(f"%{author_name}%"))
    return db_authors.offset(skip).limit(limit).all()

@router.delete('/authors/{author_id}')
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"detail": "Author deleted successfully"}

@router.put("/authors/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author.name = author.name
    db.commit()
    db.refresh(db_author)
    return db_author