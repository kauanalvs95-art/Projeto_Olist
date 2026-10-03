from fastapi import FastAPI
from app.routes import author
from app.routes import book

app = FastAPI()
app.include_router(author.router)
app.include_router(book.router)