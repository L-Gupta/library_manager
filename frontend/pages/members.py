"""
Members management page - register and manage members
"""

import streamlit as st
import sys
import os
from datetime import datetime, date

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

from members import Member, MemberManager
from utils.database_helpers import get_all_members_data


def show():
    """Display members management page"""
    st.title("👥 Members Management")
    st.markdown("---")
    
    # Get database from session state
    db = st.session_state.get('db')
    if not db:
        st.error("Database connection not available")
        return
    
    tab1, tab2, tab3 = st.tabs(["View All Members", "Register New Member", "Change Status"])
    
    with tab1:
        view_all_members(db)
    
    with tab2:
        register_new_member(db)
    
    with tab3:
        change_member_status(db)


def view_all_members(db):
    """View all members"""
    st.subheader("All Members")
    members_df = get_all_members_data(db)
    if not members_df.empty:
        st.dataframe(members_df, use_container_width=True)
        st.info(f"Total members: {len(members_df)}")
    else:
        st.warning("No members found.")


def register_new_member(db):
    """Register new member form"""
    st.subheader("Register New Member")
    with st.form("register_member_form"):
        name = st.text_input(
            "Full Name",
            placeholder="e.g., Lakshya Gupta",
            help="Member's full name"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.number_input(
                "Birth Year",
                min_value=1950,
                max_value=datetime.now().year-5,
                value=2000
            )
        with col2:
            month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        with col3:
            day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)
        
        gender = st.selectbox(
            "Gender",
            ["M", "F", "O"],
            help="Select gender"
        )
        contact = st.text_input(
            "Contact Number",
            placeholder="e.g., 9319027774",
            help="10-digit mobile number"
        )
        email = st.text_input(
            "Email",
            placeholder="e.g., user@example.com",
            help="Valid email address"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter a secure password",
            help="Member login password"
        )
        
        submitted = st.form_submit_button("Register Member", use_container_width=True)
        
        if submitted:
            if not all([name, contact, email, password]):
                st.error("❌ Please fill in all required fields.")
            else:
                try:
                    dob = date(int(year), int(month), int(day))
                    member_id_generated = Member.generate_unique_id(db)
                    member = Member(db, member_id_generated, name.title(), dob, gender.upper(), contact, email, password)
                    member.save()
                    st.success(f"✅ Member registered successfully!")
                    st.info(f"Member ID: **{member_id_generated}**")
                    st.balloons()
                except ValueError as e:
                    st.error(f"❌ Invalid date or contact: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error registering member: {str(e)}")


def change_member_status(db):
    """Change member status form"""
    st.subheader("Change Member Status")
    members_df = get_all_members_data(db)
    if not members_df.empty:
        selected_member = st.selectbox(
            "Select Member",
            options=members_df['Member ID'].tolist(),
            format_func=lambda x: f"{x} - {members_df[members_df['Member ID']==x]['Name'].values[0]}"
        )
        
        new_status = st.selectbox("New Status", ["active", "inactive", "suspended"])
        
        if st.button("Update Status", use_container_width=True):
            try:
                member = Member(db, member_id=selected_member)
                member.update_status(new_status)
                st.success(f"✅ Member status updated to '{new_status}'!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error updating status: {str(e)}")
    else:
        st.warning("No members available.")
