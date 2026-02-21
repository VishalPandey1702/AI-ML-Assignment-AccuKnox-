import requests
import time

DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

class APIError(Exception):
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def fetch_data(url, params=None, headers=None, timeout=DEFAULT_TIMEOUT):
    default_headers = {
        'Accept': 'application/json',
        'User-Agent': 'AI-ML-Assignment/1.0'
    }
    
    if headers:
        default_headers.update(headers)
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, headers=default_headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
                continue
            raise APIError(f"Request timed out after {timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
                continue
            raise APIError(f"Connection error: {e}")
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP error: {e}", status_code=response.status_code)
        except requests.exceptions.JSONDecodeError:
            raise APIError("Invalid JSON response")

def fetch_books_from_open_library(query="python programming", limit=10):
    url = "https://openlibrary.org/search.json"
    params = {
        'q': query,
        'limit': limit,
        'fields': 'title,author_name,first_publish_year,isbn'
    }
    
    data = fetch_data(url, params=params)
    
    books = []
    for doc in data.get('docs', [])[:limit]:
        book = {
            'title': doc.get('title', 'Unknown Title'),
            'author': doc.get('author_name', ['Unknown Author'])[0] if doc.get('author_name') else 'Unknown Author',
            'publication_year': doc.get('first_publish_year'),
            'isbn': doc.get('isbn', [None])[0] if doc.get('isbn') else None
        }
        books.append(book)
    
    return books

def generate_mock_student_data():
    import random
    
    students = [
        "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Ross",
        "Edward Chen", "Fiona Williams", "George Kumar", "Hannah Lee",
        "Ivan Petrov", "Julia Martinez", "Kevin O'Brien", "Laura Garcia"
    ]
    
    subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "English"]
    
    data = []
    for student in students:
        for subject in random.sample(subjects, k=random.randint(2, 4)):
            data.append({
                'name': student,
                'subject': subject,
                'score': round(random.uniform(55, 100), 2)
            })
    
    return data

if __name__ == "__main__":
    print("Testing Open Library API...")
    books = fetch_books_from_open_library("machine learning", limit=5)
    for book in books:
        print(f"  - {book['title']} by {book['author']} ({book['publication_year']})")
