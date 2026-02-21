import csv
import io

class CSVError(Exception):
    pass

def read_csv_file(file_path, required_columns=None, delimiter=','):
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            return _parse_csv(f, required_columns, delimiter)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    except UnicodeDecodeError as e:
        raise CSVError(f"Encoding error: {e}")

def read_csv_from_bytes(file_content, required_columns=None, delimiter=','):
    if isinstance(file_content, bytes):
        content = file_content.decode('utf-8')
    else:
        content = file_content.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
    
    return _parse_csv(io.StringIO(content), required_columns, delimiter)

def _parse_csv(file_obj, required_columns, delimiter):
    reader = csv.DictReader(file_obj, delimiter=delimiter)
    
    if reader.fieldnames is None:
        raise CSVError("CSV file appears to be empty")
    
    headers = list(reader.fieldnames)
    
    if required_columns:
        headers_lower = [h.lower().strip() for h in headers]
        missing = [col for col in required_columns if col.lower() not in headers_lower]
        if missing:
            raise CSVError(f"Missing required columns: {missing}")
    
    rows = []
    for row in reader:
        cleaned_row = {
            key.strip(): (value.strip() if value else '')
            for key, value in row.items()
            if key is not None
        }
        rows.append(cleaned_row)
    
    return rows

def normalize_user_data(rows):
    normalized = []
    
    name_columns = ['name', 'full_name', 'fullname', 'username']
    email_columns = ['email', 'email_address', 'e-mail', 'mail']
    phone_columns = ['phone', 'phone_number', 'telephone', 'mobile']
    
    for row in rows:
        user = {}
        
        for key, value in row.items():
            key_lower = key.lower().strip()
            
            if key_lower in name_columns and 'name' not in user:
                user['name'] = value
            elif key_lower in email_columns and 'email' not in user:
                user['email'] = value
            elif key_lower in phone_columns and 'phone' not in user:
                user['phone'] = value
        
        if 'name' in user and 'email' in user:
            if 'phone' not in user:
                user['phone'] = ''
            normalized.append(user)
    
    return normalized

if __name__ == "__main__":
    import os
    
    test_csv = """name,email,phone
John Doe,john@example.com,555-1234
Jane Smith,jane@example.com,555-5678"""
    
    test_file = "/tmp/test_users.csv"
    with open(test_file, 'w') as f:
        f.write(test_csv)
    
    print("Testing CSV reader...")
    users = read_csv_file(test_file, required_columns=['name', 'email'])
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
    
    os.remove(test_file)
