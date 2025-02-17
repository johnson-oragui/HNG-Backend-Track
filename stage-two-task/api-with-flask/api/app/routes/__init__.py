#!/usr/bin/env python3
"""
Blueprints to be registered
"""


def register_routes(app):
    from api.app.routes.auth import auth
    from api.app.routes.dashboard import dashboard
    from api.app.routes.organisation import organisation

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(organisation)
