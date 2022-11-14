from sqlalchemy import Column, Integer, String

from db.db_setup import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(50), nullable=False)
