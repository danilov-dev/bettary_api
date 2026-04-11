from datetime import date, time

from sqlalchemy import Integer, String, Numeric, Date, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cell(Base):
    __tablename__ = "cells"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    barcode: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    capacity: Mapped[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    time_charged: Mapped[time] = mapped_column(Time)
    time_discharged: Mapped[time] = mapped_column(Time)
    tested_at: Mapped[date] = mapped_column(Date, nullable=False)

    product_model_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_models.id"))
    product_model: Mapped["ProductModel"] = relationship(back_populates="cells")

    battery_id: Mapped[int] = mapped_column(Integer, ForeignKey("batteries.id"), nullable=True)
    battery: Mapped["Battery"] = relationship(back_populates="cells")

