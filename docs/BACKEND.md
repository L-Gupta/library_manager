# Backend Documentation

## Overview

The backend is built with **Python** and **MySQL**, providing the core business logic for the Library Management System. It includes data models, database operations, and utilities for managing books, members, and transactions.

**Location**: `backend/`  
**Language**: Python 3.7+  
**Database**: MySQL 5.7+  

---

## Architecture

### Modular Structure

```
backend/
├── src/                          # Source code
│   ├── main.py                   # CLI entry point
│   ├── database.py               # Database connection (150 lines)
│   ├── books.py                  # Book class & BookManager (120 lines)
│   ├── members.py                # Member class & MemberManager (180 lines)
│   ├── issue_return.py           # BookTransaction class (100 lines)
│   ├── stats.py                  # Statistics & Display classes (80 lines)
│   └── utils.py                  # Helper functions & constants (30 lines)
│
└── sql/                          # Database schema
    └── schema.sql                # Tables & sample data
```

### Design Pattern

**Object-Oriented Architecture**:
- **Entity Classes**: `Book`, `Member` - Represent data objects
- **Manager Classes**: `BookManager`, `MemberManager` - Handle collections
- **Transaction Class**: `BookTransaction` - Manage issue/return logic
- **Database Class**: `Database` - Handle SQL operations
- **Statistics Class**: `Statistics` - Generate reports

---

## Setup

### Prerequisites

```bash
# Required
Python 3.7+
MySQL Server 5.7+
pip (Python package manager)

# Verify installations
python --version
mysql --version
```

### Installation Steps

#### 1. Install Python Dependencies

From the **root directory**:

```bash
pip install -r requirements.txt
```

This installs:
- `mysql-connector-python==8.2.0` - MySQL driver

#### 2. Verify MySQL Server

Ensure MySQL is running:

```bash
# On Windows
# Check Services or use:
mysql -u root -p

# On macOS/Linux
mysql -u root -p
```

#### 3. Create Database

```bash
mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE project;
USE project;
```

#### 4. Initialize Schema

From the **root directory**:

```bash
mysql -u root -p project < backend/sql/schema.sql
```

This creates:
- ✅ 4 tables: book, member, member_details, issue_and_return
- ✅ Proper relationships and constraints
- ✅ Sample data for testing

#### 5. Configure Database Connection

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

`Database()` reads these values when constructed; explicit arguments (e.g. `Database(host=..., password=...)`) override them.

---

## Running the Backend

### Option 1: CLI Application

From the **backend/src** directory:

```bash
cd backend/src
python main.py
```

This launches an interactive menu:

```
╔════════════════════════════════════════════╗
║   📚 LIBRARY MANAGEMENT SYSTEM v2.1        ║
║          Main Menu                         ║
╠════════════════════════════════════════════╣
║  1. Book Operations                        ║
║  2. Member Operations                      ║
║  3. Issue/Return Books                     ║
║  4. Statistics & Reports                   ║
║  5. Exit                                   ║
╚════════════════════════════════════════════╝
```

### Option 2: Through Frontend

The frontend automatically uses the backend:

```bash
streamlit run frontend/dashboard.py
```

The frontend imports and uses backend classes.

---

## How It Works

### 1. Database Connection (database.py)

```python
class Database:
    def __init__(self, host, user, password, database):
        # Creates connection
        self.connection = mysql.connector.connect(...)
    
    def execute(self, query, params=None):
        # Executes SQL query
        # Uses parameterized statements (prevents SQL injection)
    
    def fetchone(self):
        # Returns single result
    
    def fetchall(self):
        # Returns all results
    
    def commit(self):
        # Saves changes
    
    def rollback(self):
        # Undoes changes on error
```

### 2. Entity Classes

#### Book Class

```python
class Book:
    def __init__(self, db, book_id, book_name, author, genre, price, count):
        self.db = db
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.genre = genre
        self.price = price
        self.count = count  # Available copies
    
    def save(self):
        # Insert into database
    
    def delete(self):
        # Remove from database
    
    def update_count(self, new_count):
        # Update available copies
```

#### Member Class

