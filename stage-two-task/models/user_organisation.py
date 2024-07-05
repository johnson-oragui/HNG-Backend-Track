#!/usr/bin/env python3
"""
User_Organisation association model
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class User_Organisation(Base):
    """
    Class Organisation that acts as the representation for organisation tables in the
    Database
    """
    # userId represents the id of the user associated with the organisation
    userId: Mapped[str] = mapped_column(
        ForeignKey("users.userId"),
        primary_key=True,
        nullable=False
        )
    # orgId represents the id of the organisation associated with the user
    orgId: Mapped[str] = mapped_column(
        ForeignKey("organisations.orgId"),
        primary_key=True,
        nullable=False
        )
