import random
import string

from database import Database


class ReferralHandler:

    def __init__(self):
        self.db = Database()

    def generate_code(self, user_id: int):

        random_part = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        return f"REF{user_id}{random_part}"

    async def get_referral_stats(
        self,
        user_id: int
    ):

        user = self.db.get_user(user_id)

        if not user:
            return {
                "referral_code": "",
                "total_referrals": 0,
                "total_earned": 0
            }

        code = user.get("referral_code")

        if not code:

            code = self.generate_code(user_id)

            self.db.set_referral_code(
                user_id,
                code
            )

        total = self.db.get_total_referrals(code)

        earned = total * Config.REFERRAL_REWARD

        return {
            "referral_code": code,
            "total_referrals": total,
            "total_earned": earned
        }

    async def reward_referral(
        self,
        referral_code: str
    ):

        owner = self.db.get_user_by_referral_code(
            referral_code
        )

        if not owner:
            return False

        self.db.add_balance(
            owner["user_id"],
            Config.REFERRAL_REWARD
        )

        return True
