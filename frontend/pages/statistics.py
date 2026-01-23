"""
Statistics and analytics page - visualize library data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database_helpers import (
    get_most_issued_books, get_active_members,
    get_best_authors, get_currently_issued_books
)


def show():
    """Display statistics page"""
    st.title("📈 Statistics & Analytics")
    st.markdown("---")
    
    # Get database from session state
    db = st.session_state.get('db')
    if not db:
        st.error("Database connection not available")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Most Issued Books",
        "Active Members",
        "Best Authors",
        "Currently Issued"
    ])
    
    with tab1:
        show_most_issued_books(db)
    
    with tab2:
        show_active_members(db)
    
    with tab3:
        show_best_authors(db)
    
    with tab4:
        show_currently_issued(db)


def show_most_issued_books(db):
    """Display most issued books chart"""
    st.subheader("Most Issued Books")
    most_issued = get_most_issued_books(db)
    if most_issued:
        df = pd.DataFrame(most_issued, columns=['Book Name', 'Issue Count'])
        
        fig = px.bar(
            df,
            x='Book Name',
            y='Issue Count',
            title='Books by Number of Issues',
            color='Issue Count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No book issue data available.")


def show_active_members(db):
    """Display active members chart"""
    st.subheader("Most Active Members")
    active_members = get_active_members(db)
    if active_members:
        df = pd.DataFrame(active_members, columns=['Member Name', 'Transaction Count'])
        
        fig = px.bar(
            df,
            x='Member Name',
            y='Transaction Count',
            title='Members by Number of Transactions',
            color='Transaction Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No member activity data available.")


def show_best_authors(db):
    """Display best authors pie chart"""
    st.subheader("Best Authors")
    best_authors = get_best_authors(db)
    if best_authors:
        df = pd.DataFrame(best_authors, columns=['Author', 'Books Issued'])
        
        fig = px.pie(
            df,
            names='Author',
            values='Books Issued',
            title='Books Issued by Author',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No author data available.")


def show_currently_issued(db):
    """Display currently issued books"""
    st.subheader("Currently Issued Books")
    issued_df = get_currently_issued_books(db)
    if not issued_df.empty:
        st.dataframe(issued_df, use_container_width=True)
        st.info(f"Total currently issued: {len(issued_df)} books")
    else:
        st.info("No books currently issued.")
