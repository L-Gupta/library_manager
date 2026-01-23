# Documentation Index

Welcome to the Library Management System documentation! This guide will help you navigate all available resources.

---

## 📚 Quick Navigation

### 🚀 Getting Started
- **New to the project?** Start with [README.md](../README.md) in the root directory
- **Want a quick setup?** See the 3-command Quick Start in README.md

### 💻 Frontend Development
- **Frontend setup & architecture**: [docs/FRONTEND.md](FRONTEND.md)
  - How to install and run Streamlit app
  - Page descriptions and features
  - Database helper functions
  - How to add new pages
  - Troubleshooting frontend issues

### 🗄️ Backend Development  
- **Backend setup & architecture**: [docs/BACKEND.md](BACKEND.md)
  - How to set up Python backend
  - Database schema and relationships
  - Class descriptions (Book, Member, etc.)
  - How to use backend functions
  - Troubleshooting backend issues

---

## 📁 Documentation Files

| File | Location | Purpose |
|------|----------|---------|
| **README.md** | Root | Complete project overview & features |
| **FRONTEND.md** | docs/ | Frontend setup, architecture, pages |
| **BACKEND.md** | docs/ | Backend setup, database, classes |
| **This File** | docs/ | Documentation index & navigation |

---

## 🎯 Choose Your Path

### I want to...

#### Run the Application
1. Read: [README.md](../README.md) Quick Start section
2. Follow: 3 simple commands to get running
3. Result: Web app opens at `http://localhost:8501`

#### Understand the Frontend
1. Read: [FRONTEND.md](FRONTEND.md) - Architecture section
2. Explore: pages/ folder structure
3. Learn: How Streamlit pages work
4. Modify: Add new features to frontend

#### Understand the Backend
1. Read: [BACKEND.md](BACKEND.md) - Architecture section
2. Explore: src/ folder structure
3. Learn: How database classes work
4. Modify: Add new backend features

#### Set Up Development Environment
1. For Frontend: [FRONTEND.md](FRONTEND.md) - Setup section
2. For Backend: [BACKEND.md](BACKEND.md) - Setup section
3. For Database: [BACKEND.md](BACKEND.md) - Database Schema section

#### Add a New Feature
1. **For UI**: [FRONTEND.md](FRONTEND.md) - Common Tasks section
2. **For Backend Logic**: [BACKEND.md](BACKEND.md) - Common Operations section
3. **For Database**: [BACKEND.md](BACKEND.md) - Tables Reference

#### Fix a Problem
1. **Frontend Issue**: [FRONTEND.md](FRONTEND.md) - Troubleshooting section
2. **Backend Issue**: [BACKEND.md](BACKEND.md) - Troubleshooting section
3. **Database Issue**: [BACKEND.md](BACKEND.md) - Database section

#### Deploy to Production
- Refer to [README.md](../README.md) - Technology Stack section
- Recommended: Streamlit Cloud for frontend
- Recommended: AWS RDS for MySQL database

---

## 📋 Project Structure

```
library_manager/
│
├── README.md                    # Main project documentation
│
├── docs/                        # Documentation folder
│   ├── INDEX.md                (THIS FILE)
│   ├── FRONTEND.md             Frontend guide
│   └── BACKEND.md              Backend guide
│
├── frontend/                    # Streamlit web application
│   ├── dashboard.py            Main entry point
│   ├── pages/                  Page modules
│   │   ├── dashboard.py
│   │   ├── books.py
│   │   ├── members.py
│   │   ├── transactions.py
│   │   └── statistics.py
│   └── utils/                  Utilities
│       ├── config.py           Settings
│       └── database_helpers.py Database queries
│
├── backend/                     Python backend
│   ├── src/                    Source code
│   │   ├── main.py             CLI entry point
│   │   ├── database.py         DB connection
│   │   ├── books.py            Book class
│   │   ├── members.py          Member class
│   │   ├── issue_return.py     Transactions
│   │   ├── stats.py            Analytics
│   │   └── utils.py            Helpers
│   └── sql/
│       └── schema.sql          Database schema
│
└── requirements.txt            Python dependencies
```

---

## 🔑 Key Concepts

### Frontend Stack
- **Framework**: Streamlit (web UI)
- **Language**: Python 3.7+
- **Database Connection**: mysql-connector-python
- **Visualization**: Plotly
- **Data**: Pandas DataFrames

### Backend Stack
- **Language**: Python 3.7+
- **Database**: MySQL 5.7+
- **Architecture**: Object-Oriented (classes)
- **Pattern**: Manager + Entity classes
- **Transactions**: MySQL transactions with rollback

### Database
- **Type**: MySQL relational database
- **Tables**: 4 (book, member, member_details, issue_and_return)
- **Relationships**: Foreign keys enforced
- **Queries**: Parameterized (SQL injection safe)

---

## 📊 Features Overview

