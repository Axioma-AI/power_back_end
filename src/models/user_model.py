from sqlalchemy import Column, Integer, String, Boolean
from src.models.base_model import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    phone = Column(String(20))
    picture = Column(String(255))
    email_verified = Column(Boolean, default=False, nullable=False)
    country_code = Column(String(5))
