from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.model import Base, id_key


class Product(Base):
    """Product table"""

    __tablename__ = 'product'

    id: Mapped[id_key] = mapped_column(init=False, comment='primary key')
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='product name')
    description: Mapped[str] = mapped_column(String(255), nullable=False, comment='product description')
    price: Mapped[float] = mapped_column(Float, nullable=False, comment='product price')
    external_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, comment='external id from external service'
    )
