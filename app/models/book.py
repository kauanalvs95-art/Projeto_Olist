from sqlalchemy import Column, Integer, String
from .database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    book = Column(String, index=True)
    
