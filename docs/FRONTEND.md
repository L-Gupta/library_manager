# Frontend Documentation

## Overview

The frontend is built with **Streamlit**, a modern Python web framework for data applications. It provides an interactive web interface for managing books, members, and library transactions.

**Location**: `frontend/`  
**Main Entry Point**: `frontend/dashboard.py`  
**Framework**: Streamlit 1.28.1+  

---

## Architecture

### Modular Structure

The frontend has been refactored into a clean, modular architecture:

```
frontend/
├── dashboard.py (80 lines)          # Main router & entry point
├── pages/                           # Page modules (UI)
│   ├── dashboard.py                 # Dashboard overview
│   ├── books.py                     # Book management
│   ├── members.py                   # Member management
│   ├── transactions.py              # Issue/Return books
│   └── statistics.py                # Analytics & charts
├── utils/                           # Utilities (Logic)
│   ├── config.py                    # Config & styling
│   └── database_helpers.py          # Database queries
└── components/                      # Custom components (future)
```

**Key Principle**: Separation of Concerns
- **pages/**: UI and user interactions
- **utils/**: Data retrieval and business logic
- **config.py**: Centralized settings

---

## Setup

### Prerequisites

```bash
# Required
Python 3.7+
pip (Python package manager)

# Optional
streamlit CLI (installed via pip)
```

### Installation Steps

#### 1. Install Dependencies

From the **root directory**:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit==1.28.1` - Web framework
- `mysql-connector-python==8.2.0` - Database driver
- `pandas==2.1.3` - Data processing
- `plotly==5.18.0` - Interactive charts

#### 2. Verify Database Connection

Copy the example file and fill in your MySQL credentials:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=project
```

`.env` is git-ignored and is read automatically by `backend/src/database.py` (via `python-dotenv`), which both the CLI and the dashboard use. Never commit real credentials.

#### 3. Ensure Backend is Set Up

The frontend imports backend classes from `../backend/src/`:
- `database.py` - Database connection
- `books.py` - Book class
- `members.py` - Member class
- `issue_return.py` - Transaction class
- `stats.py` - Statistics class
- `utils.py` - Helper functions

Make sure the backend is properly set up. See BACKEND.md for details.

---

## Running the Frontend

### From Root Directory

```bash
streamlit run frontend/dashboard.py
```

### From Frontend Directory

```bash
cd frontend
streamlit run dashboard.py
```

### Custom Configuration

```bash
# Different port
streamlit run frontend/dashboard.py --server.port 8502

# Different host
streamlit run frontend/dashboard.py --server.address 0.0.0.0

# Clear cache
streamlit cache clear
streamlit run frontend/dashboard.py
```

**Dashboard opens at**: `http://localhost:8501`

---

## How It Works

### 1. Application Startup (dashboard.py)

```python
# Step 1: Configure Streamlit
configure_page()

# Step 2: Initialize database connection (cached in session)
initialize_session()

# Step 3: Display sidebar navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Books", ...])

# Step 4: Route to selected page
if page == "Dashboard":
    dashboard.show()
```

### 2. Page Rendering (pages/*.py)

Each page module has a `show()` function:

```python
def show():
    st.title("Page Title")
    
    # Get database from session
    db = st.session_state.db
    
    # Render UI
    st.write("Content here")
```

### 3. Data Retrieval (utils/database_helpers.py)

All database queries are centralized:

```python
# Called by pages
books = get_all_books_data(db)  # Returns DataFrame
total_books = get_total_books(db)  # Returns number
```

---

## Page Descriptions

### Dashboard (`pages/dashboard.py`)

**Purpose**: Overview and key metrics

**Features**:
- 4 Metric Cards: Total Books, Members, Issued Books, Pending Fines
- Recent Transactions: Last 10 book transactions
- Real-time data updates

**Database Queries**:
- `get_total_books()`
- `get_total_members()`
- `get_issued_books_count()`
- `get_total_fines()`
- `get_transaction_history()`

---

### Books (`pages/books.py`)

**Purpose**: Manage book inventory

**3 Tabs**:

1. **View All Books**
   - Displays all books in a table
   - Columns: ID, Name, Author, Genre, Price, Available Copies
   - Sortable and filterable

2. **Add New Book**
   - Form with fields: ID, Title, Author, Genre, Price, Quantity
   - Validation for all required fields
   - Success confirmation with balloons animation

3. **Delete Book**
   - Selectbox to choose book
   - Confirmation before deletion
   - Success/error feedback

**Database Functions**:
- `get_all_books_data()` - Fetch all books
- Creates Book class instance
- Calls `book.save()` and `book.delete()`

---

### Members (`pages/members.py`)

**Purpose**: Register and manage members

**3 Tabs**:

1. **View All Members**
   - Display all registered members
   - Columns: ID, Name, DOB, Gender, Contact
   - Shows total count

2. **Register New Member**
   - Form fields: Name, DOB (year/month/day), Gender, Contact, Email, Password
   - Auto-generates unique Member ID (format: ###L##)
   - Saves to both `member` and `member_details` tables
   - Validation for email and phone format

3. **Change Member Status**
   - Selectbox to choose member
   - Radio buttons for status: active, inactive, suspended
   - Updates member status in database

**Database Functions**:
- `get_all_members_data()` - Fetch all members
- Creates Member class instance
- Calls `member.save()` and `member.update_status()`

---

### Transactions (`pages/transactions.py`)

**Purpose**: Book issue/return and transaction tracking

**3 Tabs**:

1. **Issue Book**
   - Form: Member ID, Book Selection, Issue Date, Days to Issue
   - Available books dropdown (only books with count > 0)
   - Decrements book stock on submission
   - Creates transaction record in database

2. **Return Book**
   - Form: Member ID, Book Selection, Return Date
   - Auto-calculates:
     - Days Kept
     - Fine Amount (₹0 if on time, ₹100+ if late)
   - Increments book stock
   - Updates transaction record with fine

3. **Transaction History**
   - Complete table of all transactions
   - Columns: Book ID, Book Name, Member ID, Member Name, Dates, Fine
   - Filters: By book ID, by member ID
   - Sortable and exportable

**Database Functions**:
- `get_available_books_for_issue()` - Books available to issue
- `get_issued_books_for_return()` - Currently issued books
- `get_transaction_history()` - All transactions
- Manual SQL queries for issue/return operations
- Uses `calculate_penalty()` from backend utils

---

### Statistics (`pages/statistics.py`)

**Purpose**: Data visualization and analytics

**4 Tabs**:

1. **Most Issued Books**
   - Horizontal bar chart
   - Shows top 10 books by issue count
   - Interactive hover tooltips

2. **Most Active Members**
   - Vertical bar chart
   - Shows top 10 members by transaction count
   - Color gradient visualization

3. **Best Authors**
   - Pie chart
   - Shows distribution of books by author
   - Click legend to toggle data

4. **Currently Issued Books**
   - Data table
   - Columns: Member Name, Book Name, Issue Date, Days Issued
   - Shows count of active loans

**Database Functions**:
- `get_most_issued_books()` - Books by frequency
- `get_active_members()` - Members by activity
- `get_best_authors()` - Authors by book count
- `get_currently_issued_books()` - Active loans

---

## Configuration & Styling

### Config File (`utils/config.py`)

Contains all configuration:

```python
# Database credentials live in the project-root .env file
# (read by backend/src/database.py), not in this file

# App metadata
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
```

### Styling

Custom CSS in `configure_page()`:
- Wide layout (more space)
- Consistent padding
- Metric card styling
- Responsive design

---

## Database Connection

### Session State Management

Database connection is cached in Streamlit session state:

```python
# In dashboard.py
st.session_state.db = get_database()

# Accessed by all pages
db = st.session_state.db
```

**Benefits**:
- ✅ Connection created once per session
- ✅ Cached for performance
- ✅ No connection leaks
- ✅ Accessible from all pages

### Caching

Database connection is decorated with `@st.cache_resource`:

```python
@st.cache_resource
def get_database():
    return Database(...)
```

This ensures:
- Single database instance per session
- Automatic cleanup on session end
- No redundant connections

---

## Key Functions

### Database Helper Functions (utils/database_helpers.py)

**Metrics** (4 functions):
- `get_total_books(db)` → number
- `get_total_members(db)` → number
- `get_issued_books_count(db)` → number
- `get_total_fines(db)` → float

**Data Fetching** (5 functions):
- `get_all_books_data(db)` → DataFrame
- `get_all_members_data(db)` → DataFrame
- `get_available_books_for_issue(db)` → list of tuples
- `get_issued_books_for_return(db)` → list of tuples
- `get_transaction_history(db)` → DataFrame

**Analytics** (4 functions):
- `get_most_issued_books(db)` → list of tuples
- `get_active_members(db)` → list of tuples
- `get_best_authors(db)` → list of tuples
- `get_currently_issued_books(db)` → DataFrame

**Connection**:
- `get_database()` → Database instance (cached)

---

## Common Tasks

### Add a New Page

1. Create `pages/my_page.py`:
```python
def show():
    st.title("My Page")
    db = st.session_state.db
    # Your page code
```

2. Import in `dashboard.py`:
```python
from pages import my_page
```

3. Add routing:
```python
elif page == "My Page":
    my_page.show()
```

4. Add to `PAGES` dict in `config.py`:
```python
'My Page': ('🔥', 'my_page'),
```

### Add Database Functions

1. Add to `utils/database_helpers.py`:
```python
def get_my_data(db):
    try:
        query = "SELECT * FROM table"
        db.execute(query)
        return db.fetchall()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []
```

2. Import in pages:
```python
from utils.database_helpers import get_my_data
```

### Modify Styling

Edit `utils/config.py`:
- `PAGE_CONFIG` - Streamlit page settings
- CSS in `configure_page()` - Custom styles
- `PAGES` - Navigation structure

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit==1.28.1
```

### "ModuleNotFoundError: No module named 'src'"
- Ensure you're running from correct directory
- Check `sys.path.insert()` in dashboard.py
- Verify backend path is correct

### Database Connection Error
- Check credentials in `.env`
- Verify MySQL is running
- Verify database 'project' exists
- Check network connectivity

### Page Not Loading
- Check `show()` function exists
- Verify imports in `dashboard.py`
- Check routing elif statement
- Look at Streamlit console output

### Performance Issues
- Streamlit caches database connection (good)
- Clear cache: `streamlit cache clear`
- Check database query performance
- Verify MySQL indexes

---

## Performance Tips

1. **Database Connection**: Already cached ✅
2. **Avoid reloads**: Use session state ✅
3. **Optimize queries**: All in database_helpers.py
4. **Pagination**: Add for large datasets
5. **Lazy loading**: Load data on demand

---

## Security

### SQL Injection Prevention
✅ All queries use parameterized statements with `%s` placeholders
✅ User input never directly concatenated

### Input Validation
✅ Email format validation
✅ Phone number length validation
✅ Required field checks
✅ Date range validation

### Password Security
⚠️ Current: Stored in plain text
🔒 Recommended: Hash passwords before storage (future improvement)

---

## Testing

### Manual Testing Checklist

- [ ] Streamlit runs without errors
- [ ] Dashboard page loads
- [ ] Can navigate to all pages
- [ ] Can add a book
- [ ] Can view all books
- [ ] Can delete a book
- [ ] Can register a member
- [ ] Can view all members
- [ ] Can change member status
- [ ] Can issue a book
- [ ] Can return a book
- [ ] Fine calculation works
- [ ] Statistics charts load
- [ ] All filters work

---

## Future Enhancements

### Planned Features
- [ ] Custom Streamlit components (components/ folder)
- [ ] Advanced search and filters
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Member profile photos
- [ ] Book cover images
- [ ] Rating and review system
- [ ] Reservation system

### Performance Improvements
- [ ] Database query optimization
- [ ] Caching strategies
- [ ] Pagination for large datasets
- [ ] Async database operations

### Code Improvements
- [ ] Add type hints
- [ ] Add unit tests
- [ ] Add logging
- [ ] Add error tracking (Sentry)

---

## Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| dashboard.py | Main router | 80 |
| pages/dashboard.py | Dashboard page | 40 |
| pages/books.py | Books page | 124 |
| pages/members.py | Members page | 156 |
| pages/transactions.py | Transactions page | 181 |
| pages/statistics.py | Statistics page | 126 |
| utils/config.py | Configuration | 70 |
| utils/database_helpers.py | Database queries | 282 |

**Total**: ~1,040 lines of well-organized code

---

## Summary

The frontend is a modern, modular Streamlit application with:
- ✅ Clean architecture (pages + utils separation)
- ✅ Scalable design (easy to add features)
- ✅ Production-ready (error handling, validation)
- ✅ Well-documented (inline comments)
- ✅ Performance optimized (caching)

Start with `streamlit run frontend/dashboard.py` and enjoy managing your library! 🎉
