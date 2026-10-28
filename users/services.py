from config.settings import STRIPE_API_KEY
import stripe


stripe.api_key = STRIPE_API_KEY

def create_stripe_price(amount):
    """Создает цену в страйпе."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Pay behind training"}
    )
    return price

def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url