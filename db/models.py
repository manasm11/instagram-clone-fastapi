from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    posts = relationship("DbPost", back_populates="creator")
    comments = relationship("DbComment", back_populates="creator")


class DbPost(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("DbUser", back_populates="posts")
    comments = relationship("DbComment", back_populates="post")


class DbComment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("DbPost", back_populates="comments")
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("DbUser", back_populates="comments")
