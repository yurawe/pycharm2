from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from models.model import Base


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)
