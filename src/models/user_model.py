from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text
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


class UserIndicatorFavorites(Base):
    __tablename__ = 'user_indicator_favs'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    indicator_id = Column(Integer, ForeignKey(
        'indicators.indicator_id'), primary_key=True)
    is_favorite = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
