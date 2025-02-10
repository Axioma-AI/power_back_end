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
from sqlalchemy import func
import json

logger = setup_logger(__name__, level=logging.INFO)


class IndicatorsService:
    def search_indicators(self, query: str | None, limit: int, lang: LANGUAGE, db: Session):
        try:
            logger.info(
                f"Searching indicators with query: {query}, limit: {limit}, lang: {lang}")

            if query and len(query) > 0:
                sql_query = text("""
                    WITH matched_indicators AS (
                        SELECT DISTINCT i.indicator_id, i.indicator_code, il.indicator_name, 
                               il.description, i.data_count, i.source
                        FROM indicators i
                        INNER JOIN indicators_lang il ON i.indicator_id = il.indicator_id
                        WHERE il.lang = :lang
                        AND MATCH (il.indicator_name, il.description) AGAINST (:query IN NATURAL LANGUAGE MODE)
                        LIMIT :limit
                    ),
                    entity_counts AS (
                        SELECT 
                            dv.indicator_id,
                            dv.entity_id,
                            e.entity_code,
                            el.entity_name,
                            COUNT(*) as entity_data_count
                        FROM data_values dv
                        JOIN matched_indicators mi ON dv.indicator_id = mi.indicator_id
                        JOIN entities e ON dv.entity_id = e.entity_id
                        JOIN entities_lang el ON e.entity_id = el.entity_id
                        WHERE dv.value IS NOT NULL
                        AND el.lang = :lang
                        GROUP BY dv.indicator_id, dv.entity_id, e.entity_code, el.entity_name
                    )
                    SELECT 
                        mi.*,
                        (
                            SELECT JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'id', entity_id,
                                    'code', entity_code,
                                    'name', entity_name,
                                    'data_count', entity_data_count
                                )
                            )
                            FROM (
                                SELECT *
                                FROM entity_counts
                                WHERE indicator_id = mi.indicator_id
                                ORDER BY entity_data_count DESC
                                LIMIT 100
                            ) as sorted_entities
                        ) as entities_json
                    FROM matched_indicators mi
                """)
                result = db.execute(
                    sql_query, {"query": query, "limit": limit, "lang": str(lang)}).fetchall()
            else:
                sql_query = text("""
                    WITH base_indicators AS (
                        SELECT DISTINCT i.indicator_id, i.indicator_code, il.indicator_name,
                               il.description, i.data_count, i.source
                        FROM indicators i
                        INNER JOIN indicators_lang il ON i.indicator_id = il.indicator_id
                        WHERE il.lang = :lang
                        ORDER BY i.data_count DESC
                        LIMIT :limit
                    ),
                    entity_counts AS (
                        SELECT 
                            dv.indicator_id,
                            dv.entity_id,
                            e.entity_code,
                            el.entity_name,
                            COUNT(*) as entity_data_count
                        FROM data_values dv
                        JOIN base_indicators bi ON dv.indicator_id = bi.indicator_id
                        JOIN entities e ON dv.entity_id = e.entity_id
                        JOIN entities_lang el ON e.entity_id = el.entity_id
                        WHERE dv.value IS NOT NULL
                        AND el.lang = :lang
                        GROUP BY dv.indicator_id, dv.entity_id, e.entity_code, el.entity_name
                    )
                    SELECT 
                        bi.*,
                        (
                            SELECT JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'id', entity_id,
                                    'code', entity_code,
                                    'name', entity_name,
                                    'data_count', entity_data_count
                                )
                            )
                            FROM (
                                SELECT *
                                FROM entity_counts
                                WHERE indicator_id = bi.indicator_id
                                ORDER BY entity_data_count DESC
                                LIMIT 100
                            ) as sorted_entities
                        ) as entities_json
                    FROM base_indicators bi
                """)
                result = db.execute(
                    sql_query, {"limit": limit, "lang": str(lang)}).fetchall()

            indicators = [
                IndicatorSearchResponseModel(
                    id=row.indicator_id,
                    code=row.indicator_code,
                    name=row.indicator_name,
                    description=row.description,
                    data_count=row.data_count,
                    source=row.source,
                    entities=json.loads(
                        row.entities_json) if row.entities_json else []
                )
                for row in result
            ]

            return indicators

        except Exception as e:
            logger.error(f"Error searching indicators: {e}")
            raise e

    def get_indicator_details(self, indicator_code: str, entity_code: str, lang: LANGUAGE, db: Session):
        try:
            logger.info(
                f"Fetching details for indicator: {indicator_code}, entity: {entity_code}")

            result = (
                db.query(
                    Indicator.indicator_code,
                    IndicatorLang.indicator_name,
                    IndicatorLang.description,
                    Indicator.source,
                    Entity.entity_code,
                    EntityLang.entity_name,
                    EntityLang.entity_type,
                    DataValue.value,
                    TimePeriod.period_label
                )
                .join(IndicatorLang, Indicator.indicator_id == IndicatorLang.indicator_id)
                .join(DataValue, Indicator.indicator_id == DataValue.indicator_id)
                .join(Entity, DataValue.entity_id == Entity.entity_id)
                .join(EntityLang, Entity.entity_id == EntityLang.entity_id)
                .join(TimePeriod, DataValue.period_id == TimePeriod.period_id)
                .filter(Indicator.indicator_code == indicator_code)
                .filter(Entity.entity_code == entity_code)
                .filter(IndicatorLang.lang == str(lang))
                .filter(EntityLang.lang == str(lang))
                .filter(EntityLang.entity_type.in_(['Country', 'País']))
                .order_by(TimePeriod.start_year.asc())
                .all()
            )

            if not result:
                return None

            # Get the first row for indicator and entity details
            first_row = result[0]

            # Structure the response
            indicator_details = {
                "indicator_code": first_row.indicator_code,
                "indicator_name": first_row.indicator_name,
                "indicator_desc": first_row.description,
                "source": first_row.source,
                "entity": {
                    "entity_code": first_row.entity_code,
                    "entity_name": first_row.entity_name,
                    "entity_type": first_row.entity_type,
                    "values": [
                        {
                            "value": row.value,
                            "period": row.period_label
                        }
                        for row in result
                    ]
                }
            }

            return IndicatorDetailsCustomResponseModel(**indicator_details)

        except Exception as e:
            logger.error(f"Error fetching indicator details: {e}")
            raise e
