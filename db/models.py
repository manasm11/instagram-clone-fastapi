from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    posts = relationship("DbPost", back_populates="creator")


class DbPost(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(Enum("absolute", "relative"))
    caption = Column(String)
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("DbUser", back_populates="posts")
