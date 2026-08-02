from database import Database
from config import Config


class PaymentHandler:

    def __init__(self):
        self.db = Database()

    async def create_payment(
        self,
        user_id: int,
        plan: str
    ):

        plans = {
            "pro": Config.PRO_PRICE,
            "premium": Config.PREMIUM_PRICE,
            "enterprise": Config.ENTERPRISE_PRICE,
        }

        if plan not in plans:

            return {
                "success": False,
                "message": "Invalid plan."
            }

        amount = plans[plan]

        return {
            "success": True,
            "plan": plan,
            "amount": amount,
            "currency": Config.PREMIUM_CURRENCY,
            "payment_id": f"PAY-{user_id}-{plan}"
        }

    async def verify_payment(
        self,
        payment_id: str
    ):

        # এখানে পরে Stripe / SSLCommerz / LemonSqueezy
        # ইন্টিগ্রেশন করা হবে

        return True

    async def activate_premium(
        self,
        user_id: int
    ):

        self.db.set_premium(user_id, True)

        return True
