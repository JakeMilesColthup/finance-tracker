from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    items = relationship(
        "BudgetItem",
        back_populates="budget",
        cascade="all, delete-orphan"
    )