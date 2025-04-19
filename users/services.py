import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product


def create_stripe_price(product, amount):
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(amount * 100),  # Цены в Stripe указываются в копейках
        currency="usd",
    )
    return price


def create_checkout_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
