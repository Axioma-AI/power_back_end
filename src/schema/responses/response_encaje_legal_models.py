from pydantic import BaseModel
from typing import List, Dict

class SubcategoriaValoresModel(BaseModel):
    subcategoria: str
    valores: List[float]  # Lista de valores asociados a la subcategoría

class SubcategoriaTotalModel(BaseModel):
    subcategoria: str
    valor_total: float  # Suma total por subcategoría

class CategoriaModel(BaseModel):
    categoria: str
    subcategorias: List[SubcategoriaValoresModel]  # Lista de subcategorías con sus valores

class CategoriaTotalModel(BaseModel):
    categoria: str
    subcategorias: List[SubcategoriaTotalModel]  # Totales por subcategoría

class EncajeLegalGroupedResponseModel(BaseModel):
    fuente: str
    reporte: str
    fecha_corte: Dict[str, List[CategoriaModel]]  # Agrupado por fecha, luego por categoría y subcategoría
    Total: Dict[str, List[CategoriaTotalModel]]  # Totales agrupados por categoría y subcategoría

    class Config:
        json_schema_extra = {
            "example": {
                "fuente": "Banco Central",
                "reporte": "encaje_legal",
                "fecha_corte": {
                    "2024-08-01": [
                        {
                            "categoria": "Depósitos",
                            "subcategorias": [
                                {"subcategoria": "Ahorros", "valores": [125000.50, 100000.00]}
                            ]
                        },
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Consumo", "valores": [85000.75]}
                            ]
                        }
                    ]
                },
                "Total": {
                    "2024-08-01": [
                        {
                            "categoria": "Depósitos",
                            "subcategorias": [
                                {"subcategoria": "Ahorros", "valor_total": 225000.50}  # Suma total
                            ]
                        },
                        {
                            "categoria": "Préstamos",
                            "subcategorias": [
                                {"subcategoria": "Consumo", "valor_total": 85000.75}
                            ]
                        }
                    ]
                }
            }
        }
