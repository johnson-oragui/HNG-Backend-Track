#!/usr/bin/env python3
'''
Blueprint from flask for creating app blueprints
'''
from flask import Blueprint

views = Blueprint('views', __name__)

from . import hello
