from pathlib import Path
from database.db import get_connection, initialize_database
from utils.csv_reader import read_csv_file, read_csv_from_bytes, normalize_user_data, CSVError

class UserService:
    def __init__(self):
        initialize_database()
    
    def import_from_csv_file(self, file_path):
        result = {
            'success': False,
            'total_rows': 0,
            'imported': 0,
            'skipped': 0,
            'errors': [],
            'error': None
        }
        
        try:
            rows = read_csv_file(file_path, required_columns=['name', 'email'])
            result['total_rows'] = len(rows)
            
            users = normalize_user_data(rows)
            
            imported, skipped, errors = self._insert_users(users)
            
            result['imported'] = imported
            result['skipped'] = skipped
            result['errors'] = errors
            result['success'] = True
            
        except CSVError as e:
            result['error'] = f"CSV Error: {e}"
        except FileNotFoundError as e:
            result['error'] = f"File not found: {e}"
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
        
        return result
    
    def import_from_upload(self, file_content, filename="uploaded.csv"):
        result = {
            'success': False,
            'total_rows': 0,
            'imported': 0,
            'skipped': 0,
            'errors': [],
            'error': None
        }
        
        try:
            rows = read_csv_from_bytes(file_content, required_columns=['name', 'email'])
            result['total_rows'] = len(rows)
            
            users = normalize_user_data(rows)
            
            imported, skipped, errors = self._insert_users(users)
            
            result['imported'] = imported
            result['skipped'] = skipped
            result['errors'] = errors
            result['success'] = True
            
        except CSVError as e:
            result['error'] = f"CSV Error: {e}"
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
        
        return result
    
    def _insert_users(self, users):
        imported = 0
        skipped = 0
        errors = []
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            for user in users:
                try:
                    cursor.execute("""
                        INSERT INTO users (name, email, phone)
                        VALUES (?, ?, ?)
                    """, (
                        user.get('name'),
                        user.get('email'),
                        user.get('phone', '')
                    ))
                    imported += 1
                    
                except Exception as e:
                    if 'UNIQUE constraint' in str(e):
                        skipped += 1
                        errors.append(f"Duplicate email: {user.get('email')}")
                    else:
                        skipped += 1
                        errors.append(f"Error for {user.get('email')}: {e}")
            
            conn.commit()
        
        return imported, skipped, errors
    
    def get_all_users(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, email, phone, created_at
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = [dict(row) for row in cursor.fetchall()]
        
        return users
    
    def get_user_by_email(self, email):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, email, phone, created_at FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def search_users(self, search_term):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, email, phone, created_at
                FROM users
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY name
            """, (f'%{search_term}%', f'%{search_term}%'))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_user_count(self):
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
    
    def clear_users(self):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM users")
            deleted = cursor.rowcount
            conn.commit()
            return deleted
    
    def delete_user(self, user_id):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_statistics(self):
        count = self.get_user_count()
        
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM users WHERE phone IS NOT NULL AND phone != ''"
            )
            with_phone = cursor.fetchone()[0]
        
        return {
            'total_users': count,
            'with_phone': with_phone,
            'without_phone': count - with_phone
        }

if __name__ == "__main__":
    print("Testing UserService...")
    
    service = UserService()
    
    import tempfile
    import os
    
    test_csv = """name,email,phone
John Doe,john@example.com,555-1234
Jane Smith,jane@example.com,555-5678
Bob Johnson,bob@example.com,"""
    
    test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    test_file.write(test_csv)
    test_file.close()
    
    try:
        service.clear_users()
        
        print("\n1. Importing users from CSV...")
        result = service.import_from_csv_file(test_file.name)
        print(f"   Total rows: {result['total_rows']}")
        print(f"   Imported: {result['imported']}")
        
        print("\n2. All users:")
        users = service.get_all_users()
        for user in users:
            print(f"   - {user['name']} ({user['email']})")
            
    finally:
        os.unlink(test_file.name)
