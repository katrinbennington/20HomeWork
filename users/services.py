import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """ cоздаем stripe продукт. """
    title_product = f"{instance.payed_course_or_lesson}"
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


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
