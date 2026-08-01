import sqlite3
import os
from config import Config


class Database:

    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.db = Config.DATABASE_NAME
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language TEXT,
            balance REAL DEFAULT 0,
            premium INTEGER DEFAULT 0,
            daily_used INTEGER DEFAULT 0,
            total_used INTEGER DEFAULT 0,
            referral_code TEXT,
            referred_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

    def register_user(
        self,
        user_id,
        username="",
        first_name="",
        last_name="",
        language="en",
        referred_by=None
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            user_id,
            username,
            first_name,
            last_name,
            language,
            referred_by
        )
        VALUES
        (
            ?,?,?,?,?,?
        )
        """, (
            user_id,
            username,
            first_name,
            last_name,
            language,
            referred_by
        ))

        conn.commit()
        conn.close()

    def get_user(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "user_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "language": row[5],
            "balance": row[6],
            "premium": bool(row[7]),
            "daily_used": row[8],
            "total_used": row[9],
            "referral_code": row[10],
            "referred_by": row[11],
            "created_at": row[12]
        }
