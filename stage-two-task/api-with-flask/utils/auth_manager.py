#!/usr/bin/env python3
"""
Generate and Verify access token
"""
from os import getenv
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify


load_dotenv()
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
            now = datetime.utcnow()
            payload = {
                "userId": user_dict['userId'],
                "iat": now,  # issued at
                "exp": now + timedelta(minutes=100),  #expiration time
            }

            token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm="HS256")
            return token
        except Exception as exc:
            print(f'could not generate token: {exc}')

    @staticmethod
    def verify_jwt_token(token=None):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload['userId']
        except Exception as exc:
            print(f'error verifying token: {exc}')
            return False

    @staticmethod
    def decode_token_without_validation(token):
        """
        For payload inspection
        """
        try:
            # Decode the token without signature verification to inspect the payload
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except jwt.InvalidTokenError as e:
            return {"error": str(e)}

    @staticmethod
    def login_required(request, org=False, single=False):
        def protected(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                Wrapper to validate access token
                """
                error_payload = {
                                "status": "Bad request",
                                "message": "Authentication failed",
                                "statusCode": 401
                                }
                Authorization = request.headers.get('Authorization')
                try:
                    token = Authorization.split(' ')[1]

                    if token:
                        userId = AuthManager.verify_jwt_token(token)
                        if not userId:
                            return jsonify(error_payload)

                        if org and not single:
                            args = args + (userId,)
                            return func(*args, **kwargs)
                        if org and single:
                            new_args = list(args)
                            new_args.append(userId)
                            tuple_args = tuple(new_args)
                            return func(*tuple_args, **kwargs)
                    else:
                        return jsonify(error_payload)
                except Exception as exc:
                    print(f'error getting token: {exc}')
                    return jsonify(error_payload)
                return func(*args, **kwargs)
            wrapper.__qualname__ = func.__qualname__
            return wrapper
        return protected
