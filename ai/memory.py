from database import Database


class ConversationMemory:

    def __init__(self, db: Database):
        self.db = db

    def add_message(
        self,
        user_id: int,
        role: str,
        message: str
    ):

        self.db.save_history(
            user_id,
            role,
            message
        )

    def get_context(
        self,
        user_id: int,
        limit: int = 10
    ):

        history = self.db.get_history(
            user_id,
            limit
        )

        messages = []

        for role, message in history:

            messages.append(
                {
                    "role": role,
                    "content": message
                }
            )

        return messages

    def clear(
        self,
        user_id: int
    ):

        self.db.clear_history(user_id)
