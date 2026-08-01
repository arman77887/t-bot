from typing import List, Dict


class ConversationMemory:

    def __init__(self, db):
        self.db = db

    def add_message(self, user_id, session_id, role, content):
        try:
            self.db.save_memory(
                user_id,
                session_id,
                role,
                content
            )
        except Exception:
            pass

    def get_context(
        self,
        user_id,
        session_id,
        limit=10
    ):

        try:
            return self.db.get_memory(
                user_id,
                session_id,
                limit
            )
        except Exception:
            return []

    def clear_history(
        self,
        user_id,
        session_id
    ):

        try:
            self.db.clear_memory(
                user_id,
                session_id
            )
        except Exception:
            pass

    def format_messages(
        self,
        messages: List[Dict]
    ):

        formatted = []

        for msg in messages:

            formatted.append(
                {
                    "role": msg["role"],
                    "content": msg["content"]
                }
            )

        return formatted
