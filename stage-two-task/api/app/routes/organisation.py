#!/usr/bin/env python3
"""
Organisations Protected route
"""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from utils.auth_manager import AuthManager
from utils.validate_data import escape_input
from models import DBStorage


organisation = Blueprint('organisation', __name__, url_prefix='/api/organisations')


class Organisations(MethodView):
    """
    Class to handle user dashboard
    """
    @AuthManager.login_required(request=request, org=True)
    def get(self, userId):
        """
        Handles a user record
        """
        print('handling all organisations for a single user...')
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        try:
            with DBStorage() as session:
                user_organisations = session.get("User_Organisation", userId)
                organisations = session.get('Organisation')

            if user_organisations:
                orgs_for_user_with_id = []
                for orgs in organisations:
                    for user_org in user_organisations:
                        if orgs['orgId'] == user_org['orgId']:
                            orgs_for_user_with_id.append(orgs)
                payload.pop("statusCode", None)
                payload["status"] = "success"
                payload["message"] = "Successfull"
                payload["data"] = {"organisations": orgs_for_user_with_id}
                return jsonify(payload), 200

        except Exception as exc:
            print(f'error in orgsnisations route: {exc}')
            return jsonify(payload), 400

        return jsonify(payload), 400

    @AuthManager.login_required(request=request, org=True)
    def post(self, userId):
        """
        Create new organization

        """
        print('handling creation of a single organisation for a single user...')
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        try:
            if request.content_type == "application/json":
                data: dict = request.get_json()
                for key, value in data.items():
                    data[key] = escape_input(value)
                if not (data['name'].strip() == '') and isinstance(data['name'], str):
                    if len(data) <= 2:
                        with DBStorage() as sess:
                            # create an organization with the data
                            orgId = sess.add_update_organisation(user_id=userId,
                                                                       org_dict=data)
                        if orgId:
                            data["orgId"] = orgId
                            data["description"] = data["description"] or ''
                            payload["status"] = "success"
                            payload["message"] = "Organisation created successfully"
                            payload.pop("statusCode", None)
                            payload["data"] = data

                            return jsonify(payload), 201

        except Exception as exc:
            print(f'cound not create new organization: {exc}')
            return jsonify(payload), 400
        return jsonify(payload)

class Organisation(MethodView):
    """
    Class to handle retriving a single organization
    """
    @AuthManager.login_required(request=request)
    def get(self, orgId):
        """
        Retrieves a single organisation
        """
        print('handling a single organisation for a single user...')
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        try:
            with DBStorage() as session:
                organisation = session.get('Organisation', model_id=orgId)

            if organisation:
                payload.pop("statusCode", None)
                payload["status"] = "success"
                payload["message"] = "Successfull"
                payload["data"] = organisation
                return jsonify(payload), 200

        except Exception as exc:
            print(f'error in orgsnisations route: {exc}')
            return jsonify(payload), 400

        return jsonify(payload), 400

    @AuthManager.login_required(request=request)
    def post(self, orgId):
        """
        Add a user to an existing organization
        """
        print('handling adding a single user to a single organisatio...')
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }
        try:
            if not isinstance(orgId, str):
                raise ValueError('orgId must be a string')
            orgId = escape_input(orgId)

            if request.content_type == "application/json":
                data = request.get_json()

                if "userId" in data and data["userId"] != None:
                    if isinstance(data["userId"], str) and len(data) == 1:
                        userId = escape_input(data["userId"])

                        with DBStorage() as sess:
                            user_org = sess.add_user_organization(orgId=orgId, userId=userId)
                        if user_org:
                            payload.pop("statusCode", None)
                            payload["status"] = "success"
                            payload["message"] = "User added to organisation successfully"
                            return jsonify(payload), 200
        except Exception as exc:
            print(f'could not add a user to an organisation: {exc}')
            return jsonify(payload), 400
        return jsonify(payload), 400


organisation.add_url_rule('/', view_func=Organisations.as_view("organisations"))
organisation.add_url_rule('/<string:orgId>', view_func=Organisation.as_view("organisation"))
# add a user to organisation
organisation.add_url_rule('/<string:orgId>/users', view_func=Organisation.as_view("user_organisation"))
