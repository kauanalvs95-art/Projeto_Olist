from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    books = relationship("Book", secondary="relationships", back_populates="authors")
