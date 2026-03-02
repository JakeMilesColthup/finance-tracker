from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum


class AccountType(str, enum.Enum):
    asset = "asset"
    liability = "liability"
    income = "income"
    expense = "expense"
    equity = "equity"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    subtype: Mapped[str] = mapped_column(String(255), nullable=True)