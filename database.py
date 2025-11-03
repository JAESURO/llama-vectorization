import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("users.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()
        
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
        
    def register_user(self, username: str, password: str) -> bool:
        try:
            password_hash = self.hash_password(password)
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (username, password_hash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
            
    def authenticate_user(self, username: str, password: str) -> bool:
        password_hash = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                          (username, password_hash))
        return self.cursor.fetchone() is not None