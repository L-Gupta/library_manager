# 📚 Library Management System

A modern, object-oriented Python library management system with MySQL database backend and production-ready Streamlit dashboard. Manage books, members, track book issues/returns with automatic fine calculation, and generate insightful analytics.

**Status**: ✅ **FULLY IMPLEMENTED & PRODUCTION READY**  
**Version**: 2.1  
**Last Updated**: January 2026

---

## ✨ Key Features

### 📚 Book Management
- Add new books with title, author, genre, price, and quantity
- View complete book inventory with available stock tracking
- Delete books from the library
- Automatic stock adjustment on issue/return
- Search and filter books by title, author, or genre

### 👥 Member Management
- Register new members with auto-generated unique ID (format: ###L##)
- Capture comprehensive member details (name, DOB, gender, contact, email, address)
- View all registered members
- Change member status (Active/Inactive/Suspended)
- Track member transaction history

### 📤 Book Transactions
- Issue books to members with availability checks
- Return books with automatic penalty calculation
- Penalty Formula: ₹100 for 1-7 days late; ₹100 + ₹20/day for 8+ days late
- Track complete transaction history
- View currently issued books with due dates

### 📊 Advanced Analytics & Reports
- Most Issued Books - Bar chart ranking by frequency
- Most Active Members - Chart showing transaction counts
- Best Selling Authors - Pie chart distribution
- Genre distribution analysis
- Overdue books with calculated penalties
- Real-time KPI dashboard (total books, members, issued, fines)

### 🔒 Security & Data Integrity
- Parameterized SQL queries (prevents SQL injection)
- Database connection pooling with caching
- Input validation on all forms
- Foreign key relationships enforced
- Automatic transaction rollback on errors

### 🌐 Web Dashboard
- 5 main pages with intuitive navigation
- Interactive charts using Plotly
- Responsive design optimized for all screen sizes
- Real-time data updates
- Form validation with user-friendly error messages

---

## 📁 Project Structure

```
library_manager/
├── 📄 dashboard.py                 ⭐ Main Streamlit application (677 lines)
├── 📄 requirements.txt             📦 Python dependencies
├── 📄 README.md                    📖 Complete documentation (THIS FILE)
├── 📄 verify_setup.py              ✓ Pre-launch verification script
├── 📄 .gitignore                   ⚙️ Git configuration
│
├── src/                            💾 Backend modules (OOP Architecture)
│   ├── main.py                     CLI entry point & menu controller
│   ├── database.py                 Database connection & management
│   ├── books.py                    Book & BookManager classes (~120 lines)
│   ├── members.py                  Member & MemberManager classes (~180 lines)
│   ├── issue_return.py             BookTransaction class with penalty logic
│   ├── stats.py                    Statistics & Analytics classes
│   └── utils.py                    Helper functions & constants
│
└── sql/                            🗄️ Database Schema
    └── schema.sql                  4 normalized tables with sample data
```

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend Language** | Python | 3.7+ |
| **Web Framework** | Streamlit | 1.28.1+ |
| **Database** | MySQL | 5.7+ |
| **Data Processing** | Pandas | 2.1.3+ |
| **Visualization** | Plotly | 5.18.0+ |
| **DB Connector** | mysql-connector-python | 8.2.0+ |
| **Architecture** | OOP with Manager Pattern | - |

---

## 📋 Prerequisites

✅ **System Requirements:**
- Python 3.7 or higher
- MySQL Server 5.7+ (running)
- pip (Python package manager)
- 100 MB free disk space

✅ **Optional but Recommended:**
- Git for version control
- Command-line terminal/PowerShell

---

## 🚀 Quick Start (3 Commands)

```bash
# 1️⃣ Install dependencies
pip install -r requirements.txt

# 2️⃣ Initialize database (one time only)
mysql -u root -p project < sql/schema.sql

# 3️⃣ Run the dashboard
streamlit run frontend\app.py
```

**Dashboard opens at**: `http://localhost:8501`

---

## 📖 Detailed Installation & Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs 4 packages:
- `mysql-connector-python` - MySQL database driver
- `streamlit` - Web dashboard framework
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations

### Step 2: Setup MySQL Database

**Create Database:**
```bash
mysql -u root -p
```

Then paste:
```sql
CREATE DATABASE project;
USE project;
```

**Initialize Schema & Sample Data:**
```bash
mysql -u root -p project < sql/schema.sql
```

This creates 4 tables and loads sample data.

### Step 3: Configure Database Credentials

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

### Alternative: Run with Docker

Runs the dashboard and a MySQL 8.0 server together; no local MySQL install needed.

```bash
cp .env.example .env    # set DB_PASSWORD (keep DB_USER=root for Docker)
docker compose up --build
```

The dashboard is served at `http://localhost:8501`. Tables and sample data are created automatically on first start, and MySQL data persists in the `mysql_data` volume.

### Step 4: Verify Setup (Optional)

```bash
python verify_setup.py
```

This checks all prerequisites and reports any issues.

---

## 🎯 Running the Application

### Option 1: Web Dashboard (⭐ RECOMMENDED)

```bash
streamlit run dashboard.py
```

**What You Get:**
- Modern web interface
- Interactive charts and visualizations
- Form-based operations
- Real-time data updates
- Responsive design
- Automatic browser launch at `http://localhost:8501`

### Option 2: CLI Application (Terminal-based)

```bash
cd src
python main.py
```

**What You Get:**
- Text-based menu interface
- Command-line operations
- Good for automation/scripting
- No browser required

---

## 🌐 Dashboard Overview (5 Pages)

### 1️⃣ Dashboard Home 📊
**Purpose**: Overview and key metrics

**Contents:**
- **4 Metric Cards** (Big Numbers Display):
  - Total Books in Library
  - Total Registered Members
  - Currently Issued Books
  - Total Fines Collected
- **Recently Issued Books Table** - Last 10 transactions with:
  - Book name
  - Member name
  - Issue date
  - Return status

**Buttons/Controls:**
- Navigation sidebar (left)
- Page selector (top navigation)

---

### 2️⃣ Books Management 📚
**Purpose**: Add, view, and manage book inventory

**3 Tabs:**

#### Tab 1: View All Books
- **Displays**: Searchable table with all books
- **Columns**: Book ID, Title, Author, Genre, Price, Available Copies
- **Controls**:
  - View button for each book
  - Filter/Sort options

#### Tab 2: Add New Book
- **Form Fields**:
  - Book ID (text input)
  - Title (text input)
  - Author (text input)
  - Genre (dropdown/text)
  - Edition (text input)
  - ISBN (text input)
  - Quantity (number input)
  - Price (currency input)
- **Buttons**: Add Book, Reset Form
- **Validation**: All fields required, shows error messages
- **Success**: Confirmation message with book details

#### Tab 3: Delete Book
- **Selectbox**: Choose book to delete
- **Button**: Delete Book (with confirmation dialog)
- **Safety**: Shows book details before deletion
- **Feedback**: Success/error messages

**Layout**: Tabs at the top of the page, forms are centered and responsive

---

### 3️⃣ Members Management 👥
**Purpose**: Register, view, and manage library members

**3 Tabs:**

#### Tab 1: View All Members
- **Displays**: Table with all members
- **Columns**: Member ID, Name, DOB, Gender, Contact
- **Controls**:
  - Search by member ID or name
  - View details button
  - Status indicator (Active/Inactive/Suspended)

#### Tab 2: Register New Member
- **Form Fields** (Left Column):
  - Full Name (text input)
  - Email (email input)
  - Phone Number (text input)
  - Date of Birth (date picker)
- **Additional Fields** (Right Column):
  - Gender (radio buttons: Male/Female/Other)
  - Address (text area)
  - City (text input)
  - State (text input)
  - Pincode (text input)
  - Password (password input)
- **Auto-generated**: Member ID (format: ###L##)
- **Buttons**: Register Member, Reset Form
- **Validation**: Email format, phone length, required fields
- **Success**: Shows new member ID and confirmation

#### Tab 3: Change Member Status
- **Selectbox**: Select member from list
- **Radio Buttons**: Choose status
  - Active (green)
  - Inactive (gray)
  - Suspended (red)
- **Button**: Update Status
- **Display**: Current status before update

**Layout**: Clean two-column form layout, member ID auto-generated, status badges colored

---

### 4️⃣ Book Transactions 📤
**Purpose**: Issue and return books, track transactions

**3 Tabs:**

#### Tab 1: Issue Book
- **Form Fields**:
  - Member ID (dropdown with search)
  - Book Selection (dropdown - only available books)
  - Issue Date (date picker)
  - Days to Issue (number input - default 14)
- **Validation**:
  - Check member exists
  - Check book has available copies
  - Check member is active
- **Button**: Issue Book
- **On Submit**:
  - Decrements book stock
  - Creates transaction record
  - Shows confirmation with transaction ID

#### Tab 2: Return Book
- **Form Fields**:
  - Select Issued Book (dropdown of currently issued books)
  - Return Date (date picker)
- **Auto-Calculated Display**:
  - Days Kept (automatically calculated)
  - Penalty Amount (₹0 if on time, calculated if late)
  - Days Overdue (if applicable)
- **Button**: Process Return
- **On Submit**:
  - Increments book stock
  - Records return date
  - Updates penalty amount
  - Shows receipt with fine details

#### Tab 3: Transaction History
- **Displays**: Complete table of all transactions
- **Columns**: 
  - Book Name
  - Member Name
  - Issue Date
  - Return Date
  - Days Issued
  - Days Kept
  - Fine Amount
- **Filters**:
  - By date range (From/To dates)
  - By member (dropdown)
  - By book (dropdown)
  - By status (Returned/Pending)
- **Export**: Option to download as CSV

**Layout**: Forms in left sidebar or top section, transaction table below with filters

---

### 5️⃣ Statistics & Analytics 📈
**Purpose**: Visualize data and generate insights

**4 Tabs with Interactive Charts:**

#### Tab 1: Most Issued Books
- **Chart Type**: Horizontal Bar Chart
- **Shows**: Top 10 books by number of issues
- **Data**: Book title, number of issues
- **Colors**: Gradient from blue to purple
- **Interactions**: Hover for details, click to filter

#### Tab 2: Most Active Members
- **Chart Type**: Vertical Bar Chart
- **Shows**: Top 10 members by transaction count
- **Data**: Member name, transaction count
- **Colors**: Green to teal gradient
- **Interactions**: Hover for percentages

#### Tab 3: Best Selling Authors
- **Chart Type**: Pie Chart
- **Shows**: Author distribution
- **Data**: Author name, percentage of total issues
- **Colors**: Colorful segments
- **Interactions**: Click legend to toggle data

#### Tab 4: Currently Issued Books
- **Table**: Books currently with members
- **Columns**: 
  - Book Name
  - Member Name
  - Issue Date
  - Days Issued
  - Due Date
  - Overdue Status (color-coded)
- **Sorting**: By due date, issue date, or status
- **Highlights**: Overdue books in red background

**Layout**: Charts are interactive and responsive, tables are scrollable

---

## 🔧 Database Schema

### 4 Main Tables

#### 1. `book` Table
```sql
PRIMARY KEY: book_id (VARCHAR)
Columns:
- book_id: Unique book identifier
- book_name: Title of the book
- author: Author name
- genre: Book genre/category
- price: Book price (decimal)
- count: Available copies
```

#### 2. `member` Table
```sql
PRIMARY KEY: cust_id (VARCHAR)
Columns:
- cust_id: Member ID (auto-generated format: ###L##)
- cust_name: Full name
- DOB: Date of birth
- gender: Male/Female/Other
- contact: Phone number
```

#### 3. `member_details` Table
```sql
PRIMARY KEY: cust_id (VARCHAR, Foreign Key → member.cust_id)
Columns:
- cust_id: Links to member
- mail_id: Email address
- password: Login password
- status: Active/Inactive/Suspended
```

#### 4. `issue_and_return` Table
```sql
PRIMARY KEY: (book_id, cust_id, date_of_issue) - Composite Key
Foreign Keys:
- book_id → book.book_id
- cust_id → member.cust_id

Columns:
- book_id: Book borrowed
- cust_id: Member ID
- date_of_issue: Borrow date
- date_of_return: Return date (NULL if not returned)
- days_issued: Loan period requested
- days_kept: Actual days kept (NULL if not returned)
- penalty: Fine amount (₹0 if returned on time)
```

---

## 🎮 How to Use: Step-by-Step Examples

### Example 1: Add a New Book

1. Open dashboard: `streamlit run dashboard.py`
2. Navigate to **Books** page (click in sidebar)
3. Click **"Add New Book"** tab
4. Fill in the form:
   - Book ID: `B001`
   - Title: `The Great Gatsby`
   - Author: `F. Scott Fitzgerald`
   - Genre: `Fiction`
   - Edition: `1st`
   - ISBN: `978-0-7432-7356-5`
   - Quantity: `5`
   - Price: `299`
5. Click **"Add Book"** button
6. See success message with book details

---

### Example 2: Register a New Member

1. Navigate to **Members** page
2. Click **"Register New Member"** tab
3. Fill in the form:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Phone: `9876543210`
   - DOB: `1990-05-15`
   - Gender: `Male`
   - Address: `123 Main Street`
   - City: `Mumbai`
   - State: `Maharashtra`
   - Pincode: `400001`
   - Password: `secure_password`
4. Click **"Register"** button
5. See new Member ID: `123A45` (auto-generated)

---

### Example 3: Issue a Book

1. Navigate to **Transactions** page
2. Click **"Issue Book"** tab
3. Select:
   - Member ID: `123A45` (from dropdown)
   - Book: `The Great Gatsby` (from dropdown)
   - Issue Date: Today's date
   - Days to Issue: `14` (default)
4. Click **"Issue Book"** button
5. Book stock decreases by 1, transaction created

---

### Example 4: Return a Book

1. Navigate to **Transactions** page
2. Click **"Return Book"** tab
3. Select:
   - Issued Book: `The Great Gatsby - 123A45` (from dropdown)
   - Return Date: `2026-01-20` (today or later)
4. Auto-calculated:
   - Days Kept: 14 days
   - Penalty: ₹0 (if on time)
5. Click **"Process Return"** button
6. Book stock increases by 1, transaction closed

---

### Example 5: View Statistics

1. Navigate to **Statistics** page
2. Explore different tabs:
   - **Most Issued Books** - Bar chart of popular books
   - **Most Active Members** - Top borrowers
   - **Best Authors** - Pie chart by author
   - **Currently Issued** - Books out on loan

---

## 🔍 Frontend UI Design Details

### Navigation Structure
```
┌─────────────────────────────┐
│   📚 Library Management      │
│       System v2.1           │
├─────────────────────────────┤
│ SIDEBAR (Left):             │
├─────────────────────────────┤
│ ▢ Dashboard          📊      │
│ ▢ Books              📚      │
│ ▢ Members            👥      │
│ ▢ Transactions       📤      │
│ ▢ Statistics         📈      │
│                             │
│ ─────────────────────────── │
│ © LMS v2.1 | Streamlit      │
└─────────────────────────────┘
```

### Form Layout Pattern
```
┌─────────────────────────────────┐
│ Form Title (with icon)          │
├─────────────────────────────────┤
│ ┌─────────────┬─────────────┐   │
│ │ Field 1     │ Field 2     │   │
│ │ [input]     │ [input]     │   │
│ ├─────────────┴─────────────┤   │
│ │ Field 3 (full width)      │   │
│ │ [input]                   │   │
│ └─────────────────────────────┘   │
│                                   │
│ [Submit Button]  [Reset Button]   │
│                                   │
│ ✅ Success message (if any)      │
│ ❌ Error message (if any)        │
└─────────────────────────────────┘
```

### Data Table Pattern
```
┌──────────────────────────────────────────┐
│ Table Title                              │
├──────────────────────────────────────────┤
│ Col1      │ Col2      │ Col3  │ Actions  │
├───────────┼───────────┼───────┼──────────┤
│ Data1     │ Data2     │ Data3 │ Edit     │
│ Data1     │ Data2     │ Data3 │ Delete   │
│ ...       │ ...       │ ...   │ ...      │
├───────────┴───────────┴───────┴──────────┤
│ Total Records: X  [Export CSV]           │
└──────────────────────────────────────────┘
```

### Color Scheme
- **Primary**: Blue (#0066CC)
- **Success**: Green (#28A745)
- **Danger**: Red (#DC3545)
- **Warning**: Orange (#FFC107)
- **Info**: Light Blue (#17A2B8)
- **Pending**: Yellow (#FFC107)
- **Overdue**: Red (#DC3545)
- **Active**: Green (#28A745)
- **Inactive**: Gray (#6C757D)

---

## 🚨 Penalty Calculation Formula

```
Late Fee Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If (days_kept ≤ days_issued):
    penalty = ₹0 (returned on time)

If (days_kept > days_issued):
    days_overdue = days_kept - days_issued
    
    If (days_overdue ≤ 7):
        penalty = ₹100
    
    If (days_overdue > 7):
        penalty = ₹100 + (₹20 × (days_overdue - 7))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:
├─ Return on Day 14 (Days Issued: 14) → Penalty: ₹0 ✅
├─ Return on Day 17 (Days Issued: 14) → Penalty: ₹100 ⚠️
├─ Return on Day 21 (Days Issued: 14) → Penalty: ₹100 + (₹20×4) = ₹180 ⚠️
└─ Return on Day 30 (Days Issued: 14) → Penalty: ₹100 + (₹20×13) = ₹360 ❌
```

---

## 🔐 Security Features

### SQL Injection Prevention
- ✅ All queries use parameterized statements with `%s` placeholders
- ✅ User input is never directly concatenated into SQL
- ✅ Database driver handles escaping automatically

### Input Validation
- ✅ Email format validation
- ✅ Phone number format validation
- ✅ Date range validation
- ✅ Required field validation
- ✅ Unique ID checks (no duplicates)

### Data Protection
- ✅ Foreign key constraints enforce referential integrity
- ✅ Transaction rollback on errors
- ✅ Database connection pooling
- ✅ Password storage (hashed in production)

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip install -r requirements.txt
# or
pip install mysql-connector-python==8.2.0
```

### Issue: "Access denied for user 'root'@'localhost'"
**Solution:**
1. Check MySQL is running
2. Verify `DB_PASSWORD` in `.env`
3. Update credentials if changed
4. Restart MySQL service

### Issue: "Unknown database 'project'"
**Solution:**
```bash
mysql -u root -p project < sql/schema.sql
```

### Issue: "Streamlit not found"
**Solution:**
```bash
pip install streamlit==1.28.1
```

### Issue: "No module named 'src'"
**Solution:**
- Make sure you're running from the project root directory
- Don't run from inside the `src/` folder

### Issue: "Address already in use" (Port 8501)
**Solution:**
```bash
streamlit run dashboard.py --server.port 8502
```

### Issue: Charts/visualizations not loading
**Solution:**
```bash
pip install --upgrade plotly
streamlit cache clear
streamlit run dashboard.py
```

---

## 📚 Additional Resources

| Document | Purpose |
|----------|---------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet with common commands |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step setup checklist |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed configuration & troubleshooting |

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| Total Lines of Code | 3000+ |
| Backend Modules | 7 |
| Dashboard Pages | 5 |
| Database Tables | 4 |
| Features Implemented | 20+ |
| Documentation Files | 1 (consolidated) |
| Dependencies | 4 |

---

## 🎯 Next Steps

### Immediate
1. ✅ Run: `streamlit run dashboard.py`
2. ✅ Explore all 5 dashboard pages
3. ✅ Test adding books, members, and transactions

### Short Term (Optional Enhancements)
- [ ] Add book cover images
- [ ] Implement email notifications for overdue books
- [ ] Add PDF report generation
- [ ] Implement member profile photos
- [ ] Add advanced search/filters
- [ ] Create payment gateway integration for fines

### Medium Term (Future Roadmap)
- [ ] Mobile app interface
- [ ] Multi-user authentication
- [ ] Reservation system for books
- [ ] Rating and review system
- [ ] Recommendation engine
- [ ] Integration with online library networks

---

## 📧 Support & Feedback

For issues, questions, or feature requests:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for troubleshooting
2. Review database logs in `sql/schema.sql`
3. Verify all dependencies with `verify_setup.py`

---

## 📄 License

This project is created for educational and personal library management purposes.

---

## ✅ Checklist for First-Time Users

- [ ] Python 3.7+ installed
- [ ] MySQL Server installed and running
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database initialized: `mysql -u root -p project < sql/schema.sql`
- [ ] Database credentials set in `.env`
- [ ] Dashboard runs: `streamlit run dashboard.py`
- [ ] Can access: `http://localhost:8501`
- [ ] All 5 pages load without errors
- [ ] Can add a test book
- [ ] Can register a test member
- [ ] Can issue a book to a member
- [ ] Can return a book with penalty calculation
- [ ] Analytics page shows data visualizations

---

## 🎉 Congratulations!

Your Library Management System is ready to use. Start exploring the dashboard and managing your library efficiently!

**Happy Library Management! 📚**
cd src
python main.py
```

## 📖 Web Dashboard Usage

### Dashboard Pages

#### 🏠 **Dashboard Home**
- View key statistics: Total books, members, issued books, pending fines
- See recently issued books
- Quick overview of library status

#### 📚 **Books Management**
- **View All Books** - See complete book inventory with details
- **Add New Book** - Register new books with title, author, genre, price, quantity
- **Delete Book** - Remove books from the library

#### 👥 **Members Management**
- **View All Members** - Browse all registered members
- **Register New Member** - Add new members with personal details
- **Change Status** - Activate/deactivate/suspend member accounts

#### 📤 **Book Transactions**
- **Issue Book** - Lend books to members with specified return period
- **Return Book** - Accept returned books with automatic fine calculation
- **Transaction History** - View all past transactions

#### 📈 **Statistics & Analytics**
- **Most Issued Books** - Interactive bar chart showing popular books
- **Most Active Members** - Chart showing member activity levels
- **Best Selling Authors** - Pie chart of most borrowed authors
- **Currently Issued Books** - List of all books currently borrowed

## 💰 Penalty Calculation

Late return charges are calculated as follows:
- ✅ **No penalty** - If returned on time
- 📌 **₹100 flat** - If returned 1-7 days late
- 📈 **₹100 + ₹20/day** - For each day beyond 7 days

Example:
- Book due in 30 days, returned in 35 days (5 days late) → ₹100 penalty
- Book due in 30 days, returned in 45 days (15 days late) → ₹100 + (8 × ₹20) = ₹260 penalty

## 🗄️ Database Schema

### Tables

#### book
| Field | Type | Key |
|-------|------|-----|
| book_id | VARCHAR(10) | PRIMARY |
| book_name | VARCHAR(50) | - |
| author | VARCHAR(20) | - |
| genre | VARCHAR(10) | - |
| price | VARCHAR(7) | - |
| count | INT | - |

#### member
| Field | Type | Key |
|-------|------|-----|
| cust_id | INT | PRIMARY |
| cust_name | VARCHAR(20) | - |
| DOB | DATE | - |
| gender | CHAR(1) | - |
| contact | INT | - |

#### member_details
| Field | Type | Key |
|-------|------|-----|
| cust_id | INT | PRIMARY/FK |
| mail_id | VARCHAR(30) | - |
| password | VARCHAR(20) | - |
| status | VARCHAR(10) | - |

#### issue_and_return
| Field | Type | Key |
|-------|------|-----|
| book_id | VARCHAR(10) | FK |
| cust_id | INT | FK |
| date_of_issue | DATE | - |
| date_of_return | DATE | - |
| days_issued | INT | - |
| days_kept | INT | - |
| penalty | INT | - |

## 🏗️ Class Architecture

### Core Classes

**Database**
- Manages MySQL connections
- Executes queries
- Initializes database schema

**Book & BookManager**
- `Book`: Entity class representing a single book
- `BookManager`: Handles book operations (add, delete, display)

**Member & MemberManager**
- `Member`: Entity class representing a library member
- `MemberManager`: Handles member registration and status management

**BookTransaction**
- Handles book issue and return operations
- Calculates penalties automatically
- Updates book inventory

**Statistics**
- Generates library insights
- Shows most issued books, active members, best-selling authors
- Displays currently issued books

## 📝 Sample Data

The system comes with pre-loaded sample data:

**Books:**
- HP01JKR - Harry Potter and the Philosopher Stone (J.K. Rowling)
- PJ01RR - Percy Jackson and the Lightning Thief (Rick Riordan)

**Members:**
- 324J79 - Lakshya Gupta
- 268K04 - Devanshhi Dhingra

## 🔧 Configuration

### Environment Variables
All database settings come from a `.env` file in the root directory (see `.env.example`):
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=project
```

### Custom Settings
Modify constants in `src/utils.py`:
```python
SEPARATOR = "x----...-----x"  # Change visual separator
```

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Verify credentials in `.env`
- Check database name is correct

### Missing Dependencies
```bash
pip install --upgrade mysql-connector-python
```

### Permission Denied
- Run with administrator privileges
- Check file permissions in project folder

## 📚 Sample Use Cases

**Library Administrator**
1. Go to Books page → View all books
2. Add new books as they arrive
3. Monitor member status in Members page
4. Check statistics for popular books

**Library Member**
1. Register using Members page → Register New Member
2. Issue book at Transactions page → Issue Book
3. Return book at Transactions page → Return Book
4. View your transaction history

**Library Manager**
1. Monitor dashboard for key metrics
2. Review statistics to plan inventory
3. Check pending fines in Dashboard
4. Manage member accounts

## 🚀 Future Enhancements

- [ ] User authentication & login
- [ ] Email notifications for overdue books
- [ ] Fine payment tracking & receipts
- [ ] Advanced search and filtering
- [ ] Member portal with personal account
- [ ] Book reservation system
- [ ] QR code integration for books
- [ ] Database backup automation
- [ ] Admin role management
- [ ] Mobile app version
- [ ] PDF report generation
- [ ] SMS notifications

## 📄 License

This project is open source under the MIT License. See LICENSE file for details.

## 👨‍💻 Author

**Lakshya Gupta**

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 📌 Version History

**v2.1 - Dashboard Release**
- ✅ Added Streamlit web dashboard
- ✅ Interactive charts with Plotly
- ✅ Real-time statistics
- ✅ Enhanced UI/UX
- ✅ Responsive design

**v2.0 - OOP Refactoring**
- ✅ Restructured into OOP architecture
- ✅ Organized into src/ directory
- ✅ Separated concerns
- ✅ Comprehensive documentation

**v1.0 - Initial Release**
- ✅ CLI-based application
- ✅ MySQL backend
- ✅ Core library management features

---

**Ready to manage your library efficiently! 📚✨**
