from sqlalchemy import (
    Column, String, Integer, ForeignKey, DECIMAL, Text, Enum as EnumDB, Index, Table
)
from src.models.base_model import Base
from enum import StrEnum


class LANGUAGE(StrEnum):
    EN = "EN",
    ES = "ES"


class Entity(Base):
    __tablename__ = "entities"
    entity_id = Column(Integer, primary_key=True)
    entity_code = Column(String(50), nullable=False)


class EntityLang(Base):
    __tablename__ = "entities_lang"
    entity_id = Column(Integer, ForeignKey(
        "entities.entity_id"), primary_key=True)
    lang = Column(String(2), primary_key=True)
    entity_name = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_extra_category = Column(String(50))


class DataCategory(Base):
    __tablename__ = "data_categories"
    category_id = Column(Integer, primary_key=True)
    category_name_en = Column(String(255), nullable=False)


class DataCategoryLang(Base):
    __tablename__ = "data_categories_lang"
    category_id = Column(Integer, ForeignKey(
        "data_categories.category_id"), primary_key=True)
    lang = Column(String(2), primary_key=True)
    category_name = Column(String(255), nullable=False)
    category_description = Column(Text)


class Indicator(Base):
    __tablename__ = "indicators"
    indicator_id = Column(Integer, primary_key=True)
    indicator_code = Column(String(50), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("data_categories.category_id"))
    unit_of_measurement = Column(String(100))
    data_count = Column(Integer)
    source = Column(String(100))


class IndicatorLang(Base):
    __tablename__ = "indicators_lang"
    indicator_id = Column(Integer, ForeignKey(
        "indicators.indicator_id"), primary_key=True)
    lang = Column(String(2), primary_key=True)
    indicator_name = Column(String(255), nullable=False)
    description = Column(Text)


class TimePeriod(Base):
    __tablename__ = "time_periods"
    period_id = Column(Integer, primary_key=True)
    start_date = Column(Integer)
    end_date = Column(Integer)
    start_month = Column(EnumDB('January', 'February', 'March', 'April', 'May',
                         'June', 'July', 'August', 'September', 'October', 'November', 'December'))
    end_month = Column(EnumDB('January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October', 'November', 'December'))
    start_year = Column(Integer)
    end_year = Column(Integer)
    period_label = Column(String(50))


class DataValue(Base):
    __tablename__ = "data_values"
    data_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.entity_id"))
    indicator_id = Column(Integer, ForeignKey("indicators.indicator_id"))
    period_id = Column(Integer, ForeignKey("time_periods.period_id"))
    value = Column(DECIMAL(20, 10))
