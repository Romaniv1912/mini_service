from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from src.app.model import Product
from src.app.schema.product import CreateProductParam, UpdateProductParam


class CRUDProduct(CRUDPlus[Product]):
    async def get(self, db: AsyncSession, pk: int) -> Product:
        """Get product by id"""
        return await self.select_model(db, pk)

    def get_list(self) -> Select:
        """
        Get product select

        :return:
        """
        query = select(Product).order_by(desc(self.model.created_time))

        return query

    async def create(self, db: AsyncSession, obj: CreateProductParam) -> Product:
        """
        Create new product

        :param db:
        :param obj:
        :return:
        """
        return await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateProductParam) -> int:
        """
        Update product by id

        :param db:
        :param pk:
        :param obj:
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db, pk: int) -> int:
        """
        Delete product by id

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model(db, pk)


product_dao: CRUDProduct = CRUDProduct(Product)
