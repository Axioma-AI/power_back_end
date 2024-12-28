from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    # Relación con EncajeLegalModel
    encajes = relationship("EncajeLegalModel", back_populates="category", cascade="all, delete-orphan")
