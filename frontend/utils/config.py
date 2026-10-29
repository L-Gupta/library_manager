"""
Configuration and styling utilities for Streamlit dashboard
"""

import streamlit as st

# Database credentials are read from the project-root .env file
# (see .env.example) by backend/src/database.py

# Application metadata
APP_NAME = "Library Management System"
APP_VERSION = "2.1"
APP_ICON = "📚"

# Page configuration
PAGE_CONFIG = {
    'page_title': APP_NAME,
    'page_icon': APP_ICON,
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Navigation pages
PAGES = {
    'Dashboard': ('📊', 'dashboard'),
    'Books': ('📚', 'books'),
    'Members': ('👥', 'members'),
    'Transactions': ('🔄', 'transactions'),
    'Statistics': ('📈', 'statistics')
}

def configure_page():
    """Configure Streamlit page settings and styling"""
    st.set_page_config(**PAGE_CONFIG)
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
            .main {
                padding: 0rem 1rem;
            }
            .metric-card {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .sidebar .sidebar-content {
                padding-top: 2rem;
            }
            .header-container {
                text-align: center;
                margin-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

def get_page_options():
    """Get page navigation options"""
    return list(PAGES.keys())

def get_page_icon(page_name):
    """Get icon for a page"""
    return PAGES.get(page_name, ('❓', ''))[0]
