from datetime import date, time
from typing import List

from sqlalchemy import Integer, String, Numeric, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Battery(Base):
    __tablename__ = "batteries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    barcode: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    capacity: Mapped[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    time_charged: Mapped[time] = mapped_column(Time)
    time_discharged: Mapped[time] = mapped_column(Time)
    tested_at: Mapped[date] = mapped_column(Date, nullable=False)

    cells: Mapped[List["Cell"]] = relationship(back_populates="battery")