"""
Database helper functions for fetching data and metrics
"""

import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import importlib.util

# Add src directory to path for backend imports
backend_src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src')
if backend_src_path not in sys.path:
    sys.path.insert(0, backend_src_path)

from database import Database

# Import backend utils directly by file path to avoid naming conflicts
backend_utils_file = os.path.join(backend_src_path, 'backend_utils.py')
spec = importlib.util.spec_from_file_location("backend_utils", backend_utils_file)
backend_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_utils)

calculate_days = backend_utils.calculate_days
calculate_penalty = backend_utils.calculate_penalty


@st.cache_resource
def get_database():
    """Initialize and cache database connection"""
    try:
        from utils.config import DB_CONFIG
        db = Database(**DB_CONFIG)
        return db
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None


# ============ Metrics Functions ============

def get_total_books(db):
    """Get total number of books in library"""
    try:
        query = "SELECT SUM(count) FROM book;"
        db.execute(query)
        result = db.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        st.warning(f"Could not fetch total books: {str(e)}")
        return 0


def get_total_members(db):
    """Get total number of members"""
    try:
        query = "SELECT COUNT(*) FROM member;"
        db.execute(query)
        result = db.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        st.warning(f"Could not fetch total members: {str(e)}")
        return 0


def get_issued_books_count(db):
    """Get count of currently issued books"""
    try:
        query = "SELECT COUNT(*) FROM issue_and_return WHERE date_of_return IS NULL;"
        db.execute(query)
        result = db.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        st.warning(f"Could not fetch issued books count: {str(e)}")
        return 0


def get_total_fines(db):
    """Get total pending fines"""
    try:
        query = "SELECT COALESCE(SUM(penalty), 0) FROM issue_and_return WHERE penalty IS NOT NULL;"
        db.execute(query)
        result = db.fetchone()
        return result[0] if result[0] else 0
    except Exception as e:
        st.warning(f"Could not fetch total fines: {str(e)}")
        return 0


# ============ Data Fetching Functions ============

def get_all_books_data(db):
    """Fetch all books as DataFrame"""
    try:
        query = "SELECT book_id, book_name, author, genre, price, count FROM book;"
        db.execute(query)
        books = db.fetchall()
        if books:
            df = pd.DataFrame(books, columns=['Book ID', 'Book Name', 'Author', 'Genre', 'Price', 'Available Copies'])
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching books: {str(e)}")
        return pd.DataFrame()


def get_all_members_data(db):
    """Fetch all members as DataFrame"""
    try:
        query = "SELECT cust_id, cust_name, DOB, gender, contact FROM member;"
        db.execute(query)
        members = db.fetchall()
        if members:
            df = pd.DataFrame(members, columns=['Member ID', 'Name', 'Date of Birth', 'Gender', 'Contact'])
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching members: {str(e)}")
        return pd.DataFrame()


def get_available_books_for_issue(db):
    """Get list of available books (count > 0)"""
    try:
        query = "SELECT book_id, book_name, author FROM book WHERE count > 0;"
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error fetching available books: {str(e)}")
        return []


def get_issued_books_for_return(db):
    """Get list of currently issued books (not returned)"""
    try:
        query = """
            SELECT DISTINCT I.book_id, B.book_name 
            FROM issue_and_return I 
            JOIN book B ON I.book_id = B.book_id 
            WHERE I.date_of_return IS NULL;
        """
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error fetching issued books: {str(e)}")
        return []


def get_transaction_history(db):
    """Get transaction history as DataFrame"""
    try:
        query = """
            SELECT 
                I.book_id, 
                B.book_name,
                I.cust_id,
                M.cust_name,
                I.date_of_issue,
                I.date_of_return,
                I.days_issued,
                COALESCE(I.days_kept, 0) as days_kept,
                COALESCE(I.penalty, 0) as penalty
            FROM issue_and_return I
            JOIN book B ON I.book_id = B.book_id
            JOIN member M ON I.cust_id = M.cust_id
            ORDER BY I.date_of_issue DESC;
        """
        db.execute(query)
        transactions = db.fetchall()
        if transactions:
            df = pd.DataFrame(transactions, columns=[
                'Book ID', 'Book Name', 'Member ID', 'Member Name', 
                'Issue Date', 'Return Date', 'Days Issued', 'Days Kept', 'Fine'
            ])
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching transaction history: {str(e)}")
        return pd.DataFrame()


# ============ Analytics Functions ============

def get_most_issued_books(db):
    """Get most issued books data"""
    try:
        query = """
            SELECT B.book_name, COUNT(I.book_id) as issue_count
            FROM issue_and_return I
            JOIN book B ON I.book_id = B.book_id
            GROUP BY B.book_id
            ORDER BY issue_count DESC
            LIMIT 10;
        """
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error fetching most issued books: {str(e)}")
        return []


def get_active_members(db):
    """Get most active members data"""
    try:
        query = """
            SELECT M.cust_name, COUNT(I.cust_id) as transaction_count
            FROM issue_and_return I
            JOIN member M ON M.cust_id = I.cust_id
            GROUP BY I.cust_id
            ORDER BY transaction_count DESC
            LIMIT 10;
        """
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error fetching active members: {str(e)}")
        return []


def get_best_authors(db):
    """Get best selling authors data"""
    try:
        query = """
            SELECT B.author, COUNT(B.author) as book_count
            FROM book B
            JOIN issue_and_return I ON B.book_id = I.book_id
            GROUP BY B.author
            ORDER BY book_count DESC
            LIMIT 10;
        """
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error fetching best authors: {str(e)}")
        return []


def get_currently_issued_books(db):
    """Get currently issued books with member details"""
    try:
        query = """
            SELECT 
                M.cust_name,
                B.book_name,
                I.date_of_issue,
                I.days_issued
            FROM issue_and_return I
            JOIN member M ON I.cust_id = M.cust_id
            JOIN book B ON I.book_id = B.book_id
            WHERE I.date_of_return IS NULL
            ORDER BY I.date_of_issue DESC;
        """
        db.execute(query)
        issued = db.fetchall()
        if issued:
            df = pd.DataFrame(issued, columns=['Member Name', 'Book Name', 'Issue Date', 'Days Issued'])
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching currently issued books: {str(e)}")
        return pd.DataFrame()
