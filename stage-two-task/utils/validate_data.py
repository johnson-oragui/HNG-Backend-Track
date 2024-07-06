#!/usr/bin/env pyth0n3
"""
Validate data from request
"""
from email_validator import validate_email, EmailNotValidError
import bleach

def validate_data(data: dict, reg=True):
    """
    Validates data from request

    Return:
        True on validation or False on invalidation
    """
    if reg:
        if "firstName" not in data or "lastName" not in data:
            return False
    if "email" not in data or "password" not in data:
        return False
    valid_email = is_valid_email(data.get('email'))
    if not valid_email:
        return False
    for key, value in data.items():
        if key == "password":
            continue
        data[key] = escape_input(value)

    return data


def is_valid_email(email):
    """
    Validates users emails
    """
    try:
        # Validate.
        v = validate_email(email)
        # Update with the normalized form.
        email = v["email"]
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False


def escape_input(data):
    """
    Escapes inputs from users
    """
    return bleach.clean(data)
