import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(product_name):
    """Создаем stripe продукт"""
    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product


def create_stripe_price(stripe_product_id):
    """ cоздаем цену stripe"""
    return stripe.Price.create(
      currency="usd",
      unit_amount=1000,
      product_data={"name": stripe_product_id},
    )


def create_stripe_session(price):
    """ cоздаем сессию stripe
     """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000",
        line_items=[{'price': price.get("id"), 'quantity': 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
