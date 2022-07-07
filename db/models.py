from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .database import Base


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
