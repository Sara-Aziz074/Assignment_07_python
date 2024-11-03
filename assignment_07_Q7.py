#Design a Library Management System using Object-Oriented Programming (OOP)
#  concepts and Python's typing features. The system should support basic CRUD
#  operations (Create, Read, Update, Delete) for books, manage different types of
#  users (Librarians and Members), and handle book borrowing transactions with file-based 
# data persistence. Appropriate error handling for file operations is required.


import json
import os
from typing import List, Dict, Optional, Union

# Book Class
class Book:
    def __init__(self, book_id: int, title: str, author: str, isbn: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def update_info(self, title: Optional[str] = None, author: Optional[str] = None, isbn: Optional[str] = None):
        if title: self.title = title
        if author: self.author = author
        if isbn: self.isbn = isbn

    def display(self):
        status = "Available" if not self.is_borrowed else "Borrowed"
        return f"{self.book_id}: {self.title} by {self.author} - {status}"

# User Classes
class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

class Librarian(User):
    pass

class Member(User):
    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name)
        self.borrowed_books: List[int] = []

# Library Class
class Library:
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.users: Dict[int, Union[Librarian, Member]] = {}
        self.load_data()

    # CRUD for Books
    def add_book(self, book: Book):
        if book.book_id in self.books:
            print("Book already exists!")
        else:
            self.books[book.book_id] = book
            self.save_data()

    def update_book(self, book_id: int, title: Optional[str] = None, author: Optional[str] = None, isbn: Optional[str] = None):
        if book_id in self.books:
            self.books[book_id].update_info(title, author, isbn)
            self.save_data()
        else:
            print("Book not found.")

    def delete_book(self, book_id: int):
        if book_id in self.books:
            del self.books[book_id]
            self.save_data()
        else:
            print("Book not found.")

    def display_books(self):
        for book in self.books.values():
            print(book.display())

    # User Registration
    def add_user(self, user: Union[Librarian, Member]):
        if user.user_id in self.users:
            print("User already exists!")
        else:
            self.users[user.user_id] = user
            self.save_data()

    # Borrow and Return
    def borrow_book(self, book_id: int, member_id: int):
        if book_id in self.books and member_id in self.users:
            book = self.books[book_id]
            member = self.users[member_id]
            if isinstance(member, Member) and not book.is_borrowed:
                book.is_borrowed = True
                member.borrowed_books.append(book_id)
                self.save_data()
                print(f"{member.name} borrowed '{book.title}'.")
            else:
                print("Book is not available or user is not a member.")
        else:
            print("Invalid book or user ID.")

    def return_book(self, book_id: int, member_id: int):
        if book_id in self.books and member_id in self.users:
            book = self.books[book_id]
            member = self.users[member_id]
            if isinstance(member, Member) and book_id in member.borrowed_books:
                book.is_borrowed = False
                member.borrowed_books.remove(book_id)
                self.save_data()
                print(f"{member.name} returned '{book.title}'.")
            else:
                print("Book was not borrowed by this member.")
        else:
            print("Invalid book or user ID.")

    # Data Persistence
    def save_data(self):
        try:
            with open("library_data.json", "w") as file:
                data = {
                    "books": {bid: vars(book) for bid, book in self.books.items()},
                    "users": {uid: {"id": user.user_id, "name": user.name, "type": user.__class__.__name__} for uid, user in self.users.items()}
                }
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if os.path.exists("library_data.json"):
            try:
                with open("library_data.json", "r") as file:
                    data = json.load(file)
                    for bid, book_data in data.get("books", {}).items():
                        book = Book(book_data['book_id'], book_data['title'], book_data['author'], book_data['isbn'])
                        book.is_borrowed = book_data['is_borrowed']
                        self.books[bid] = book
                    for uid, user_data in data.get("users", {}).items():
                        if user_data['type'] == "Librarian":
                            self.users[uid] = Librarian(user_data['id'], user_data['name'])
                        elif user_data['type'] == "Member":
                            self.users[uid] = Member(user_data['id'], user_data['name'])
            except Exception as e:
                print(f"Error loading data: {e}")

# Usage Example
def main():
    library = Library()
    
    # Adding Users
    librarian = Librarian(1, "Alice")
    member = Member(2, "Bob")
    library.add_user(librarian)
    library.add_user(member)
    
    # Adding Books
    book1 = Book(101, "The Great Gatsby", "F. Scott Fitzgerald", "123456789")
    library.add_book(book1)
    book2 = Book(102, "1984", "George Orwell", "987654321")
    library.add_book(book2)

    # Borrowing and Returning
    library.borrow_book(101, 2)  # Bob borrows "The Great Gatsby"
    library.return_book(101, 2)  # Bob returns "The Great Gatsby"

    # Display All Books
    print("\nCurrent Books in Library:")
    library.display_books()

main()
