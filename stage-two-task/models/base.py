#!/usr/bin/env python3
"""
Base Model for all models
"""
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    A Base class for all models to be mapped to the database
    """
    @declared_attr
    def __tablename__(cls):
        """
        Automatically Sets the table name based on the class name.
        """
        tablename = f"{cls.__name__.lower()}s"
        return tablename
