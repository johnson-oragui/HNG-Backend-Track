#!/usr/bin/env python3
"""
Users Protected route
"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from utils.auth_manager import AuthManager
from models import DBStorage


dashboard = Blueprint('dashboard', __name__, url_prefix='/api/users')


class DashBoard(MethodView):
    """
    Class to handle user dashboard
    """
    @AuthManager.login_required(request=request)
    def get(self, id):
        """
        Handles a user record
        """
        # print('token valid, entered protected route.')
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        try:
            with DBStorage() as session:
                user = session.get('User', id)
            if user:
                payload = {
                    "status": "success",
                    "message": "Successful",
                    "data": user
                }
                return jsonify(payload), 200
            else:
                return jsonify(payload), 401
        except Exception as exc:
            print(f'error in users route: {exc}')
            return jsonify(payload), 401

dashboard.add_url_rule('/<string:id>', view_func=DashBoard.as_view("dashboard"))
