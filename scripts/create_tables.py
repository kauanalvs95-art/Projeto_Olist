from app.database import Base, engine
from app.models.book import Book
from app.models.author import Author

Base.metadata.create_all(bind=engine)