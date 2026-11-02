
from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class Triage(BaseModel):
    category: Literal["billing", "shipping", "other"]
    priority: int = Field(ge=1, le=5)


def check(answer):
    try:
        return Triage.model_validate_json(answer)
    except ValidationError:
        return None


FORMAT = """Reply with one line of JSON and nothing else, like this:
{"category": "shipping", "priority": 3}
priority is 1 (can wait) to 5 (urgent)."""


BEFORE = """You sort customer support tickets for an online shop.

Categories:
- billing: payments, charges, refunds
- shipping: parcels, delivery, damaged boxes
- other: anything else

""" + FORMAT


AFTER = """You sort customer support tickets for an online shop.

Categories:
- billing: payments, charges, refunds, and any fee a customer is asked to pay, even at the door
- shipping: where a parcel is, late or lost deliveries, damaged boxes
- other: account changes, cancelling an order, anything else

""" + FORMAT


EXAMPLES = [
    {"role": "user", "content": "You took money from my card two times"},
    {"role": "assistant", "content": '{"category": "billing", "priority": 4}'},

    {"role": "user", "content": "Where is my delivery? It is a week late"},
    {"role": "assistant", "content": '{"category": "shipping", "priority": 3}'},

    {"role": "user", "content": "Can I change the email on my account?"},
    {"role": "assistant", "content": '{"category": "other", "priority": 2}'},
]


TICKETS = [
    ("I was charged twice for one order", "billing"),
    ("My parcel has not arrived", "shipping"),
    ("Can I get a refund for the blue mug?", "billing"),
    ("How do I change my password?", "other"),
    ("The parcel arrived but the box was crushed", "shipping"),
    ("The courier asked me to pay a delivery fee at the door", "billing"),
    ("I want to cancel my order before it ships", "other"),
]
