from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class BudgetItem(Base):
    __tablename__ = "budget_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    budget_id: Mapped[int] = mapped_column(
        ForeignKey("budgets.id", ondelete="CASCADE"),
        nullable=False
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)

    budget = relationship("Budget", back_populates="items")