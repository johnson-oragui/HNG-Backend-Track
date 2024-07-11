#!/usr/bin/env python3
"""
Create and configure flask app
"""
from flask import Flask
from api.config import Config
from api.app.routes import register_routes


class FLASKAPP:
    """
    Class that represents the flask app
    """
    def __init__(self, module_name) -> None:
        self.app = Flask(module_name)
        self.configure_app()
        self.url_rules()
        self.register_routes()


    def register_routes(self):
        """
        Register all blueprints to flask app
        """
        register_routes(self.app)

    def configure_app(self):
        """
        Cofigure app
        """
        self.app.config.from_object(Config)

    def url_rules(self):
        """
        Sets the rule for url mapping
        """
        self.app.url_map.strict_slashes = False

    def run(self):
        """
        Options for running the flask app
        """
        self.app.run(host="0.0.0.0", port=5000, threaded=True)


def create_app():
    """
    Creates an instance of FLASKAPP
    """
    app_instance = FLASKAPP(__name__)
    return app_instance
