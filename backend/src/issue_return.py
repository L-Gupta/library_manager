"""
Book issue and return transaction module for Library Manager
"""
import datetime as dt
from backend_utils import SEPARATOR, calculate_days, calculate_penalty


class BookTransaction:
    """Handles book issue and return transactions"""
    
    def __init__(self, db):
        """Initialize BookTransaction with database connection"""
        self.db = db
    
    def issue_book(self):
        """Issue a book to a member"""
        y = int(input("Enter current year(YYYY):....."))
        m = int(input("Enter current month(MM):....."))
        d = int(input("Enter today's date(DD):....."))
        issue_date = dt.date(y, m, d)
        days_issued = int(input("Enter number of days book is issued:....."))
        member_id = input("Enter your membership ID:....")
        
        # Get available books
        query = "select * from book where count > 0;"
        self.db.execute(query)
        available_books = self.db.fetchall()
        
        print("Current books in library are:")
        for book in available_books:
            print(book)
        print()
        
        book_id = input("Enter book ID:.....")
        print()
        
        for book in available_books:
            if book[0] == book_id:
                if book[5] == 0:
                    print("Sorry, book out of stock")
                    print(SEPARATOR)
                    print()
                else:
                    # Insert issue record
                    query = "insert into issue_and_return (book_id, cust_id, date_of_issue, days_issued) values(%s, %s, %s, %s);"
                    values = (book_id, member_id, issue_date, days_issued)
                    self.db.execute(query, values)
                    self.db.commit()
                    
                    print(values)
                    print()
                    print("Book issued successful")
                    print(SEPARATOR)
                    print()
                    
                    # Update book count
                    query = "update book set count = count - 1 where book_id = %s;"
                    self.db.execute(query, (book_id,))
                    self.db.commit()
    
    def return_book(self):
        """Return a book from a member"""
        y = int(input("Enter current year(YYYY):....."))
        m = int(input("Enter current month(MM):....."))
        d = int(input("Enter current date(DD):....."))
        return_date = dt.date(y, m, d)
        member_id = input("Enter your membership ID:.....")
        book_id = input("Enter book ID:.....")
        
        # Update return date
        query = "update issue_and_return set date_of_return = %s where book_id = %s and cust_id = %s;"
        self.db.execute(query, (return_date, book_id, member_id))
        self.db.commit()
        
        # Get issue details
        query = "select date_of_issue, days_issued from issue_and_return where book_id = %s and cust_id = %s and date_of_return = %s;"
        self.db.execute(query, (book_id, member_id, return_date))
        result = self.db.fetchall()
        
        if result:
            issue_date = result[0][0]
            issue_days = result[0][1]
        
        print()
        
        # Calculate penalty and days kept
        fine = calculate_penalty(issue_date, return_date, issue_days)
        days_kept = calculate_days(issue_date, return_date)
        
        # Update transaction record
        query = "update issue_and_return set days_kept = %s, penalty = %s where cust_id = %s and book_id = %s;"
        self.db.execute(query, (days_kept, fine, member_id, book_id))
        self.db.commit()
        
        # Update book count
        query = "update book set count = count + 1 where book_id = %s;"
        self.db.execute(query, (book_id,))
        self.db.commit()
        
        print("Book returned successfully")
        print("You kept the book for", days_kept, "days")
        print("Your late fee is Rs", fine)
        print(SEPARATOR)
        print()
