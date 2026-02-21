from database.db import get_connection, initialize_database
from utils.api_client import generate_mock_student_data

class StudentService:
    def __init__(self):
        initialize_database()
    
    def fetch_student_data(self):
        data = generate_mock_student_data()
        return data
    
    def save_student_data(self, students):
        saved_count = 0
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            for student in students:
                try:
                    cursor.execute("""
                        INSERT INTO students (name, subject, score)
                        VALUES (?, ?, ?)
                    """, (
                        student.get('name'),
                        student.get('subject'),
                        student.get('score')
                    ))
                    saved_count += 1
                except Exception as e:
                    print(f"Error saving student: {e}")
            
            conn.commit()
        
        return saved_count
    
    def get_student_data(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, subject, score, created_at
                FROM students
                ORDER BY name, subject
            """)
            
            students = [dict(row) for row in cursor.fetchall()]
        
        return students
    
    def calculate_average_score(self):
        with get_connection() as conn:
            cursor = conn.execute("SELECT AVG(score) FROM students")
            avg = cursor.fetchone()[0]
            return round(avg, 2) if avg else 0.0
    
    def calculate_statistics(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as count,
                    AVG(score) as average,
                    MIN(score) as min_score,
                    MAX(score) as max_score,
                    COUNT(DISTINCT name) as student_count,
                    COUNT(DISTINCT subject) as subject_count
                FROM students
            """)
            
            row = cursor.fetchone()
            
            stats = {
                'total_records': row['count'],
                'average_score': round(row['average'], 2) if row['average'] else 0,
                'min_score': row['min_score'],
                'max_score': row['max_score'],
                'unique_students': row['student_count'],
                'unique_subjects': row['subject_count']
            }
        
        return stats
    
    def get_scores_by_subject(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT subject, AVG(score) as avg_score
                FROM students
                GROUP BY subject
                ORDER BY avg_score DESC
            """)
            
            return {row['subject']: round(row['avg_score'], 2) 
                    for row in cursor.fetchall()}
    
    def get_scores_by_student(self):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT name, AVG(score) as avg_score
                FROM students
                GROUP BY name
                ORDER BY avg_score DESC
            """)
            
            return {row['name']: round(row['avg_score'], 2) 
                    for row in cursor.fetchall()}
    
    def get_top_performers(self, limit=5):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT name, AVG(score) as avg_score, COUNT(*) as subjects_taken
                FROM students
                GROUP BY name
                ORDER BY avg_score DESC
                LIMIT ?
            """, (limit,))
            
            return [
                {
                    'name': row['name'],
                    'average_score': round(row['avg_score'], 2),
                    'subjects_taken': row['subjects_taken']
                }
                for row in cursor.fetchall()
            ]
    
    def get_chart_data(self):
        return {
            'by_subject': self.get_scores_by_subject(),
            'by_student': self.get_scores_by_student(),
            'top_performers': self.get_top_performers()
        }
    
    def clear_students(self):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM students")
            deleted = cursor.rowcount
            conn.commit()
            return deleted
    
    def get_student_count(self):
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]
    
    def fetch_and_store_data(self):
        result = {
            'success': False,
            'fetched': 0,
            'saved': 0,
            'average_score': 0,
            'error': None
        }
        
        try:
            self.clear_students()
            
            data = self.fetch_student_data()
            result['fetched'] = len(data)
            
            saved = self.save_student_data(data)
            result['saved'] = saved
            
            result['average_score'] = self.calculate_average_score()
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result

if __name__ == "__main__":
    print("Testing StudentService...")
    
    service = StudentService()
    
    print("\n1. Fetching and storing student data...")
    result = service.fetch_and_store_data()
    print(f"   Fetched: {result['fetched']}, Saved: {result['saved']}")
    print(f"   Average Score: {result['average_score']}")
    
    print("\n2. Scores by Subject:")
    subject_scores = service.get_scores_by_subject()
    for subject, score in subject_scores.items():
        print(f"   {subject}: {score}")
