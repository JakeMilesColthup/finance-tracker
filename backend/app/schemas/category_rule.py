from pydantic import BaseModel, ConfigDict
from app.models.category_rule import RuleMatchType


class CategoryRuleCreate(BaseModel):
    pattern: str
    match_type: RuleMatchType
    account_id: int


class CategoryRuleRead(BaseModel):
    id: int
    pattern: str
    match_type: RuleMatchType
    account_id: int

    model_config = ConfigDict(from_attributes=True)