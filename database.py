import sqlite3
from datetime import datetime
from config import Config


class Database:

    def __init__(self):
        self.db = Config.DATABASE_NAME
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db)

    def create_tables(self):

        conn = self.connect()
        cursor = conn.cursor()

        # Users
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
            premium_expire TEXT,
            daily_used INTEGER DEFAULT 0,
            total_used INTEGER DEFAULT 0,
            referral_code TEXT,
            referred_by TEXT,
            total_referrals INTEGER DEFAULT 0,
            total_earned REAL DEFAULT 0,
            total_spent REAL DEFAULT 0,
            banned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Chat History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Memory
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Payments
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            currency TEXT,
            method TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Referral
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter INTEGER,
            invited INTEGER,
            reward REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Settings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            user_id INTEGER PRIMARY KEY,
            model TEXT DEFAULT 'gemini',
            language TEXT DEFAULT 'en',
            image_provider TEXT DEFAULT 'openai'
        )
        """)

        conn.commit()
        conn.close()
          # ==========================
    # USER MANAGEMENT
    # ==========================

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

        referral_code = f"REF{user_id}"

        cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            user_id,
            username,
            first_name,
            last_name,
            language,
            referral_code,
            referred_by
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            user_id,
            username,
            first_name,
            last_name,
            language,
            referral_code,
            referred_by
        ))

        cursor.execute("""
        INSERT OR IGNORE INTO settings(user_id)
        VALUES(?)
        """, (user_id,))

        conn.commit()
        conn.close()

    def get_user(self, user_id):

        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return dict(row)

    def update_user_usage(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET
            daily_used = daily_used + 1,
            total_used = total_used + 1
        WHERE user_id=?
        """, (user_id,))

        conn.commit()
        conn.close()

    def reset_daily_usage(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET daily_used=0
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
        """, (
            1 if status else 0,
            user_id
        ))

        conn.commit()
        conn.close()

    def ban_user(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

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

        cursor.execute("""
        SELECT banned
        FROM users
        WHERE user_id=?
        """, (user_id,))

        row = cursor.fetchone()

        conn.close()

        return bool(row[0]) if row else False
          # ==========================
    # BALANCE
    # ==========================

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
        SET
            balance = balance + ?,
            total_earned = total_earned + ?
        WHERE user_id=?
        """, (
            amount,
            amount,
            user_id
        ))

        conn.commit()
        conn.close()

    def deduct_balance(self, user_id, amount):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET
            balance = balance - ?,
            total_spent = total_spent + ?
        WHERE user_id=?
        """, (
            amount,
            amount,
            user_id
        ))

        conn.commit()
        conn.close()

    # ==========================
    # HISTORY
    # ==========================

    def save_history(
        self,
        user_id,
        message,
        response,
        model
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO history
        (
            user_id,
            role,
            message,
            model
        )
        VALUES
        (
            ?,?,?,?
        )
        """, (
            user_id,
            "assistant",
            response,
            model
        ))

        conn.commit()
        conn.close()

    def get_history(self, user_id, limit=20):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
          # ==========================
    # REFERRAL
    # ==========================

    def add_referral(self, inviter, invited):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO referrals(inviter, invited)
        VALUES(?,?)
        """, (inviter, invited))

        cursor.execute("""
        UPDATE users
        SET total_referrals = total_referrals + 1
        WHERE user_id=?
        """, (inviter,))

        conn.commit()
        conn.close()

    def get_referral_stats(self, user_id):

        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            referral_code,
            total_referrals,
            total_earned
        FROM users
        WHERE user_id=?
        """, (user_id,))

        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)

        return {}

    # ==========================
    # PAYMENTS
    # ==========================

    def add_payment(
        self,
        user_id,
        amount,
        currency,
        method,
        status="pending"
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO payments(
            user_id,
            amount,
            currency,
            method,
            status
        )
        VALUES(?,?,?,?,?)
        """, (
            user_id,
            amount,
            currency,
            method,
            status
        ))

        conn.commit()
        conn.close()

    def update_payment_status(self, payment_id, status):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE payments
        SET status=?
        WHERE id=?
        """, (
            status,
            payment_id
        ))

        conn.commit()
        conn.close()

    # ==========================
    # USER SETTINGS
    # ==========================

    def get_settings(self, user_id):
