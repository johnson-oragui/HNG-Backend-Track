#!/usr/bin/env python3
"""
User model creation
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from models.base import Base
from models.user_organisation import User_Organisation

class User(Base):
    """
    Class User that acts as the representation for user tables in the
    Database
    """
    # userId represents id for each user
    userId: Mapped[str] = mapped_column(
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False
        )
    # firstName represents the firstname of each user
    firstName: Mapped[str] = mapped_column(nullable=False)
    # lastName represents the lastname of each user
    lastName: Mapped[str] = mapped_column(nullable=False)
    # email represents the email of each user
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    # password represents the password of each user
    password: Mapped[str] = mapped_column(nullable=False)
    # phone represents the phone of each user
    phone: Mapped[str]

    # organisations represents the relationship between a user and his organisation(s)
    organisations: Mapped[list] = relationship("Organisation", secondary="user_organisations")
