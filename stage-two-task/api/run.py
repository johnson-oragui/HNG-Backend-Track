#!/usr/bin/env python3
"""
Runs flask app
"""
from api.app import create_app

app_instance = create_app()

@app_instance.app.after_request
def after_request(response):
    """
    Sets header for no sniff
    """
    response.headers['X-Content-Type-Option'] = "nosnif"
    return response


if __name__ == '__main__':
    app_instance.app.run()
