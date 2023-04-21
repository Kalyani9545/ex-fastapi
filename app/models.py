from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from typing import List
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default='TRUE', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    #many-to-one
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))

class User(Base):
    __tablename__="Users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String, nullable=False,unique=True)
    password=Column(String, nullable=False) 
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    posts: Mapped[List["Post"]] = relationship()
    phone_number=Column(String)

class Vote(Base):
    __tablename__ = "voting"
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)