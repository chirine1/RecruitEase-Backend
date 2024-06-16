import secrets
import string
import random

from collections import abc

def is_password_strong_enough(password: str) -> bool:

    SPECIAL_CHARACTERS = [
        "@",
        "#",
        "$",
        "%",
        "=",
        ":",
        "?",
        ".",
        "/",
        "|",
        "~",
        ">",
    ]

    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(
        char in SPECIAL_CHARACTERS for char in password
    ):
        return False

    return True


def gen_token() -> str:
    return secrets.token_urlsafe()


def generate_code(size=6, chars=string.digits):
    return "".join(
        random.choice(chars) for x in range(size)
    )



def is_iterable(attr):
  """Checks if an object is iterable using isinstance."""
  return isinstance(attr, abc.Iterable)
