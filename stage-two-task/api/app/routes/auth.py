#!/usr/bin/env python3
"""
Module for user registration
"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from utils.validate_data import validate_data
from models import DBStorage
from utils.auth_manager import AuthManager

auth = Blueprint('auth', __name__, url_prefix='/auth')


class Register(MethodView):
    """
    Class for user registeration
    """
    def post(self):
        """
        Registers a user
        """
        payload =  {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400
                }
        try:
            if request.content_type == "application/json":
                data = request.get_json()
                valid_data, is_valid = validate_data(data)  # returns escaped data and bool
                if not is_valid:
                    print('valid_data: ', valid_data)
                    res = jsonify(valid_data)
                    return res, 422
                try:
                    print('valid_data: ', valid_data)
                    with DBStorage() as session:
                        new_user = session.add_update_user(user_dict=valid_data, update=False)
                except Exception as exc:
                    print(f'exception occured during registration: {exc}')
                    return jsonify(payload), 400
                if new_user:
                    print('new_user: ', new_user)
                    token = AuthManager.gerenate_token(new_user)
                    payload.pop("statusCode", None)
                    payload["status"] = "success"
                    payload["message"] =  "Registration successful",
                    payload["data"] = {
                            "accessToken": token,
                            "user": new_user
                        }
                    return jsonify(payload), 201
            return jsonify(payload), 400
        except Exception as exc:
            print(f'Error in registering a new user" {exc}')
            return jsonify(payload), 400


class Login(MethodView):
    """
    Handles route for login
    """
    def post(self):
        """
        Handles post login request
        """
        payload = {
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }
        try:
            if request.content_type == "application/json":

                data = request.get_json()

                valid_data, is_valid = validate_data(data, reg=False)

                if valid_data and is_valid:
                    with DBStorage() as session:
                        user_valid = session.check_password(data)
                    if user_valid:
                        print('here:')
                        token = AuthManager.gerenate_token(user_dict=user_valid)
                        if token:
                            payload.pop("statusCode", None)
                            payload["status"] = "success"
                            payload["message"] =  "Login successful",
                            payload["data"] = {
                                    "accessToken": token,
                                    "user": user_valid
                                    }
                            return jsonify(payload), 200
        except Exception as exc:
            print(f'Error logging in user: {exc}')
            return jsonify(payload), 401

        print('auth error:')
        return jsonify(payload), 401



auth.add_url_rule('/register', view_func=Register.as_view('register'))
auth.add_url_rule('/login', view_func=Login.as_view('login'))
