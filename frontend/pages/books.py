"""
Books management page - add, view, and delete books
"""

import streamlit as st
import sys
import os
from datetime import date

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

from books import Book, BookManager
from utils.database_helpers import get_all_books_data, get_available_books_for_issue


def show():
    """Display books management page"""
    st.title("📚 Books Management")
    st.markdown("---")
    
    # Get database from session state
    db = st.session_state.get('db')
    if not db:
        st.error("Database connection not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["View All Books", "Add New Book", "Delete Book"])
    
    with tab1:
        view_all_books(db)
    
    with tab2:
        add_new_book(db)
    
    with tab3:
        delete_book(db)


def view_all_books(db):
    """View all books in library"""
    st.subheader("All Books in Library")
    books_df = get_all_books_data(db)
    if not books_df.empty:
        st.dataframe(books_df, use_container_width=True)
        st.info(f"Total books: {len(books_df)}")
    else:
        st.warning("No books found in the library.")


def add_new_book(db):
    """Add new book form"""
    st.subheader("Add New Book")
    with st.form("add_book_form"):
        book_id = st.text_input(
            "Book ID",
            placeholder="e.g., HP01JKR",
            help="Unique identifier for the book"
        )
        book_name = st.text_input(
            "Book Name",
            placeholder="e.g., Harry Potter",
            help="Title of the book"
        )
        author = st.text_input(
            "Author",
            placeholder="e.g., J.K. Rowling",
            help="Author name"
        )
        genre = st.text_input(
            "Genre",
            placeholder="e.g., Fantasy",
            help="Book genre"
        )
        price = st.number_input(
            "Price (₹)",
            min_value=0.0,
            step=10.0,
            help="Price of the book"
        )
        count = st.number_input(
            "Available Copies",
            min_value=1,
            step=1,
            help="Number of copies available"
        )
        
        submitted = st.form_submit_button("Add Book", use_container_width=True)
        
        if submitted:
            if not all([book_id, book_name, author, genre, price, count]):
                st.error("❌ Please fill in all fields.")
            else:
                try:
                    book = Book(db, book_id, book_name, author, genre, float(price), int(count))
                    book.save()
                    st.success(f"✅ Book '{book_name}' added successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error adding book: {str(e)}")


def delete_book(db):
    """Delete book form"""
    st.subheader("Delete Book")
    books_df = get_all_books_data(db)
    if not books_df.empty:
        book_to_delete = st.selectbox(
            "Select Book to Delete",
            options=books_df['Book ID'].tolist(),
            format_func=lambda x: f"{x} - {books_df[books_df['Book ID']==x]['Book Name'].values[0]}"
        )
        
        if st.button("Delete Book", use_container_width=True, type="secondary"):
            try:
                book = Book(db, book_id=book_to_delete)
                book.delete()
                st.success(f"✅ Book '{book_to_delete}' deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error deleting book: {str(e)}")
    else:
        st.warning("No books available to delete.")
