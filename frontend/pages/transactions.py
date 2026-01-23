"""
Transactions page - issue, return books and view transaction history
"""

import streamlit as st
from datetime import date

from utils.database_helpers import (
    get_available_books_for_issue, get_issued_books_for_return,
    get_transaction_history, calculate_days, calculate_penalty
)


def show():
    """Display transactions page"""
    st.title("🔄 Transactions")
    st.markdown("---")
    
    # Get database from session state
    db = st.session_state.get('db')
    if not db:
        st.error("Database connection not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["Issue Book", "Return Book", "Transaction History"])
    
    with tab1:
        issue_book(db)
    
    with tab2:
        return_book(db)
    
    with tab3:
        view_transaction_history(db)


def issue_book(db):
    """Issue book form"""
    st.subheader("Issue Book to Member")
    with st.form("issue_book_form"):
        member_id = st.text_input(
            "Member ID",
            placeholder="e.g., 324J79",
            help="Member's ID"
        )
        
        available_books = get_available_books_for_issue(db)
        if available_books:
            book_options = [f"{book[0]} - {book[1]} by {book[2]}" for book in available_books]
            book_selection = st.selectbox("Select Book", options=book_options)
            book_id = book_selection.split(" - ")[0]
        else:
            st.warning("No books available to issue.")
            book_id = None
        
        issue_date = st.date_input("Issue Date", value=date.today())
        days_issued = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=365,
            value=14,
            help="Number of days book is issued for"
        )
        
        submitted = st.form_submit_button("Issue Book", use_container_width=True)
        
        if submitted:
            if not member_id or not book_id:
                st.error("❌ Please fill in all fields.")
            else:
                try:
                    query = "INSERT INTO issue_and_return (book_id, cust_id, date_of_issue, days_issued) VALUES(%s, %s, %s, %s);"
                    db.execute(query, (book_id, member_id, issue_date, int(days_issued)))
                    db.commit()
                    
                    # Update book count
                    query_update = "UPDATE book SET count = count - 1 WHERE book_id = %s;"
                    db.execute(query_update, (book_id,))
                    db.commit()
                    
                    st.success(f"✅ Book issued successfully to member {member_id}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error issuing book: {str(e)}")


def return_book(db):
    """Return book form"""
    st.subheader("Return Book from Member")
    with st.form("return_book_form"):
        member_id = st.text_input(
            "Member ID",
            placeholder="e.g., 324J79",
            help="Member's ID"
        )
        
        issued_books = get_issued_books_for_return(db)
        if issued_books:
            book_options = [f"{book[0]} - {book[1]}" for book in issued_books]
            book_selection = st.selectbox("Select Book to Return", options=book_options)
            book_id = book_selection.split(" - ")[0]
        else:
            st.warning("No books currently issued.")
            book_id = None
        
        return_date = st.date_input("Return Date", value=date.today())
        
        submitted = st.form_submit_button("Process Return", use_container_width=True)
        
        if submitted:
            if not member_id or not book_id:
                st.error("❌ Please fill in all fields.")
            else:
                try:
                    # Get issue details
                    query = "SELECT date_of_issue, days_issued FROM issue_and_return WHERE book_id = %s AND cust_id = %s AND date_of_return IS NULL;"
                    db.execute(query, (book_id, member_id))
                    result = db.fetchone()
                    
                    if result:
                        issue_date = result[0]
                        issue_days = result[1]
                        
                        # Calculate penalty
                        fine = calculate_penalty(issue_date, return_date, issue_days)
                        days_kept = calculate_days(issue_date, return_date)
                        
                        # Update return record
                        query_update = "UPDATE issue_and_return SET date_of_return = %s, days_kept = %s, penalty = %s WHERE book_id = %s AND cust_id = %s;"
                        db.execute(query_update, (return_date, days_kept, fine, book_id, member_id))
                        db.commit()
                        
                        # Update book count
                        query_count = "UPDATE book SET count = count + 1 WHERE book_id = %s;"
                        db.execute(query_count, (book_id,))
                        db.commit()
                        
                        st.success(f"✅ Book returned successfully!")
                        st.info(f"Days Kept: {days_kept} | Fine: ₹{fine if fine else 0}")
                        st.balloons()
                    else:
                        st.error("❌ No issued record found for this book and member.")
                except Exception as e:
                    st.error(f"❌ Error processing return: {str(e)}")


def view_transaction_history(db):
    """View transaction history"""
    st.subheader("Transaction History")
    transactions_df = get_transaction_history(db)
    if not transactions_df.empty:
        st.dataframe(transactions_df, use_container_width=True)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_by = st.selectbox("Filter by:", ["None", "Book", "Member"])
        
        if filter_by == "Book":
            book_filter = st.text_input("Enter Book ID:")
            if book_filter:
                filtered_df = transactions_df[transactions_df['Book ID'].str.contains(book_filter, case=False)]
                st.dataframe(filtered_df, use_container_width=True)
        
        elif filter_by == "Member":
            member_filter = st.text_input("Enter Member ID:")
            if member_filter:
                filtered_df = transactions_df[transactions_df['Member ID'].astype(str).str.contains(member_filter, case=False)]
                st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No transactions found.")
