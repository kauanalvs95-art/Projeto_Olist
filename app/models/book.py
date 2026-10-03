from sqlalchemy import Column, Integer, String, ForeignKey, Table
from app.database import Base
from sqlalchemy.orm import relationship


book_author_association = Table(
        "relationships",
        Base.metadata,
        Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
        Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    )


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    edition = Column (String, index=True)
    publication_year = Column(Integer, index=True )

    authors = relationship("Author", secondary="relationships", back_populates="books")
    
