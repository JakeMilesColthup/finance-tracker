import re
from sqlalchemy.orm import Session
from app.models.category_rule import CategoryRule, RuleMatchType
from app.models.account import Account


class CategorizationService:

    @staticmethod
    def categorize(db: Session, description: str) -> Account | None:

        rules = db.query(CategoryRule).all()

        desc = description.upper()

        for rule in rules:

            if rule.match_type == RuleMatchType.contains:
                if rule.pattern.upper() in desc:
                    return db.get(Account, rule.account_id)

            elif rule.match_type == RuleMatchType.regex:
                if re.search(rule.pattern, desc):
                    return db.get(Account, rule.account_id)

        return None