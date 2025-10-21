

from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI(title="Library Books Catalog")

books = []
next_id = 1

# Create
@app.post("/books/")
def add_book(title: str, author: str, genre: str, publicationyear: int, availability: bool):
    global next_id
    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "genre": genre,
        "publicationyear": publicationyear,
        "availability": availability,
    }
    books.append(book)
    next_id += 1
    return {"message": f"Book '{title}' added successfully!", "book": book}


# Read all books
@app.get("/books/")
def view_all_books():
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books


# Read single book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


# Update
@app.put("/books/{book_id}")
def update_book(book_id: int,
                title: Optional[str] = None,
                author: Optional[str] = None,
                genre: Optional[str] = None,
                publicationyear: Optional[int] = None,
                availability: Optional[bool] = None):
    for b in books:
        if b["id"] == book_id:
            if title: b["title"] = title
            if author: b["author"] = author
            if genre: b["genre"] = genre
            if publicationyear: b["publicationyear"] = publicationyear
            if availability is not None: b["availability"] = availability
            return {"message": "Book updated successfully.", "book": b}
    raise HTTPException(status_code=404, detail="Book not found")


# Delete
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            books.remove(b)
            return {"message": "Book deleted successfully.", "book": b}
    raise HTTPException(status_code=404, detail="Book not found")


# Search
@app.get("/books/search/")
def search_books(keyword: str):
    results = [b for b in books if keyword.lower() in b["title"].lower() or keyword.lower() in b["author"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No matching books found")
    return results


