from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    urls = relationship("URL", back_populates="owner")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String)
    short_key = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    qr_code = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="urls")
