"""
Book management module for Library Manager
"""
from backend_utils import SEPARATOR


class Book:
    """Represents a book in the library"""
    
    def __init__(self, db, book_id=None, book_name=None, author=None, genre=None, price=None, count=None):
        """Initialize a book object"""
        self.db = db
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.genre = genre
        self.price = price
        self.count = count
    
    def save(self):
        """Add a new book to the database"""
        query = "insert into book(book_id, book_name, author, genre, price, count) values(%s, %s, %s, %s, %s, %s);"
        values = (self.book_id, self.book_name, self.author, self.genre, self.price, self.count)
        self.db.execute(query, values)
        self.db.commit()
    
    def delete(self):
        """Delete a book from the database"""
        query = "delete from book where book_id = %s;"
        self.db.execute(query, (self.book_id,))
        self.db.commit()
    
    def update_count(self, delta):
        """Update the count of available books"""
        query = "update book set count = count + %s where book_id = %s;"
        self.db.execute(query, (delta, self.book_id))
        self.db.commit()
    
    @staticmethod
    def get_all_available(db):
        """Get all books with available copies"""
        query = "select * from book where count > 0;"
        db.execute(query)
        return db.fetchall()
    
    @staticmethod
    def get_all(db):
        """Get all books from the database"""
        query = "select * from book"
        db.execute(query)
        return db.fetchall()


class BookManager:
    """Manages book operations"""
    
    def __init__(self, db):
        """Initialize BookManager with database connection"""
        self.db = db
    
    def add_new_book(self):
        """Add a new book to the library system"""
        book_name = input("Enter name of the book:.....")
        book_author = input("Enter name of the author of the book:.....")
        book_code = input("Enter code of the book:.....")
        genre = input("Enter genre of book:.....")
        price = input("Enter price of the book:.....")
        count = int(input("Enter number of books available:....."))
        
        book = Book(self.db, book_code, book_name, book_author, genre, price, count)
        print((book_code, book_name, book_author, genre, price, count))
        print()
        print("To confirm to add the book enter 'Yes'")
        print("To cancel and return to main menu enter anything else")
        ch = input("Do you confirm?\n")
        print()
        
        if ch.lower() == 'yes':
            book.save()
            print("Book added successfully.")
            print(SEPARATOR)
            print()
        else:
            print("Book not added")
            print(SEPARATOR)
            print()
    
    def delete_book(self):
        """Remove a book from library"""
        book_id = input("Enter book ID:.....")
        ch = input(f"Do you wish to delete book with book code {book_id}:.....\n")
        
        if ch.lower() == 'yes':
            book = Book(self.db, book_id=book_id)
            book.delete()
            print(book_id, "successfully deleted")
            print(SEPARATOR)
            print()
        else:
            print(book_id, "not deleted")
            print(SEPARATOR)
            print()
    
    def display_all_books(self):
        """Display all books in library"""
        books = Book.get_all(self.db)
        print("  BOOK ID \t\t BOOK NAME \t AUTHOR   GENRE   PRICE   AVAILABLE")
        for book in books:
            print(book)
        print(SEPARATOR)
