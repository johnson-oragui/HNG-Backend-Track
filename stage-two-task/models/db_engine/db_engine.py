#!/usr/bin/env python3
"""
The Engine for database operations and transactions
"""
from os import getenv
from dotenv import load_dotenv
import bcrypt
from functools import wraps
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
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

MODELS = {"User": User, "Organisation": Organisation, "User_Organisation": User_Organisation}

def check_all_attr(model):
    def check_attr(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for key in kwargs['user_dict'].keys():
                print('key: ', key)
                if not (hasattr(model, key)):
                    raise AttributeError(f"{model.__name__} does not has an attribute: {key}")
            return func(*args, **kwargs)
        wrapper.__qualname__ = func.__qualname__
        return wrapper
    return check_attr

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
            return self
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
        except SQLAlchemyError as exc:
            self.session.rollback()
            print(f'An error occured: {exc}')
        finally:
            if self.session:
                self.session.close()

    @check_all_attr(model=User)
    def add_update_user(self, user_id: str = '', user_dict: dict = {}, update: bool = False):
        """
        Handdles insertion into the users table
        """
        if user_dict is None or not isinstance(user_dict, dict):
            raise TypeError("user_dict must be a dictionary")
        if not user_dict['email'] or not user_dict['password']:
            raise ValueError("email and password are required fields")
        try:
            with self.Session() as session:
                if not update:
                    with session.begin():
                        email_exists = session.query(User).filter_by(email=user_dict.get('email')).one_or_none()
                        if email_exists:
                            print('\nuser_email already exists: ')
                            return

                        new_user = User(**user_dict)
                        session.add(new_user)
                        usr = new_user.__dict__.copy()
                        usr.pop('password', None)
                        usr.pop('_sa_instance_state', None)
                        return usr
                elif user_id and isinstance(user_id, str) and update:
                    with session.begin():
                        usr = session.query(User).filter_by(user_id=user_id).one_or_none()
                        if not usr:
                            print('\nuser does not exist: ')
                            return
                        for key, val in user_dict.items():
                            setattr(usr, key, val)
                else:
                    raise Exception('Method is only for update and insertion!')
        except SQLAlchemyError as exc:
            print(f'An error occured in add new user: {exc}')
        finally:
            print('end of transaction for add new user!')

    def get(self, model, model_id):
        """
        Retrieves a specific model
        """
        try:
            if model and not model_id:
                klass = MODELS.get(model)

                if klass:
                    with self.Session() as sess:
                        all_objects = sess.query(klass).all()
                        if all_objects:
                            return self.to_dict(all_objects)
            elif model and model_id and isinstance(model_id, str):

                klass = MODELS.get(model)

                if klass:
                    with self.Session() as sess:
                        if klass == User or klass == User_Organisation:
                            obj = sess.query(klass).filter_by(userId=model_id).one_or_none()
                        if klass == Organisation:
                            obj = sess.query(klass).filter_by(orgId=model_id).one_or_none()

                        if obj:
                            return self.to_dict(obj)
        except Exception as exc:
            print(f"error retrieving objects: {exc}")
            pass

    def to_dict(self, objs):
        """
        Returns a dictionary representation of objects
        """
        try:
            if objs and isinstance(objs, list):
                all_objs = []
                for ob in objs:
                    ob_copy = ob.__dict__.copy()
                    ob_copy.pop('password', None)
                    ob_copy.pop('_sa_instance_state', None)
                    all_objs.append(ob_copy)
                    return all_objs
            if objs:
                obj = objs.__dict__.copy()
                obj.pop('_sa_instance_state', None)
                obj.pop('password', None)
                return obj
        except Exception as exc:
            print(f'error converting objects to dict: {exc}')
            pass



    @check_all_attr(model=Organisation)
    def add_update_organisation(self, user_id: str = '', org_dict: dict = {}, update: bool = False):
        """
        Handdles insertion into the users table
        """
        if org_dict is None or not isinstance(org_dict, dict):
            raise TypeError("org_dict must be a dictionary")
        if not org_dict['name']:
            raise ValueError("organisation requires a name")
        try:
            with self.Session() as session:
                if not update:
                    with session.begin():
                        email_exists = session.query(User).filter_by(email=org_dict.get('email')).one_or_none()
                        if email_exists:
                            print('\nuser_email already exists: ')
                            return

                        new_user = User(**org_dict)
                        session.add(new_user)
                elif user_id and isinstance(user_id, str) and update:
                    with session.begin():
                        usr = session.query(User).filter_by(user_id=user_id).one_or_none()
                        if not usr:
                            print('\nuser does not exist: ')
                            return
                        for key, val in org_dict.items():
                            setattr(usr, key, val)
                else:
                    raise Exception('Method is only for update and insertion!')
        except SQLAlchemyError as exc:
            print(f'An error occured in add new user: {exc}')
        finally:
            print('end of transaction for add new user!')

    def check_password(self, data):
        """
        Checks if the provided password matches the hashed password stored for the user.
        Returns user data if the password matches, False otherwise.
        """
        try:
            with self.Session() as session:
                usr = session.query(User).filter_by(email=data['email']).one_or_none()
            if usr:
                usr = usr.__dict__.copy()
                usr.pop('_sa_instance_state', None)

                hashed: str = usr['password'].encode()
                plain_pwd: str = data['password'].encode()
                hashed_to_compare = bcrypt.hashpw(plain_pwd, bcrypt.gensalt())
                result = secrets.compare_digest(hashed_to_compare, hashed)
                if result:
                    usr.pop('password', None)
                    return usr
                else:
                    return result
        except Exception as exc:
            print(f'error in checking password: {exc}')

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
