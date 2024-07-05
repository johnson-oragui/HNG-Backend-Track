#!/usr/bin/env python3
"""
The Engine for database operations and transactions
"""
from os import getenv
from dotenv import load_dotenv
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base
from models.user import User
from models.organisation import Organisation
from models.user_organisation import User_Organisation

# Parse a .env file and then load all the variables found as env variables.
load_dotenv()

# retrieve all environment variables for database connection
DB_USER = getenv('DB_USER')
DB_PWD = getenv('DB_PWD')
DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')

CON_STRING = f'mysql+mysqlconnector://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'


class DBStorage:
    """
    Class to handle table creation, database operations
    """
    def __init__(self) -> None:
        self.engine = create_engine(CON_STRING)

        self.session_factory = sessionmaker(bind=self.engine,
                                            autoflush=False,
                                            expire_on_commit=False)

        self.Session = scoped_session(self.session_factory)
        self.session = None

    def __enter__(self):
        """
        The entry point of DBStorage when used as a context manager
        """
        try:
            self.session = self.Session()
            return self.session
        except Exception as exc:
            print(f'An error occured: {exc}')

    def __exit__(self, exc_type, exc_val, traceback):
        """
        The exit point of DBStorage when used as a context manager
        """
        try:
            if exc_type:
                print(f'An error occured, exc_value: {exc_val}')
                self.session.rollback()
            else:
                self.session.commit()
        except Exception as exc:
            self.session.rollback()
            print(f'An error occured: {exc}')
        finally:
            if self.session:
                self.session.close()

    @staticmethod
    def check_password(plain_password, hashed_pass):
        """
        Checks if the provided password matches the hashed password stored for the user.
        Returns True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_pass.encode('utf-8'))

    def create_tables(self):
        """
        Creates all mapped models as tabales
        """
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """
        Creates all mapped models as tabales
        """
        Base.metadata.drop_all(self.engine)
