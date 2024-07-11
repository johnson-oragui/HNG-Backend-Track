#!/usr/bin/env python3
"""
User model creation
"""
import bcrypt
from sqlalchemy import String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from models.base import Base
from models.user_organisation import User_Organisation
from models.organisation import Organisation

class User(Base):
    """
    Class User that acts as the representation for user tables in the
    Database
    """
    # userId represents id for each user
    userId: Mapped[str] = mapped_column(
        String(60),
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False
        )
    # firstName represents the firstname of each user
    firstName: Mapped[str] = mapped_column(String(60), nullable=False)
    # lastName represents the lastname of each user
    lastName: Mapped[str] = mapped_column(String(60), nullable=False)
    # email represents the email of each user
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    # password represents the password of each user
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    # phone represents the phone of each user
    phone: Mapped[str] = mapped_column(String(40), nullable=True)

    # organisations represents the relationship between a user and his organisation(s)
    organisations: Mapped[list] = relationship("Organisation",
                                               secondary="user_organisations",
                                               back_populates="users")

    @staticmethod
    def set_password(plaintext_password: str):
        """
        Sets the password for the user, hashing it securely with bcrypt.
        """
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
        password = hashed_password.decode('utf-8')
        return password


# SQLAlchemy event listener to hash password before insert or update
@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password_before_insert_or_update(mapper, connection, target):
    """
    Hashes password before saving to the database
    """
    try:
        if target.password:
            hashed_pwd = User.set_password(target.password)

            target.password = hashed_pwd
            # print('target.password: ', target.password)
    except Exception as exc:
        print(f'An error occured: {exc}')
    finally:
        pass
        # print('end of transaction for password hashing!')

# SQLAlchemy event listener to create an organisation for a user after insert
@event.listens_for(User, 'after_insert')
def create_org_after_user_insert(mapper, connection, target):
    """
    create an organisation for a user after insert
    """
    if target.userId:
        # print('target.userId: ', target.userId)
        try:
            org_name = f"{target.firstName}'s Organisation"

            org_values = {
                "name": org_name,
                "description": f"{org_name} is One of a Kind.",
                }

            result = connection.execute(Organisation.__table__.insert().values(**org_values))

            org_id = result.inserted_primary_key[0]

            # Establish the relationship between the user and the organisation
            user_org_values = {
                "userId": target.userId,
                "orgId": org_id
            }

            connection.execute(User_Organisation.__table__.insert().values(**user_org_values))

        except Exception as exc:
            print(f'An error occcured! {exc}')
        finally:
            pass
            # print('end of trasanction for adding organisation!')
