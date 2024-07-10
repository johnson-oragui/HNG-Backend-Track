import os
import jwt
import bcrypt
from datetime import datetime, timedelta
import bleach
from email_validator import validate_email
from user.models import User

def val_email(email):
    """
    Validate email
    """
    try:
        validate_email(email)
    except Exception as exc:
        return str(exc)

def escape_data(data: dict):
    """
    Escapes user data
    """
    try:
        for key, value in data.items():
            if key == 'password':
                continue
            data[key] = bleach.clean(value)
        return data
    except Exception as exc:
        print(f"could not escape data: {exc}")


def validate_data(data: dict, login=False):
    """
    Validates data
    """
    try:
        if login:
            email_valid = val_email(data.get('email', ''))
            if email_valid or not data.get('password', ''):
                return '', False
            else:
                data = escape_data(data)

                refined_data = {
                    "email": data['email'],
                    "password": data["password"],
                }
                return refined_data, True
        payload = {
            "errors": []
        }

        if not data.get('firstName', '').strip() or len(data.get('firstName', '')) <= 2:
            f_name_error = {
                "firstName": data.get('firstName', ''),
                "message": "firstName must not be empty or less than two characters",
            }
            payload['errors'].append(f_name_error)

        if not data.get('lastName', '').strip() or len(data.get('lastName', '')) <= 2:
            l_name_error = {
                "lastName": data.get('lastName', ''),
                "message": "lastName must not be empty or less than two characters",
            }
            payload['errors'].append(l_name_error)

        email_valid = val_email(data.get('email', ''))
        if email_valid:
            email_error = {"email": data.get('email', ''), "message": email_valid}
            payload['errors'].append(email_error)

        if not data.get('password', '').strip() or len(data.get('password', '')) <= 6:
            passwd_error = {"password": data.get('password', ''),
                            "message": "password must not be empty or less than 6 chars."}
            payload['errors'].append(passwd_error)

        if len(payload['errors']) > 0:
            return payload, False
        else:
            data = escape_data(data)
            return data, True
    except Exception as exc:
        print(f"could not validate data: {exc}")
        return payload, False

def create_user(data):
    """
    Creates a user
    """
    try:
        new_user = User.objects.create(**data)
        new_user = new_user.__dict__.copy()
        new_user.pop('password', None)
        new_user.pop('_state', None)
        new_user.pop('created_at', None)
        new_user.pop('updated_at', None)
        return new_user
    except Exception as exc:
        print(f'error creating user: {exc}')

def check_user(data: dict):
    """
    Check for user and compare password
    """
    try:
        user = User.objects.get(email=data['email'])
        if user:
            user = user.__dict__.copy()
            hashed_pwd = user.get('password')
            is_valid = compare_password(data['password'], hashed_pwd)
            if is_valid:
                user.pop('password', None)
                user.pop('_state', None)
                user.pop('created_at', None)
                user.pop('updated_at', None)
                return user
            else:
                return
        else:
            return
    except Exception as exc:
        print(f'could not retrieve user: {exc}')

def compare_password(plain_pwd: str, hashed: str):
    """
    compare password before Authentication
    """
    try:
        is_valid = bcrypt.checkpw(plain_pwd.encode(), hashed.encode())

        return is_valid
    except Exception as exc:
        print(f'error comparing password: {exc}')

def generate_token(data: dict):
    """
    Generate token for user registration or login
    """
    SECRET = os.getenv('JWT_SECRET')
    try:
        email = data.get('email')
        user_id = data.get('id')

        now = datetime.utcnow()

        payload = {
            "email": email,
            "user_id": user_id,
            "iat": now,
            "exp": now + timedelta(days=10)
        }
        token = jwt.encode(payload=payload, key=SECRET, algorithm="HS256")

        return token
    except Exception as exc:
        print(f'error generating jwt: {exc}')

def verify_token(token: str):
    """
    Verify token for user authorization
    """
    SECRET = os.getenv('JWT_SECRET')
    try:
        payload: dict = jwt.decode(jwt=token, key=SECRET, algorithms=['HS256'])
        email = payload.get('email')
        user_id = payload.get('user_id')
        return (email, user_id)
    except Exception as exc:
        print(f'error verifying jwt: {exc}')
