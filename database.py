import sqlite3
import os
from config import Config


class Database:

    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.db = Config.DATABASE_NAME
        self.create_tables()

    def connect(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):

        conn = self.connect()
        cursor = conn.cursor()

        # ==========================
        # USERS
        # ==========================

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

        # ==========================
        # HISTORY
        # ==========================

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

        # ==========================
        # MEMORY
        # ==========================

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

        # ==========================
        # PAYMENTS
        # ==========================

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

        # ==========================
        # REFERRALS
        # ==========================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter INTEGER,
            invited INTEGER,
            reward REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ==========================
        # SETTINGS
        # ==========================

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
        INSERT OR IGNORE INTO users(
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
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None

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

    def get_daily_usage(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT daily_used FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return row["daily_used"] if row else 0

    def reset_daily_usage(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET daily_used=0
        """)

        conn.commit()
        conn.close()

    def is_premium(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT premium FROM users WHERE user_id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return bool(row["premium"]) if row else False

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

        return bool(row["banned"]) if row else False

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

        return row["balance"] if row else 0

    def add_balance(self, user_id, amount):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET
            balance = balance + ?,
            total_earned = total_earned + ?
        WHERE user_id=?
        """, (amount, amount, user_id))

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
        """, (amount, amount, user_id))

        conn.commit()
        conn.close()

    # ==========================
    # HISTORY
    # ==========================

    def save_history(self, user_id, role, message, model="gemini"):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO history(
            user_id,
            role,
            message,
            model
        )
        VALUES(?,?,?,?)
        """, (
            user_id,
            role,
            message,
            model
        ))

        conn.commit()
        conn.close()

def get_history(self, user_id, limit=20):

    conn = self.connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, message
    FROM history
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()

    conn.close()

    return [(row["role"], row["message"]) for row in rows[::-1]]


def clear_history(self, user_id):

    conn = self.connect()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    # =====================
    # REFERRAL
    # ==========================

    def set_referral_code(self, user_id, code):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET referral_code=?
        WHERE user_id=?
        """, (code, user_id))

        conn.commit()
        conn.close()

    def get_user_by_referral_code(self, code):

        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE referral_code=?
        """, (code,))

        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None

    def get_total_referrals(self, referral_code):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE referred_by=?
        """, (referral_code,))

        total = cursor.fetchone()[0]

        conn.close()

        return total

    def add_referral(self, inviter, invited):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO referrals(
            inviter,
            invited
        )
        VALUES(?,?)
        """, (
            inviter,
            invited
        ))

        cursor.execute("""
        UPDATE users
        SET total_referrals = total_referrals + 1
        WHERE user_id=?
        """, (inviter,))

        conn.commit()
        conn.close()

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

    def update_payment_status(
        self,
        payment_id,
        status
    ):

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

    def get_total_balance(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT SUM(balance)
        FROM users
        """)

        row = cursor.fetchone()

        conn.close()

        return row[0] if row and row[0] else 0
          # ==========================
    # SETTINGS
    # ==========================

    def get_settings(self, user_id):

        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM settings
        WHERE user_id=?
        """, (user_id,))

        row = cursor.fetchone()

        conn.close()

        return dict(row) if row else None

    def update_settings(
        self,
        user_id,
        model=None,
        language=None,
        image_provider=None
    ):

        conn = self.connect()
        cursor = conn.cursor()

        if model:
            cursor.execute("""
            UPDATE settings
            SET model=?
            WHERE user_id=?
            """, (model, user_id))

        if language:
            cursor.execute("""
            UPDATE settings
            SET language=?
            WHERE user_id=?
            """, (language, user_id))

        if image_provider:
            cursor.execute("""
            UPDATE settings
            SET image_provider=?
            WHERE user_id=?
            """, (image_provider, user_id))

        conn.commit()
        conn.close()

    # ==========================
    # ADMIN
    # ==========================

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

    def get_all_users(self):

        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]