```python
class Member:
    def __init__(self, db, member_id, name, dob, gender, contact, email, password):
        self.db = db
        self.member_id = member_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact = contact
        self.email = email
        self.password = password
    
    def save(self):
        # Insert into member and member_details tables
    
    def update_status(self, status):
        # Change member status (active/inactive/suspended)
    
    @staticmethod
    def generate_unique_id(db):
        # Auto-generates member ID (format: ###L##)
```

### 3. Manager Classes

#### BookManager

```python
class BookManager:
    @staticmethod
    def get_all_books(db):
        # Retrieve all books
    
    @staticmethod
    def get_available_books(db):
        # Books with count > 0
    
    @staticmethod
    def get_book_by_id(db, book_id):
        # Get specific book
```

#### MemberManager

```python
class MemberManager:
    @staticmethod
    def get_all_members(db):
        # Retrieve all members
    
    @staticmethod
    def get_member_by_id(db, member_id):
        # Get specific member
    
    @staticmethod
    def get_active_members(db):
        # Members with status = 'active'
```

### 4. Transaction Class (issue_return.py)

```python
class BookTransaction:
    @staticmethod
    def issue_book(db, book_id, member_id, issue_date, days_issued):
        # 1. Check book availability
        # 2. Check member exists
        # 3. Create transaction record
        # 4. Decrement book stock
    
    @staticmethod
    def return_book(db, book_id, member_id, return_date):
        # 1. Get issue details
        # 2. Calculate penalty
        # 3. Update transaction with return date
        # 4. Increment book stock
```

### 5. Statistics Class (stats.py)

```python
class Statistics:
    @staticmethod
    def get_most_issued_books(db):
        # Top 10 books by issue count
    
    @staticmethod
    def get_active_members(db):
        # Top 10 members by transaction count
    
    @staticmethod
    def get_best_authors(db):
        # Top 10 authors
    
    @staticmethod
    def get_unreturned_books(db):
        # Books not yet returned
```

---

## Database Schema

### Tables

#### 1. book Table

```sql
CREATE TABLE book (
    book_id VARCHAR(50) PRIMARY KEY,
    book_name VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    price DECIMAL(10, 2),
    count INT DEFAULT 0  -- Available copies
);
```

**Purpose**: Store book inventory  
**Primary Key**: book_id (unique)  
**Relationships**: Referenced by issue_and_return

---

#### 2. member Table

```sql
CREATE TABLE member (
    cust_id VARCHAR(20) PRIMARY KEY,  -- Auto-generated ID
    cust_name VARCHAR(100) NOT NULL,
    DOB DATE,
    gender CHAR(1),
    contact VARCHAR(20)
);
```

