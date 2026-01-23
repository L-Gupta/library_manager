"""
Dashboard page - displays overview and key metrics
"""

import streamlit as st
from utils.database_helpers import (
    get_total_books, get_total_members, get_issued_books_count,
    get_total_fines, get_transaction_history
)


def show():
    """Display dashboard page"""
    st.title("📊 Library Dashboard")
    st.markdown("---")
    
    # Get database from session state
    db = st.session_state.get('db')
    if not db:
        st.error("Database connection not available")
        return
    
    # Get metrics
    total_books = get_total_books(db)
    total_members = get_total_members(db)
    issued_books = get_issued_books_count(db)
    total_fines = get_total_fines(db)
    
    # Display metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Books", total_books, delta=None)
    
    with col2:
        st.metric("👥 Total Members", total_members, delta=None)
    
    with col3:
        st.metric("🏷️ Issued Books", issued_books, delta=None)
    
    with col4:
        st.metric("💰 Pending Fines", f"₹{total_fines}", delta=None)
    
    st.markdown("---")
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    transactions_df = get_transaction_history(db)
    if not transactions_df.empty:
        st.dataframe(transactions_df.tail(10), use_container_width=True)
    else:
        st.info("No transactions found.")
