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
        payload = {
            "error": []
        }
        if not data["firstName"] or data["firstName"].strip() == '':
            detail1 = {"firstName": data['firstName'], "message": "firstName must not be empty"}
            payload["error"].append(detail1)
        if not data['lastName'] or data['lastName'].strip() == '':
            detail2 = {"lastName": data['lastName'], "message": "lastName must not be empty"}
            payload["error"].append(detail2)
        email_valid = is_valid_email(data.get('email'))
        if isinstance(email_valid, str):
            detail3 = {"email": data['email'], "message": email_valid}
            payload["error"].append(detail3)
        if not data['password'] or data['password'].strip() == '':
            detail4 = {"password": data['password'], "message": "password must not be empty"}
            payload["error"].append(detail4)
        if len(payload["error"]) > 0:
            return payload, False
        else:
            return data, True
    if not reg:
        if "email" not in data or "password" not in data:
            return '', False
        valid_email = is_valid_email(data.get('email'))
        if isinstance(valid_email, str):
            return '', False
        for key, value in data.items():
            if key == "password":
                continue
            data[key] = escape_input(value)

        return data, True


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
        return str(e)


def escape_input(data):
    """
    Escapes inputs from users
    """
    return bleach.clean(data)
