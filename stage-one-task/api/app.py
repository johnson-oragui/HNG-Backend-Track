#!/usr/bin/env python3
'''
views blueprint for routing
'''
from flask import Flask
from .views import views


app = Flask(__name__)
app.register_blueprint(views, url_prefix='/api/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
