"""
Library Manager - Main Application
"""
from database import Database
from books import BookManager
from members import MemberManager
from issue_return import BookTransaction
from stats import Statistics
from backend_utils import SEPARATOR

MAIN_SEPARATOR = "x--------------------x--------------------x--------------------LIBRARY RECORDS--------------------x--------------------x--------------------x"


class LibraryManager:
    """Main controller for the library management system"""
    
    def __init__(self):
        """Initialize the library manager"""
        self.db = Database()
        self.book_manager = BookManager(self.db)
        self.member_manager = MemberManager(self.db)
        self.transaction_manager = BookTransaction(self.db)
        self.statistics = Statistics(self.db)
    
    def display_main_menu(self):
        """Display the main menu"""
        while True:
            print("x--------------------x--------------------MAIN MENU--------------------x--------------------x")
            print("1. Add a new book to the library records.")
            print("2. Add a new member to the library.")
            print("3. Issue a book.")
            print("4. Return a book.")
            print("5. Delete a book from the library records.")
            print("6. Change status of a member.")
            print("7. Display all books.")
            print("8. Display all members")
            print("9. Display all issued books and their owners")
            print("10. Show statistics")
            print("Enter anything else to exit program.")
            
            try:
                choice = int(input("Enter your decision:......"))
            except ValueError:
                print("Invalid input. Exiting...")
                break
            
            print()
            
            if choice == 1:
                print("x--------------------x--------------------BOOK INSERTION--------------------x--------------------x")
                self.book_manager.add_new_book()
            elif choice == 2:
                print("x--------------------x--------------------NEW MEMBER--------------------x--------------------x")
                self.member_manager.register_new_member()
            elif choice == 3:
                print("x--------------------x--------------------BOOK ISSUE--------------------x--------------------x")
                self.transaction_manager.issue_book()
            elif choice == 4:
                print("x--------------------x--------------------BOOK RETURN--------------------x--------------------x")
                self.transaction_manager.return_book()
            elif choice == 5:
                print("x--------------------x--------------------BOOK DELETION--------------------x--------------------x")
                self.book_manager.delete_book()
            elif choice == 6:
                print("x--------------------x--------------------MEMBER STATUS--------------------x--------------------x")
                self.member_manager.change_member_status()
            elif choice == 7:
                print("x--------------------x--------------------BOOKS IN LIBRARY--------------------x--------------------x")
                self.book_manager.display_all_books()
            elif choice == 8:
                print("x--------------------x--------------------OUR CURRENT MEMBERS--------------------x--------------------x")
                self.member_manager.display_all_members()
            elif choice == 9:
                print("x--------------------x--------------------CURRENTLY ISSUED BOOKS--------------------x--------------------x")
                self.statistics.show_issued_books()
            elif choice == 10:
                print("x--------------------x--------------------STATISTICS--------------------x--------------------x")
                self.statistics.show_statistics_menu()
            else:
                self.db.close()
                print("x--------------------x--------------------x--------------------THANK YOU--------------------x--------------------x--------------------x")
                break
    
    def run(self):
        """Run the library manager application"""
        print(MAIN_SEPARATOR)
        self.db.initialize_tables()
        self.display_main_menu()


if __name__ == "__main__":
    library = LibraryManager()
    library.run()
