# AI-ML Assignment - AccuKnox

## 🚀 Live Demo

### **[Click Here to View Live App](https://accuknox-aiml-assignment.streamlit.app/)**

---

## About This Assessment

This is my submission for the AI/ML position assessment at AccuKnox. I've built a web application that covers all three problem statements mentioned in the assignment.

### What I Built

**Problem Statement 1** - The app has three main features:

1. **Books API Module** - Fetches book data from Open Library API, stores it in SQLite database, and displays it
2. **Student Scores Module** - Generates student test score data, calculates average and other stats, shows bar charts
3. **CSV Import Module** - Lets you upload a CSV file with user info and imports it into SQLite

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/VishalPandey1702/AI-ML-Assignment-AccuKnox-.git
cd AI-ML-Assignment-AccuKnox-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Project Structure

```
AI-ML-Assignment/
├── app.py                  # Main Streamlit app
├── config.py               # Config settings
├── requirements.txt        
│
├── database/
│   └── db.py               # SQLite connection and tables
│
├── services/
│   ├── book_service.py     # Books API logic
│   ├── student_service.py  # Student scores logic
│   └── user_service.py     # CSV import logic
│
├── utils/
│   ├── api_client.py       # HTTP client for API calls
│   └── csv_reader.py       # CSV parsing
│
└── data/
    └── users.csv           # Sample CSV file
```

---

## Tech Stack

- Python 3.x
- Streamlit (for the UI)
- SQLite (database)
- Requests (API calls)
- Pandas (data handling)

---

## Features Breakdown

### 1. Books API Module
- Search books using Open Library API
- Results get stored in SQLite
- Shows book title, author, year, ISBN
- Can clear database and fetch again

### 2. Student Scores Module
- Generates mock student test scores
- Calculates average, min, max scores
- Shows bar charts for scores by subject
- Lists top performing students

### 3. CSV Import Module  
- Upload any CSV with name and email columns
- Data gets inserted into SQLite
- Handles duplicate emails
- Search through imported users

---

## Assumptions I Made

- Used Open Library API since it's free and doesn't need API keys
- Student scores are generated randomly (no free student data API exists)
- CSV files should have at least 'name' and 'email' columns
- Duplicate books are handled by title + author combination
- Duplicate users are handled by email

---

## Problem Statement 2 Answers

The theoretical questions about LLM, Vector Databases, etc. are answered in the `PROBLEM_STATEMENT_2.md` file.

---

**Author:** Vishal Pandey  
**Assessment For:** AI/ML Position at AccuKnox
