from database import Database


class HistoryHandler:

    def __init__(self):
        self.db = Database()

    async def save_chat(
        self,
        user_id: int,
        user_message: str,
        ai_response: str,
        model: str = "gemini"
    ):

        self.db.save_history(
            user_id,
            "user",
            user_message
        )

        self.db.save_history(
            user_id,
            "assistant",
            ai_response
        )

    async def get_user_history(
        self,
        user_id: int,
        limit: int = 20
    ):

        history = self.db.get_history(
            user_id,
            limit
        )

        result = []

        for role, message in history:

            result.append({
                "role": role,
                "message": message
            })

        return result

    async def delete_history(
        self,
        user_id: int
    ):

        self.db.clear_history(user_id)

        return True
