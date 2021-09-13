# -*- coding: utf-8 -*-
"""Module to declare all database types."""

from sqlalchemy import (
    Column,
    BigInteger, Boolean, DateTime, String, Text
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """Support agent which can reply to tickets."""
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    login = Column(String(32), unique=True, nullable=False)
    password = Column(String(32), unique=True, nullable=False)


class Ticket(Base):
    """Support ticket."""
    __tablename__ = "ticket"

    id = Column(String(64), primary_key=True)
    created = Column(DateTime, nullable=True)
    author = Column(String(64), nullable=False)
    opened = Column(Boolean, default=True, nullable=False)
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
