# AI-ML Assignment

A production-style Python web application demonstrating REST API integration, SQLite database operations, data visualization, and CSV file processing.

## 🎯 Project Overview

This project addresses three key problem statements:

1. **API Data Retrieval and Storage** - Fetch books from Open Library API, store in SQLite, and display
2. **Data Processing and Visualization** - Generate student test scores, calculate statistics, and create visualizations
3. **CSV Data Import** - Read user data from CSV files and import into SQLite database

## 🏗 Architecture

```
┌─────────────────────────────────────────────┐
│              Streamlit UI (app.py)          │
├─────────────────────────────────────────────┤
│              Service Layer                   │
│  ┌─────────────┬────────────┬─────────────┐ │
│  │ BookService │StudentSvc  │ UserService │ │
│  └─────────────┴────────────┴─────────────┘ │
├─────────────────────────────────────────────┤
│              Database Layer                  │
│                (SQLite)                      │
├─────────────────────────────────────────────┤
│              Utilities                       │
│  ┌──────────────────┬─────────────────────┐ │
│  │   API Client     │    CSV Reader       │ │
│  └──────────────────┴─────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
AI-ML-Assignment/
│
├── app.py                  # Streamlit frontend application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── database/
│   ├── __init__.py
│   └── db.py               # Database connection & table management
│
├── services/
│   ├── __init__.py
│   ├── book_service.py     # Book-related operations
│   ├── student_service.py  # Student score operations
│   └── user_service.py     # User/CSV import operations
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py       # Reusable HTTP client
│   └── csv_reader.py       # CSV parsing utilities
│
├── data/
│   └── users.csv           # Sample CSV file
│
└── books.db                # SQLite database (auto-generated)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd AI-ML-Assignment
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:8501`

## 📚 Modules

### 1. Books API Module

- **API Source:** [Open Library API](https://openlibrary.org/developers/api)
- **Features:**
  - Search books by keyword (default: "python programming")
  - Store results in SQLite database
  - Display books with metadata (title, author, publication year, ISBN)
  - Show statistics (total books, unique authors, average publication year)

### 2. Student Scores Module

- **Data Source:** Mock data generator (realistic student test scores)
- **Features:**
  - Generate random but realistic student scores
  - Calculate comprehensive statistics (average, min, max, etc.)
  - Visualize scores by subject (bar chart)
  - Show top performers

### 3. CSV Import Module

- **Features:**
  - Upload CSV files with user data
  - Validate required columns (name, email)
  - Handle duplicate emails gracefully
  - Search imported users
  - Download sample CSV template

## 🛠 Technical Details

### Database Schema

```sql
-- Books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER,
    isbn TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, author)
);

-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Error Handling

- API retry mechanism with exponential backoff
- Database transaction management
- CSV validation with detailed error reporting
- User-friendly error messages in UI

### Logging

All operations are logged with timestamps for debugging:
```
2024-XX-XX HH:MM:SS - book_service - INFO - Fetching books for query: 'python'
```

## 🌐 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy!

### Deploy to Render

1. Create a `render.yaml`:
   ```yaml
   services:
     - type: web
       name: ai-ml-assignment
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port $PORT
   ```

2. Push to GitHub and connect Render

## 📝 Assumptions Made

1. **Books API:** Using Open Library API as it's free and doesn't require authentication
2. **Student Data:** Generated mock data since no reliable free API exists for student scores
3. **CSV Format:** Expects columns named `name` and `email` (case-insensitive)
4. **Database:** SQLite is sufficient for demonstration purposes
5. **Duplicate Handling:** Books are deduplicated by title+author; users by email

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_PATH` | Path to SQLite database file | `books.db` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `API_TIMEOUT` | API request timeout (seconds) | `30` |

## 🧪 Testing Individual Modules

```bash
# Test database setup
python -m database.db

# Test API client
python -m utils.api_client

# Test CSV reader
python -m utils.csv_reader

# Test services
python -m services.book_service
python -m services.student_service
python -m services.user_service
```

## 📊 Sample Output

### Books Module
| Title | Author | Year | ISBN |
|-------|--------|------|------|
| Learning Python | Mark Lutz | 2013 | 978-1449355739 |
| Python Crash Course | Eric Matthes | 2019 | 978-1593279288 |

### Student Scores Statistics
- **Average Score:** 78.5%
- **Highest Score:** 98.2%
- **Lowest Score:** 55.1%
- **Total Records:** 48

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is created for educational purposes as part of an AI/ML assessment.

---

**Author:** Vishal  
**Date:** 2024  
**Technologies:** Python, Streamlit, SQLite, Pandas, Requests
