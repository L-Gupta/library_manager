"""
Database connection and management for Library Manager
"""
import mysql.connector as msc


class Database:
    """Manages database connection and operations"""
    
    def __init__(self, host='localhost', user='root', password='lakshya', database='project'):
        """Initialize database connection"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        self.connection = msc.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
    
    def execute(self, query, values=None):
        """Execute a query"""
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
    
    def fetchone(self):
        """Fetch one result"""
        return self.cursor.fetchone()
    
    def fetchall(self):
        """Fetch all results"""
        return self.cursor.fetchall()
    
    def commit(self):
        """Commit changes to database"""
        self.connection.commit()
    
    def table_exists(self, table):
        """Check if a table exists in the database"""
        query = "show tables like %s"
        self.execute(query, (table,))
        return self.fetchone() is not None
    
    def initialize_tables(self):
        """Create databases, tables and add mock data"""
        # Creating a database if does not exist
        self.execute("create database if not exists project;")
        self.execute("use project;")
        
        # Creating table book
        if self.table_exists('book'):
            print("The table 'book' already exists in the MySQL server")
        else:
            self.execute("""create table if not exists book(
                book_id varchar(10), 
                book_name varchar(50), 
                author varchar(20), 
                genre varchar(10), 
                price varchar(7), 
                count int
            );""")
            self.execute("insert into book values('HP01JKR', 'Harry Potter and the Philosopher stone','J.K.Rowling', 'Fantasy', 280.00, 4);")
            self.execute("insert into book values('PJ01RR', 'Percy Jackson and the Lightning Thied','Rick Riordan', 'Fantasy', 320.00, 3);")
            self.commit()
        
        # Creating table member
        if self.table_exists('member'):
            print("The table 'member' already exists in the MySQL server")
        else:
            self.execute("""create table if not exists member(
                cust_id int, 
                cust_name varchar(20), 
                DOB date, 
                gender char(1), 
                contact int
            );""")
            self.execute("insert into member values('324J79', 'Lakshya Gupta','2006-12-30', 'M', 9319027774);")
            self.execute("insert into member values('268K04', 'Devanshhi Dhingra','2006-08-13', 'F', 8287314273);")
            self.commit()

        # Creating table issue_and_return
        if self.table_exists('issue_and_return'):
            print("The table 'issue_and_return' already exists in the MySQL server")
        else:
            self.execute("""create table if not exists issue_and_return(
                book_id varchar(10), 
                cust_id int, 
                date_of_issue date, 
                date_of_return date, 
                days_issued int, 
                days_kept int, 
                penalty int default 0
            );""")
            self.execute("insert into issue_and_return values('PJ01RR', '324J79', '2023-05-21', '2023-06-18', 30, 28, 0);")
            self.execute("insert into issue_and_return values('HP01JKR', '268K04', '2023-07-13', '2023-08-07', 30, 24, 0);")
            self.commit()

        # Creating table member_details
        if self.table_exists('member_details'):
            print("The table 'member_details' already exists in the MySQL server")
        else:   
            self.execute("""create table if not exists member_details(
                cust_id int, 
                mail_id varchar(30), 
                password varchar(20), 
                status varchar(10)
            );""")
            self.execute("insert into member_details values('324J79', 'lakshya@gmail.com', 'lakshya3012', 'active');")
            self.execute("insert into member_details values('268K04', 'devanshhi@gmail.com', 'devanshhi1308', 'active');")
            self.commit()

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