**Purpose**: Store member basic info  
**Primary Key**: cust_id (auto-generated format: ###L##)  
**Relationships**: Referenced by member_details and issue_and_return

---

#### 3. member_details Table

```sql
CREATE TABLE member_details (
    cust_id VARCHAR(20) PRIMARY KEY,
    mail_id VARCHAR(100),
    password VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active'  -- active/inactive/suspended
    
    FOREIGN KEY (cust_id) REFERENCES member(cust_id)
);
```

**Purpose**: Store member credentials and status  
**Primary Key**: cust_id (foreign key to member)  
**Status Values**: active, inactive, suspended

---

#### 4. issue_and_return Table

```sql
CREATE TABLE issue_and_return (
    book_id VARCHAR(50),
    cust_id VARCHAR(20),
    date_of_issue DATE,
    date_of_return DATE NULL,  -- NULL if not returned
    days_issued INT,           -- Loan period
    days_kept INT NULL,        -- Actual days kept
    penalty DECIMAL(10, 2) DEFAULT 0,
    
    PRIMARY KEY (book_id, cust_id, date_of_issue),
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (cust_id) REFERENCES member(cust_id)
);
```

**Purpose**: Track book transactions  
**Composite Key**: (book_id, cust_id, date_of_issue)  
**Relationships**: Links books and members

---

### Relationships

```
book (1) ──────────────── (M) issue_and_return
                               │
                               │
member (1) ───────────────── (M) issue_and_return

member (1) ──────────── (1) member_details
```

### Constraints

- ✅ Foreign key references enforced
- ✅ NOT NULL constraints on required fields
- ✅ Default values (status='active', penalty=0)
- ✅ Primary keys prevent duplicates
- ✅ Composite key prevents duplicate transactions

---

## Key Functions

### Database Operations (database.py)

```python
# Initialize connection
db = Database(host, user, password, database)

# Execute query with parameters (safe)
db.execute("SELECT * FROM book WHERE book_id = %s", (book_id,))

# Fetch results
result = db.fetchone()      # Single row
results = db.fetchall()     # All rows

# Save changes
db.commit()

# Undo changes
db.rollback()

# Close connection
db.close()
```

### Book Operations (books.py)

```python
# Create book
book = Book(db, "B001", "Title", "Author", "Genre", 299, 5)
book.save()

# Get all books
books = BookManager.get_all_books(db)

# Get available books
available = BookManager.get_available_books(db)

# Delete book
book = Book(db, book_id="B001")
book.delete()

# Update stock
book.update_count(3)
```

### Member Operations (members.py)

```python
# Generate unique ID
member_id = Member.generate_unique_id(db)

# Create member
member = Member(db, member_id, "John Doe", dob, "M", "9876543210", "john@email.com", "pwd")
member.save()

# Get all members
members = MemberManager.get_all_members(db)

# Update status
member = Member(db, member_id="123A45")
member.update_status("inactive")
```

### Transaction Operations (issue_return.py)

```python
# Issue book
BookTransaction.issue_book(db, "B001", "123A45", issue_date, 14)

# Return book
BookTransaction.return_book(db, "B001", "123A45", return_date)

# Penalty calculated automatically based on:
# - Days issued (requested)
# - Days kept (actual)
# - Formula: ₹100 for 1-7 days late, ₹100 + ₹20/day for 8+ days
```

### Statistics (stats.py)

```python
# Get most issued books
stats = Statistics.get_most_issued_books(db)

# Get active members
members = Statistics.get_active_members(db)

# Get best authors
authors = Statistics.get_best_authors(db)

# Get unreturned books
unreturned = Statistics.get_unreturned_books(db)
```

### Utilities (utils.py)

```python
# Calculate days between dates
days = calculate_days(date1, date2)

# Calculate penalty amount
fine = calculate_penalty(issue_date, return_date, days_issued)

# Print formatted output
display_books(books_list)
display_members(members_list)
```

---

## Penalty Calculation

### Formula

```
If days_kept ≤ days_issued:
    penalty = ₹0 (returned on time)

If days_kept > days_issued:
    days_overdue = days_kept - days_issued
    
    If days_overdue ≤ 7:
        penalty = ₹100
    
    If days_overdue > 7:
        penalty = ₹100 + (₹20 × (days_overdue - 7))
```

### Examples

```
Loan Period: 14 days

Return on Day 14: Penalty = ₹0 ✅
Return on Day 17: Penalty = ₹100 ⚠️
Return on Day 21: Penalty = ₹100 + (₹20 × 4) = ₹180 ⚠️
Return on Day 30: Penalty = ₹100 + (₹20 × 13) = ₹360 ❌
```

---

## Security Features

### SQL Injection Prevention

✅ All queries use parameterized statements:

```python
# GOOD - Safe
db.execute("SELECT * FROM book WHERE book_id = %s", (book_id,))

# BAD - Vulnerable
db.execute(f"SELECT * FROM book WHERE book_id = '{book_id}'")
```

### Password Storage

⚠️ **Current**: Passwords stored in plain text  
🔒 **Recommended**: Hash with bcrypt before storing

```python
# Future improvement
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Data Validation

✅ Input validation in classes
✅ Foreign key constraints enforced
✅ Transaction rollback on error

---

## Common Operations

### Add a Book

```python
from database import Database
from books import Book

db = Database('localhost', 'root', 'password', 'project')
book = Book(db, 'B001', 'Python Guide', 'John Doe', 'Programming', 499, 5)
book.save()
db.close()
```

### Register a Member

```python
from members import Member
from datetime import date

db = Database('localhost', 'root', 'password', 'project')
member_id = Member.generate_unique_id(db)
member = Member(db, member_id, 'Jane Doe', date(1995, 5, 15), 'F', '9876543210', 'jane@email.com', 'password123')
member.save()
db.close()
```

### Issue a Book

```python
from issue_return import BookTransaction
from datetime import date

db = Database('localhost', 'root', 'password', 'project')
BookTransaction.issue_book(db, 'B001', '123A45', date.today(), 14)
db.close()
```

### Return a Book

```python
from issue_return import BookTransaction
from datetime import date

db = Database('localhost', 'root', 'password', 'project')
BookTransaction.return_book(db, 'B001', '123A45', date.today())
db.close()
```

---

## Testing

### Sample Data

The `schema.sql` includes sample data:

```
Books:
- HP001: Harry Potter (J.K. Rowling)
- TG001: The Great Gatsby (F.S. Fitzgerald)

Members:
- 001A01: John Doe
- 002B02: Jane Smith

Transactions:
- Sample issue/return records
```

### Testing Checklist

- [ ] Database connection works
- [ ] Can create books
- [ ] Can register members
- [ ] Can issue books
- [ ] Can return books
- [ ] Penalty calculation correct
- [ ] Member ID generation unique
- [ ] Status updates work
- [ ] Queries return correct data
- [ ] Error handling works

---

## Troubleshooting

### "Access denied for user 'root'"
```bash
# Verify password
mysql -u root -p
# Update DB_PASSWORD in .env
```

### "Unknown database 'project'"
```bash
# Initialize schema
mysql -u root -p project < backend/sql/schema.sql
```

### "No module named 'mysql'"
```bash
# Install connector
pip install mysql-connector-python==8.2.0
```

### "Book with ID already exists"
- Book ID must be unique
- Change book_id and try again

### "Member not found"
- Verify member_id exists
- Check member is active (not suspended)

### "SQL error in transaction"
- Check date formats (YYYY-MM-DD)
- Verify book/member exist
- Check for duplicate transactions

---

## Performance Optimization

### Database Indexes

Current indexes (in schema):
- PRIMARY KEY on all tables
- FOREIGN KEY indexes

**Future improvements**:
- Add index on `book_name` for search
- Add index on `cust_name` for search
- Add index on `author` for analytics

### Query Optimization

Current approach:
- Direct queries with parameters
- Efficient join operations
- Proper WHERE clauses

**Future improvements**:
- Add pagination for large datasets
- Cache frequently accessed data
- Use prepared statements

---

## Future Enhancements

### Features
- [ ] Book reservations
- [ ] Multi-user authentication
- [ ] Email notifications
- [ ] Fine payment tracking
- [ ] Book recommendations
- [ ] Member ratings
- [ ] Wishlist system

### Code Improvements
- [ ] Add type hints
- [ ] Add unit tests
- [ ] Add logging
- [ ] Add API layer (Flask/FastAPI)
- [ ] Better error messages
- [ ] Transaction handling

### Database Improvements
- [ ] Backup system
- [ ] Query optimization
- [ ] Connection pooling
- [ ] Stored procedures
- [ ] Views for common queries

---

## Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| database.py | DB connection & operations | 150 |
| books.py | Book class & manager | 120 |
| members.py | Member class & manager | 180 |
| issue_return.py | Transaction logic | 100 |
| stats.py | Statistics & reports | 80 |
| utils.py | Helper functions | 30 |
| main.py | CLI entry point | 150 |
| schema.sql | Database schema | 100+ |

**Total**: ~900 lines of backend code

---

## Summary

The backend provides:
- ✅ Object-oriented design
- ✅ Safe database operations (parameterized queries)
- ✅ Complete business logic
- ✅ Proper error handling
- ✅ Clean, maintainable code
- ✅ Scalable architecture

**Key Features**:
- Book management (add, view, delete)
- Member management (register, view, status)
- Transaction tracking (issue, return, history)
- Automatic penalty calculation
- Real-time statistics
- Data integrity via foreign keys

Start with database setup, then explore the CLI or use through the frontend! 🚀
