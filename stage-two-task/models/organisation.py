#!/usr/bin/env python3
"""
Organisation model
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from models.base import Base
from models.user_organisation import User_Organisation

class Organisation(Base):
    """
    Class Organisation that acts as the representation for organisation tables in the
    Database
    """
    # orgId represents the id of each organisation
    orgId: Mapped[str] = mapped_column(
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
        nullable=False
        )
    # name represents the name of each organisation
    name: Mapped[str] = mapped_column(nullable=False)
    # description represents the description forf each organisation
    description: Mapped[str]

    # users represent the relationship between users and organisation(s)
    users: Mapped[list] = relationship("User", secondary="user_organisations")
