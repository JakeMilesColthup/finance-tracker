from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category_rule import CategoryRule
from app.schemas.category_rule import CategoryRuleCreate, CategoryRuleRead

router = APIRouter(prefix="/category_rules", tags=["category_rules"])


@router.post("", response_model=CategoryRuleRead)
def create_rule(data: CategoryRuleCreate, db: Session = Depends(get_db)):

    rule = CategoryRule(
        pattern=data.pattern,
        match_type=data.match_type,
        account_id=data.account_id
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


@router.get("", response_model=list[CategoryRuleRead])
def list_rules(db: Session = Depends(get_db)):
    return db.query(CategoryRule).all()