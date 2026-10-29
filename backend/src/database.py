"""
Database connection and schema management for Library Manager
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from mysql.connector import connect, Error

# Load credentials from the project-root .env (no-op if the file is missing,
# e.g. in Docker where the variables come from the container environment)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Database:
    """Manages database connection and operations"""

    def __init__(
        self,
        host=None,
        user=None,
        password=None,
        database=None,
        port=None
    ):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = int(port or os.getenv("DB_PORT", "3306"))
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password if password is not None else os.getenv("DB_PASSWORD", "")
        self.database = database or os.getenv("DB_NAME", "project")
        self.connection = None
        self.cursor = None

        self.connect()
        self.initialize_database()
        self.create_tables()
        self.seed_mock_data()

    # ---------------- CONNECTION ---------------- #

    def connect(self):
        """Connect to MySQL server (without selecting DB)"""
        try:
            self.connection = connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                auth_plugin="mysql_native_password",
                use_pure=True
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            raise RuntimeError(f"Database connection failed: {e}")

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    # ---------------- HELPERS ---------------- #

    def execute(self, query, values=None):
        """Execute a SQL query"""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
        except Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Query failed: {e}")

    def commit(self):
        """Commit transaction"""
        self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def table_exists(self, table):
        query = "SHOW TABLES LIKE %s"
        self.execute(query, (table,))
        return self.fetchone() is not None

    # ---------------- DATABASE ---------------- #

    def initialize_database(self):
        """Create and select database"""
        self.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.execute(f"USE {self.database}")

    # ---------------- SCHEMA ---------------- #

    def create_tables(self):
        """Create all tables with proper schema"""

        # BOOK TABLE
        self.execute("""
        CREATE TABLE IF NOT EXISTS book (
            book_id VARCHAR(10) PRIMARY KEY,
            book_name VARCHAR(100) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre VARCHAR(30),
            price DECIMAL(7,2),
            count INT CHECK (count >= 0)
        );
        """)

        # MEMBER TABLE
        self.execute("""
        CREATE TABLE IF NOT EXISTS member (
            cust_id VARCHAR(10) PRIMARY KEY,
            cust_name VARCHAR(50) NOT NULL,
            dob DATE,
            gender CHAR(1),
            contact VARCHAR(15)
        );
        """)

        # MEMBER DETAILS TABLE
        self.execute("""
        CREATE TABLE IF NOT EXISTS member_details (
            cust_id VARCHAR(10) PRIMARY KEY,
            mail_id VARCHAR(50) UNIQUE,
            password VARCHAR(100),
            status VARCHAR(15),
            FOREIGN KEY (cust_id) REFERENCES member(cust_id)
                ON DELETE CASCADE
        );
        """)

        # ISSUE AND RETURN TABLE
        self.execute("""
        CREATE TABLE IF NOT EXISTS issue_and_return (
            issue_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id VARCHAR(10),
            cust_id VARCHAR(10),
            date_of_issue DATE,
            date_of_return DATE,
            days_issued INT,
            days_kept INT,
            penalty INT DEFAULT 0,
            FOREIGN KEY (book_id) REFERENCES book(book_id)
                ON DELETE CASCADE,
            FOREIGN KEY (cust_id) REFERENCES member(cust_id)
                ON DELETE CASCADE
        );
        """)

        self.commit()

    # ---------------- MOCK DATA ---------------- #

    def seed_mock_data(self):
        """Insert mock data only if tables are empty"""

        # BOOK DATA
        self.execute("SELECT COUNT(*) FROM book")
        if self.fetchone()[0] == 0:
            self.execute("""
            INSERT INTO book VALUES
            ('HP01JKR', 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Fantasy', 280.00, 4),
            ('PJ01RR', 'Percy Jackson and the Lightning Thief', 'Rick Riordan', 'Fantasy', 320.00, 3);
            """)

        # MEMBER DATA
        self.execute("SELECT COUNT(*) FROM member")
        if self.fetchone()[0] == 0:
            self.execute("""
            INSERT INTO member VALUES
            ('324J79', 'Lakshya Gupta', '2006-12-30', 'M', '9319027774'),
            ('268K04', 'Devanshhi Dhingra', '2006-08-13', 'F', '8287314273');
            """)

        # MEMBER DETAILS DATA
        self.execute("SELECT COUNT(*) FROM member_details")
        if self.fetchone()[0] == 0:
            self.execute("""
            INSERT INTO member_details VALUES
            ('324J79', 'lakshya@gmail.com', 'lakshya3012', 'active'),
            ('268K04', 'devanshhi@gmail.com', 'devanshhi1308', 'active');
            """)

        # ISSUE DATA
        self.execute("SELECT COUNT(*) FROM issue_and_return")
        if self.fetchone()[0] == 0:
            self.execute("""
            INSERT INTO issue_and_return
            (book_id, cust_id, date_of_issue, date_of_return, days_issued, days_kept, penalty)
            VALUES
            ('PJ01RR', '324J79', '2023-05-21', '2023-06-18', 30, 28, 0),
            ('HP01JKR', '268K04', '2023-07-13', '2023-08-07', 30, 24, 0);
            """)

        self.commit()
