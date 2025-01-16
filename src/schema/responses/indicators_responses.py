from pydantic import BaseModel
from typing import List, Optional


class IndicatorSearchResponseModel(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    data_count: Optional[int]
    source: Optional[str]


class IndicatorDetailModel(BaseModel):
    entity: str
    indicator_code: str
    indicator_name: str
    description: Optional[str]
    source: Optional[str]
    value: Optional[float]
    period: Optional[str]


class IndicatorDetailsResponseModel(BaseModel):
    details: List[IndicatorDetailModel]


class IndicatorEntityValueModel(BaseModel):
    value: Optional[float]
    period: Optional[str]


class IndicatorEntityModel(BaseModel):
    entity_code: str
    entity_name: str
    entity_type: Optional[str]
    values: List[IndicatorEntityValueModel]


class IndicatorDetailsCustomResponseModel(BaseModel):
    indicator_code: str
    indicator_name: str
    indicator_desc: str
    source: str
    entities: List[IndicatorEntityModel]
