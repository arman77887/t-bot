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
    def update_daily_usage(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET daily_used = daily_used + 1,
                total_used = total_used + 1
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def reset_daily_usage(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET daily_used = 0
        """)

        conn.commit()
        conn.close()

    def get_daily_usage(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT daily_used FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:
            return row[0]

        return 0

    def is_premium(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT premium FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return bool(row[0]) if row else False

    def set_premium(self, user_id, status=True):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET premium=?
            WHERE user_id=?
        """, (1 if status else 0, user_id))

        conn.commit()
        conn.close()

    def get_balance(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return row[0] if row else 0

    def add_balance(self, user_id, amount):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET balance = balance + ?
            WHERE user_id=?
        """, (amount, user_id))

        conn.commit()
        conn.close()

    def deduct_balance(self, user_id, amount):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET balance = balance - ?
            WHERE user_id=?
        """, (amount, user_id))

        conn.commit()
        conn.close()
            def save_history(self, user_id, role, message):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        INSERT INTO history(user_id, role, message)
        VALUES(?,?,?)
        """, (user_id, role, message))

        conn.commit()
        conn.close()

    def get_history(self, user_id, limit=20):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT role,message
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return rows[::-1]

    def clear_history(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM history WHERE user_id=?",
            (user_id,)
        )

        conn.commit()
        conn.close()

    def get_total_users(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]

        conn.close()
        return total

    def get_total_premium(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE premium=1
        """)

        total = cursor.fetchone()[0]

        conn.close()
        return total

    def ban_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            ALTER TABLE users
            ADD COLUMN banned INTEGER DEFAULT 0
            """)
        except:
            pass

        cursor.execute("""
        UPDATE users
        SET banned=1
        WHERE user_id=?
        """, (user_id,))

        conn.commit()
        conn.close()

    def unban_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET banned=0
        WHERE user_id=?
        """, (user_id,))

        conn.commit()
        conn.close()

    def is_banned(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            SELECT banned
            FROM users
            WHERE user_id=?
            """, (user_id,))

            row = cursor.fetchone()
            conn.close()

            return bool(row[0]) if row else False

        except:
            conn.close()
            return False
