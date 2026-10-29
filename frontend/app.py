"""
Library Management System - Streamlit Dashboard
Main entry point for the web application

This is the refactored main file that imports and routes to individual page modules.
Previous monolithic dashboard.py has been split into organized modules for better
code management and debugging.

Folder Structure:
├── app.py (THIS FILE - Main router)
├── pages/
│   ├── __init__.py
│   ├── dashboard.py (Dashboard home page)
│   ├── books.py (Books management)
│   ├── members.py (Members management)
│   ├── transactions.py (Issue/Return books)
│   └── statistics.py (Analytics & charts)
├── utils/
│   ├── __init__.py
│   ├── config.py (Configuration & styling)
│   └── database_helpers.py (Database queries & metrics)
└── components/
    └── __init__.py (For future custom components)
"""

import streamlit as st

# Import configuration - these should work since we're running from the frontend directory
from utils.config import configure_page, PAGES, APP_NAME, APP_VERSION
from utils.database_helpers import get_database

# Import page modules  
from pages import dashboard, books, members, transactions, statistics


def initialize_session():
    """Initialize session state with database connection"""
    if 'db' not in st.session_state:
        db = get_database()
        if db is None:
            st.error("❌ Failed to connect to database. Please check your connection settings.")
            st.stop()
        st.session_state.db = db


def main():
    """Main application function"""
    # Configure page
    configure_page()
    
    # Initialize session
    initialize_session()
    
    # Get database from session
    db = st.session_state.db
    
    # Sidebar navigation
    st.sidebar.title("📚 Library Management")
    st.sidebar.markdown("---")
    
    page_names = list(PAGES.keys())
    page_icons = [PAGES[name][0] for name in page_names]
    
    page = st.sidebar.radio(
        "Navigation Menu",
        page_names,
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📌 {APP_NAME} v{APP_VERSION}\nBuilt with Streamlit")
    
    # Route to pages
    if page == "Dashboard":
        dashboard.show()
    elif page == "Books":
        books.show()
    elif page == "Members":
        members.show()
    elif page == "Transactions":
        transactions.show()
    elif page == "Statistics":
        statistics.show()


if __name__ == "__main__":
    main()
