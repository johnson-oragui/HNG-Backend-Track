#!/usr/bin/env python3
"""
Generate and Verify access token
"""
from os import getenv
import bcrypt
import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps

JWT_SECRET = getenv('JWT_SECRET')


class AuthManager:
    """
    Class to manage jwt tokens
    """
    @staticmethod
    def gerenate_token(user_dict: dict):
        """
        Generate token using email and id
        """
        try:
            payload = {
                "email": user_dict['email'],
                "exp": datetime.now() + timedelta(minutes=5),  #expiration time
                "iat": datetime.now()  # issued at
            }
            token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm="HS256")
            return token
        except Exception as exc:
            print(f'could not generate token: {exc}')

    @staticmethod
    def verify_jwt_token(token=None):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithm=['HS256'])
            return payload['email']
        except jwt.ExpiredSignatureError as exc:
            print(f'token expired: {exc}')
            return False
        except jwt.InvalidTokenError:
            print(f'token invalid: {exc}')
            return False
        except Exception as exc:
            print(f'error verifying token: {exc}')
            return False

    @staticmethod
    def login_required(request):
        def protected(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                Wrapper to validate access token
                """
                Authorization = request.headers.get('Authorization')
                print("Bearer: ", Authorization)
                try:
                    token = Authorization.split(' ')[1]
                    if token:
                        print('token: ', token)
                except Exception:
                    pass

                for ar in args:
                    print(ar)
                for kw in kwargs:
                    print(kw)
                return func(*args, **kwargs)
            wrapper.__qualname__ = func.__qualname__
            return wrapper
        return protected
