from datetime import date
from src.utils.convert import convert_nan_to_none

class EncajeLegalData:
    def __init__(self, categoria: str, subcategoria: str, valor: float, fecha_corte: date, reporte: str, fuente: str):
        self.categoria = convert_nan_to_none(categoria)
        self.subcategoria = convert_nan_to_none(subcategoria)
        self.valor = convert_nan_to_none(valor)
        self.fecha_corte = convert_nan_to_none(fecha_corte)
        self.reporte = convert_nan_to_none(reporte)
        self.fuente = convert_nan_to_none(fuente)

    def to_dict(self):
        return {
            "categoria": self.categoria,
            "subcategoria": self.subcategoria,
            "valor": float(self.valor) if self.valor is not None else None,
            "fecha_corte": self.fecha_corte.isoformat() if self.fecha_corte else None,
            "reporte": self.reporte,
            "fuente": self.fuente,
        }
