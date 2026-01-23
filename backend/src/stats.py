"""
Statistics module for Library Manager
"""
from backend_utils import SEPARATOR


class Statistics:
    """Generates library statistics"""
    
    def __init__(self, db):
        """Initialize Statistics with database connection"""
        self.db = db
    
    def show_most_issued_book(self):
        """Show most issued book"""
        query = "select B.book_name, count(I.book_id) from issue_and_return I, book B where I.book_id = B.book_id group by B.book_id;"
        self.db.execute(query)
        results = self.db.fetchall()
        for record in results:
            print(record)
        print()
    
    def show_most_active_member(self):
        """Show most active member"""
        query = "select M.cust_name, count(I.cust_id) from issue_and_return I, member M where M.cust_id = I.cust_id group by I.cust_id;"
        self.db.execute(query)
        results = self.db.fetchall()
        for record in results:
            print(record)
        print()
    
    def show_best_selling_author(self):
        """Show best selling author"""
        query = "select B.author, count(B.author) from book B, issue_and_return I where B.book_id = I.book_id group by B.author;"
        self.db.execute(query)
        results = self.db.fetchall()
        for record in results:
            print(record)
        print()
    
    def show_issued_books(self):
        """Show currently issued books"""
        query = """select M.cust_name, B.book_name, I.date_of_issue 
                   from issue_and_return I, member M, book B 
                   where I.cust_id = M.cust_id and I.book_id = B.book_id 
                   and date_of_return is null;"""
        self.db.execute(query)
        issued_books = self.db.fetchall()
        
        if len(issued_books) == 0:
            print("No books are currently issued")
            print(SEPARATOR)
            print()
        else:
            for record in issued_books:
                print(record)
                print(SEPARATOR)
                print()
    
    def show_statistics_menu(self):
        """Display statistics menu"""
        while True:
            print("1. See most issued book")
            print("2. See most active member")
            print("3. See best selling author")
            print("4. Return to main menu")
            ch = int(input("Enter your choice:....."))
            print()
            
            if ch == 1:
                self.show_most_issued_book()
            elif ch == 2:
                self.show_most_active_member()
            elif ch == 3:
                self.show_best_selling_author()
            else:
                break
