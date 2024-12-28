from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base_model import Base

class EncajeLegalModel(Base):
    __tablename__ = 'encaje_legal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    banco = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)
    subcategoria = Column(String(50), nullable=False)
    valor = Column(DECIMAL(20, 5), nullable=False)
    fecha_corte = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), nullable=False)

    # Relación con CategoryModel
    category = relationship("CategoryModel", back_populates="encajes")
