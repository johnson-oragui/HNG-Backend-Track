
#!/usr/bin/env python3
"""
Configurations for flask app
"""
from os import getenv
import dotenv

dotenv.load_dotenv()


class Config:
    """
    Class for app configurations.
    """
    DEBUG = True
    SECRET_KEY = getenv('APP_SECRET_KEY')
