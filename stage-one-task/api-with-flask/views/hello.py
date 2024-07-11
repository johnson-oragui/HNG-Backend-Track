#!/usr/bin/env python3
'''
views blueprint for routing
'''
from flask import request, make_response, jsonify, Response
from api.views import views
from api.utils.user_locate import user_locate


@views.get('/hello')
def hello() -> Response:
    '''
    Sends a greeting message using the client's ip address and

    Returns:
        Response:
            A response containing a defined message to the client
    '''
    if request.method == 'GET':
        # during deployment, when app is behind a proxy
        if request.headers.getlist('X-Forwarded-For'):
            user_ip = request.headers.getlist('X-Forwarded-For')[0]
            # contains comma seperated ip addresses
            # first ip is the client's ip
        else:
            # during development when app is not behind a proxy
            user_ip = request.remote_addr

        # retrieve path params
        name = request.args.get('visitor_name', 'Mark')
        # use user's ip to get his location and location weather
        location, country, temperature = user_locate(user_ip)
        if not location or not country or not temperature:
            message = {"error": "could not verify client IP"}
            res = make_response(jsonify(message))
            return res, 404

        greeting1 = f"Hello, {name}!, the temperature is"
        greeting2 = f"{temperature} degrees Celcius in {location}"
        # generate a message using the user_ip and location
        message = {
            "client_ip": user_ip,
            "location": location,
            "greeting": f'{greeting1} {greeting2}'
        }
        # create a response and parse the generated message
        response = make_response(jsonify(message))
        # return the response with a status code of 200
        return response, 200
    # if request is not GET
    else:
        # generate a error message
        msg = {"error": "Method not allowed"}
        # parse the error message to json
        response = make_response(jsonify(msg))
        # add a header of allowed METHOD
        response.headers['Allow'] = 'GET'
        # return the error message with 403 status code
        return response, 403
