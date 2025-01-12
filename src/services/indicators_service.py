import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from models.indicators_model import (
    LANGUAGE,
    IndicatorLang,
    Indicator,
    DataValue,
    Entity,
    EntityLang,
    TimePeriod
)
from schema.responses.indicators_responses import (
    IndicatorSearchResponseModel,
    IndicatorDetailsCustomResponseModel,
)
from utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)


class IndicatorsService:
    def search_indicators(self, query: str | None, limit: int, lang: LANGUAGE, db: Session):
        try:
            logger.info(
                f"Searching indicators with query: {query}, limit: {limit}, lang: {lang}")

            # Validar si el query está presente
            if query and len(query) > 0:
                # Usar `text` para el query con WITH
                sql_query = text("""
                    WITH limited_indicators AS (
                        SELECT indicator_id
                        FROM indicators_lang
                        WHERE MATCH (indicator_name, description) AGAINST (:query IN NATURAL LANGUAGE MODE)
                        LIMIT :limit
                    )
                    SELECT
                        indicators.indicator_id,
                        indicators.indicator_code,
                        indicators_lang.indicator_name,
                        indicators_lang.description,
                        indicators.data_count
                    FROM indicators
                    INNER JOIN indicators_lang ON indicators.indicator_id = indicators_lang.indicator_id
                    INNER JOIN limited_indicators ON indicators.indicator_id = limited_indicators.indicator_id
                    WHERE indicators_lang.lang = :lang
                    ORDER BY indicators.data_count DESC
                """)

                # Ejecutar el query
                result = db.execute(
                    sql_query, {"query": query, "limit": limit, "lang": str(lang)}).fetchall()
            else:
                # Si no hay query, ejecutar un query más simple
                stmt = (
                    select(
                        IndicatorLang.indicator_id,
                        Indicator.indicator_code,
                        IndicatorLang.indicator_name,
                        IndicatorLang.description,
                        Indicator.data_count,
                    )
                    .join(Indicator, IndicatorLang.indicator_id == Indicator.indicator_id)
                    .where(IndicatorLang.lang == str(lang))
                    .order_by(Indicator.data_count.desc())
                    .limit(limit)
                )
                result = db.execute(stmt).fetchall()

            # Formatear la respuesta
            indicators = [
                IndicatorSearchResponseModel(
                    id=row.indicator_id,
                    code=row.indicator_code,
                    name=row.indicator_name,
                    description=row.description,
                    data_count=row.data_count,
                )
                for row in result
            ]

            return indicators

        except Exception as e:
            logger.error(f"Error searching indicators: {e}")
            raise e

    def get_indicator_details(self, indicator_code: str, lang: LANGUAGE, db: Session):
        try:
            logger.info(f"Fetching details for indicator: {indicator_code}")
            stmt = (
                select(
                    Indicator.indicator_code,
                    IndicatorLang.indicator_name,
                    IndicatorLang.description,
                    Indicator.source,
                    Entity.entity_code,
                    EntityLang.entity_name,
                    EntityLang.entity_type,
                    DataValue.value,
                    TimePeriod.period_label,
                )
                .join(Indicator, IndicatorLang.indicator_id == Indicator.indicator_id)
                .join(DataValue, Indicator.indicator_id == DataValue.indicator_id)
                .join(Entity, DataValue.entity_id == Entity.entity_id)
                .join(EntityLang, DataValue.entity_id == EntityLang.entity_id)
                .join(TimePeriod, DataValue.period_id == TimePeriod.period_id)
                .where(EntityLang.entity_type.in_(["Country", "País"]))
                .where(Indicator.indicator_code == indicator_code)
                .where(IndicatorLang.lang == str(lang))
                .where(EntityLang.lang == str(lang))
            )
            result = db.execute(stmt).fetchall()

            logger.info(
                f"Found {len(result)} details for indicator: {indicator_code}")

            # Agrupar los datos por entidad
            entities_data = {}
            for row in result:
                entity_code = row.entity_code
                if entity_code not in entities_data:
                    entities_data[entity_code] = {
                        "entity_code": entity_code,
                        "entity_name": row.entity_name,
                        "entity_type": row.entity_type,
                        "values": []
                    }
                entities_data[entity_code]["values"].append({
                    "value": row.value,
                    "period": row.period_label
                })

            # Preparar los datos para el formato de respuesta
            indicator_details = {
                "indicator_code": result[0].indicator_code if result else "",
                "indicator_name": result[0].indicator_name if result else "",
                "indicator_desc": result[0].description if result else "",
                "source": result[0].source if result else "",
                "entities": [
                    {
                        "entity_code": entity_data["entity_code"],
                        "entity_name": entity_data["entity_name"],
                        "entity_type": entity_data["entity_type"],
                        "values": [
                            {"value": value["value"],
                                "period": value["period"]}
                            for value in entity_data["values"]
                        ]
                    }
                    for entity_data in entities_data.values()
                ]
            }

            # Retornar el modelo de respuesta personalizado
            return IndicatorDetailsCustomResponseModel(**indicator_details)

        except Exception as e:
            logger.error(f"Error fetching indicator details: {e}")
            raise e
