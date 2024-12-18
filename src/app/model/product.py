from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.model import Base, id_key


class Product(Base):
    """Product table"""

    __tablename__ = 'product'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    external_id: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
