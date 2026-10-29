from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import schemas

import models
from database import engine, get_db


# Create the database tables when the app starts.
# This uses the Course model from models.py.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message":"Books API is running"}

@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    # response_model tells FastAPI to return a list of CourseResponse objects.
    # Read all courses from the database.
    books = db.query(models.Book).all()
    return books

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # Find one course by primary key.
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found psaxe allo")

    return book



@app.post("/books", response_model=schemas.BookResponse, status_code=201)
def create_book(book_data: schemas.BookCreate, db: Session = Depends(get_db)):
    # course_data has already been checked by Pydantic.
    # We can use dot notation because course_data is a CourseCreate object.
    book = models.Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year
    )

    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book code already exists")
