import datetime
from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, default=datetime.datetime.now)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    author = relationship("User")


class Vote(Base):
    __tablename__ = 'votes'
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), primary_key=True)
