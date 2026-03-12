from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum


class RuleMatchType(str, enum.Enum):
    contains = "contains"
    regex = "regex"


class CategoryRule(Base):
    __tablename__ = "category_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    pattern: Mapped[str] = mapped_column(String(255), nullable=False)

    match_type: Mapped[RuleMatchType] = mapped_column(
        Enum(RuleMatchType),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False
    )