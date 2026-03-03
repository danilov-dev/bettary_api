from datetime import date, time

from sqlalchemy import Integer, String, Numeric, Date, Time
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.database import Base


class Cell(Base):
    __tablename__ = "cells"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, index=True)
    type: MappedColumn[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    barcode: MappedColumn[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    capacity: MappedColumn[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    time_charged: MappedColumn[time] = mapped_column(Time)
    time_discharged: MappedColumn[time] = mapped_column(Time)
    tested_at: MappedColumn[date] = mapped_column(Date, nullable=False)

