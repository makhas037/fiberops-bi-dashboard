import os

class StripeService:
    """Placeholder Stripe integration.

    Fill in real Stripe SDK interaction when you provide STRIPE keys.
    """

    def __init__(self, secret_key: str | None = None):
        self.secret_key = secret_key or os.getenv("STRIPE_SECRET_KEY")

    def configured(self) -> bool:
        return bool(self.secret_key)

    def create_checkout_session(self, *args, **kwargs):
        raise NotImplementedError("Integrate the stripe SDK here")
