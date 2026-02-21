import os
from dataclasses import dataclass, field

@dataclass
class DatabaseConfig:
    path: str = "books.db"
    timeout: int = 30
    
    def __post_init__(self):
        self.path = os.environ.get('DATABASE_PATH', self.path)

@dataclass
class APIConfig:
    open_library_base_url: str = "https://openlibrary.org"
    timeout: int = 30
    max_retries: int = 3
    
    def __post_init__(self):
        self.timeout = int(os.environ.get('API_TIMEOUT', self.timeout))

@dataclass
class AppConfig:
    app_name: str = "AI-ML Assignment"
    app_version: str = "1.0.0"
    debug: bool = False
    
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    
    def __post_init__(self):
        self.debug = os.environ.get('DEBUG', 'false').lower() == 'true'

config = AppConfig()

def get_config():
    return config

def get_database_path():
    return config.database.path

if __name__ == "__main__":
    print("Current Configuration:")
    print(f"  App Name: {config.app_name}")
    print(f"  Database Path: {config.database.path}")
