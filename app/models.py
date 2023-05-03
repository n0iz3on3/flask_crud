import uuid
from typing import Type

from cachetools import cached
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy_utils import EmailType, UUIDType

import config


Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(37), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())


class Token(Base):

    __tablename__ = 'tokens'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', lazy='joined')


class Ads(Base):

    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=35), nullable=True, unique=False)
    description = Column(String(length=120), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', lazy='joined')


@cached({})
def get_engine():
    return create_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine())


def init_db():
    Base.metadata.create_all(bind=get_engine())


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[User] | Type[Token] | Type[Ads]
ORM_MODEL = User | Token | Ads
