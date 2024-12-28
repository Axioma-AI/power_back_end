import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from sqlalchemy.sql import distinct
from src.models.encaje_legal_model import EncajeLegalModel
from src.models.category_model import CategoryModel
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)

class EncajeLegalService:
    def __init__(self):
        self.reporte_name = "encaje_legal"

    def get_grouped_entries_by_date(self, db: Session):
        try:
            logger.info("Fetching and grouping records from 'encaje_legal' by the 3 most recent fecha_corte.")

            # Obtener las tres fechas de corte más recientes
            recent_dates = (
                db.query(EncajeLegalModel.fecha_corte)
                .distinct()
                .order_by(desc(EncajeLegalModel.fecha_corte))
                .limit(3)
                .all()
            )
            recent_dates = [date[0] for date in recent_dates]  # Extraer valores de las tuplas

            logger.info(f"Recent dates found: {recent_dates}")

            # Diccionario para agrupar resultados por fecha
            grouped_data = {}
            totals_data = {}

            # Consultar registros para las fechas seleccionadas
            records = (
                db.query(
                    EncajeLegalModel.categoria,
                    EncajeLegalModel.subcategoria,
                    EncajeLegalModel.valor,
                    EncajeLegalModel.fecha_corte,
                    CategoryModel.name.label("fuente")
                )
                .join(CategoryModel, EncajeLegalModel.category_id == CategoryModel.id)
                .filter(EncajeLegalModel.fecha_corte.in_(recent_dates))  # Filtrar por las fechas más recientes
                .order_by(desc(EncajeLegalModel.fecha_corte))
                .all()
            )

            # Procesar los registros obtenidos
            fuente_name = None
            for record in records:
                fecha = record.fecha_corte.isoformat()
                if not fuente_name:
                    fuente_name = record.fuente  # Configurar la fuente al primer valor encontrado

                if fecha not in grouped_data:
                    grouped_data[fecha] = []
                    totals_data[fecha] = {}

                # Agregar registro a grouped_data
                categoria_entry = next(
                    (entry for entry in grouped_data[fecha] if entry["categoria"] == record.categoria),
                    None
                )
                if not categoria_entry:
                    categoria_entry = {
                        "categoria": record.categoria,
                        "subcategorias": []
                    }
                    grouped_data[fecha].append(categoria_entry)

                # Buscar o crear subcategoría en grouped_data
                subcategoria_entry = next(
                    (sub for sub in categoria_entry["subcategorias"] if sub["subcategoria"] == record.subcategoria),
                    None
                )
                if not subcategoria_entry:
                    subcategoria_entry = {
                        "subcategoria": record.subcategoria,
                        "valores": []
                    }
                    categoria_entry["subcategorias"].append(subcategoria_entry)

                subcategoria_entry["valores"].append(float(record.valor))

                # Calcular totales agrupados por categoría y subcategoría
                categoria_totals = totals_data[fecha].get(record.categoria, {
                    "categoria": record.categoria,
                    "subcategorias": []
                })

                subcategoria_total = next(
                    (sub for sub in categoria_totals["subcategorias"] if sub["subcategoria"] == record.subcategoria),
                    None
                )
                if not subcategoria_total:
                    subcategoria_total = {
                        "subcategoria": record.subcategoria,
                        "valor_total": 0.0
                    }
                    categoria_totals["subcategorias"].append(subcategoria_total)

                subcategoria_total["valor_total"] += float(record.valor)
                totals_data[fecha][record.categoria] = categoria_totals

            # Convertir los totales a la estructura esperada
            formatted_totals = {
                fecha: list(categorias.values())
                for fecha, categorias in totals_data.items()
            }

            # Construir la respuesta final
            response = {
                "fuente": fuente_name if fuente_name else "N/A",
                "reporte": self.reporte_name,
                "fecha_corte": grouped_data,
                "Total": formatted_totals
            }

            logger.info(f"Successfully grouped records into {len(grouped_data)} unique dates.")
            return response

        except Exception as e:
            logger.error(f"Error grouping entries: {e}")
            raise e