### Book Management
- ✅ Add, view, delete books
- ✅ Track inventory (available copies)
- ✅ Search by title, author, genre
- ✅ Price and genre management

### Member Management
- ✅ Register members (auto-generates ID)
- ✅ View member details
- ✅ Change member status
- ✅ Track member history

### Transactions
- ✅ Issue books to members
- ✅ Return books with automatic fine calculation
- ✅ Complete transaction history
- ✅ Filter by book, member, or date

### Analytics
- ✅ Most issued books chart
- ✅ Most active members chart
- ✅ Best authors distribution
- ✅ Currently issued books
- ✅ Real-time statistics

---

## 🚀 Quick Reference

### Run Frontend
```bash
streamlit run frontend/dashboard.py
```

### Run Backend CLI
```bash
cd backend/src
python main.py
```

### Initialize Database
```bash
mysql -u root -p project < backend/sql/schema.sql
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔧 Troubleshooting Guide

| Issue | Solution | Docs |
|-------|----------|------|
| Streamlit won't start | Check Python version, install requirements | FRONTEND.md |
| Database connection error | Verify MySQL running, check credentials | BACKEND.md |
| Import errors | Check sys.path, verify backend location | FRONTEND.md |
| Penalty calculation wrong | Check penalty formula in utils.py | BACKEND.md |
| Page not loading | Check show() function, verify imports | FRONTEND.md |

---

## 📞 Support Resources

### For Frontend Issues
- Check: [FRONTEND.md - Troubleshooting](FRONTEND.md#troubleshooting)
- Look in: frontend/ folder
- Check: Streamlit console output

### For Backend Issues
- Check: [BACKEND.md - Troubleshooting](BACKEND.md#troubleshooting)
- Look in: backend/src/ folder
- Check: Python error messages

### For Database Issues
- Check: [BACKEND.md - Database Schema](BACKEND.md#database-schema)
- Verify: MySQL credentials
- Test: MySQL connection directly

---

## 🎓 Learning Path

### Beginner
1. Read: README.md (Overview)
2. Run: Frontend application
3. Explore: Dashboard and pages
4. Try: Add a book, register a member

### Intermediate
1. Read: FRONTEND.md (Architecture)
2. Read: BACKEND.md (Classes)
3. Modify: Add a new field to member form
4. Test: Verify changes work

### Advanced
1. Read: BACKEND.md (Database Schema)
2. Study: Code in src/ and pages/
3. Add: New page with custom query
4. Optimize: Database performance

---

## 📈 Development Guidelines

### Code Organization
- ✅ Frontend code goes in frontend/
- ✅ Backend code goes in backend/src/
- ✅ Database code goes in backend/sql/
- ✅ Documentation goes in docs/

### Adding Features
- **New UI**: Create pages/new_feature.py
- **New Logic**: Add to backend/src/
- **New Table**: Update backend/sql/schema.sql
- **New Docs**: Add to docs/ folder

### Best Practices
- ✅ Use parameterized SQL queries
- ✅ Add error handling
- ✅ Write descriptive comments
- ✅ Test thoroughly before commit
- ✅ Update documentation

---

## 🎯 Next Steps

### To Get Started
1. Read [README.md](../README.md) Quick Start
2. Run `streamlit run frontend/dashboard.py`
3. Explore the web interface

### To Develop
1. Read [FRONTEND.md](FRONTEND.md) for UI changes
2. Read [BACKEND.md](BACKEND.md) for logic changes
3. Follow Common Tasks sections

### To Troubleshoot
1. Find your issue in Troubleshooting sections
2. Follow the suggested solution
3. Check error messages for clues
4. Refer to relevant code sections

---

## 📚 Additional Resources

### Inside the Project
- Code comments in all files
- Docstrings in all functions
- README.md for project overview
- Schema.sql for database structure

### External Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [MySQL Docs](https://dev.mysql.com/doc/)
- [Python Docs](https://docs.python.org/)
- [Pandas Docs](https://pandas.pydata.org/docs/)

---

## ✅ Checklist for Starting

- [ ] Read README.md
- [ ] Install Python 3.7+
- [ ] Install MySQL
- [ ] Run: `pip install -r requirements.txt`
- [ ] Initialize database
- [ ] Configure credentials
- [ ] Run frontend: `streamlit run frontend/dashboard.py`
- [ ] Explore pages and features
- [ ] Read relevant docs (FRONTEND.md or BACKEND.md)
- [ ] Start developing!

---

## Summary

This documentation provides everything you need to:
- ✅ Understand the project architecture
- ✅ Set up your environment
- ✅ Run the application
- ✅ Add new features
- ✅ Fix problems
- ✅ Deploy to production

**Start with README.md, then dive into FRONTEND.md or BACKEND.md based on what you need!** 🚀

---

*Last Updated: January 20, 2026*  
*Version: 2.1*  
*Maintainer: Lakshya Gupta*
