from database.db import get_connection, initialize_database
from utils.api_client import fetch_books_from_open_library, APIError

class BookService:
    def __init__(self):
        initialize_database()
    
    def fetch_books_from_api(self, query="python programming", limit=10):
        try:
            books = fetch_books_from_open_library(query, limit)
            return books
        except APIError as e:
            raise
    
    def save_books_to_db(self, books):
        saved_count = 0
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            for book in books:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO books (title, author, publication_year, isbn)
                        VALUES (?, ?, ?, ?)
                    """, (
                        book.get('title'),
                        book.get('author'),
                        book.get('publication_year'),
                        book.get('isbn')
                    ))
                    saved_count += 1
                except Exception as e:
                    print(f"Error saving book: {e}")
            
            conn.commit()
        
        return saved_count
    
    def get_books_from_db(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, title, author, publication_year, isbn, created_at
                FROM books
                ORDER BY created_at DESC
            """)
            
            books = []
            for row in cursor.fetchall():
                books.append({
                    'id': row['id'],
                    'title': row['title'],
                    'author': row['author'],
                    'publication_year': row['publication_year'],
                    'isbn': row['isbn'],
                    'created_at': row['created_at']
                })
        
        return books
    
    def get_book_count(self):
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM books")
            return cursor.fetchone()[0]
    
    def search_books(self, search_term):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, title, author, publication_year, isbn, created_at
                FROM books
                WHERE title LIKE ? OR author LIKE ?
                ORDER BY title
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def clear_books(self):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM books")
            deleted = cursor.rowcount
            conn.commit()
            return deleted
    
    def fetch_and_store_books(self, query="python programming", limit=10):
        result = {
            'success': False,
            'fetched': 0,
            'saved': 0,
            'error': None
        }
        
        try:
            books = self.fetch_books_from_api(query, limit)
            result['fetched'] = len(books)
            
            saved = self.save_books_to_db(books)
            result['saved'] = saved
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result

if __name__ == "__main__":
    print("Testing BookService...")
    
    service = BookService()
    
    print("\n1. Fetching books from API...")
    result = service.fetch_and_store_books("artificial intelligence", limit=5)
    print(f"   Fetched: {result['fetched']}, Saved: {result['saved']}")
    
    print("\n2. Retrieving books from database...")
    books = service.get_books_from_db()
    for book in books:
        print(f"   - {book['title']} by {book['author']}")
