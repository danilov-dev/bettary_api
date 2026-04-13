import enum
from typing import List

from sqlalchemy import Integer, String, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class ProductTypes(enum.Enum):
    BATTERY = "battery"
    CELL = "cell"


class ProductModel(Base):
    __tablename__ = "product_models"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    type: Mapped[ProductTypes] = mapped_column(Enum(ProductTypes), nullable=False)

    voltage: Mapped[float] = mapped_column(Float, nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)

    height: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)

    batteries: Mapped[List["Battery"]] = relationship(back_populates="product_model")
    cells: Mapped[List["Cell"]] = relationship(back_populates="product_model")
