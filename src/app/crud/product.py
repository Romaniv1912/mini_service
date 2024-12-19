from typing import Sequence

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from sqlalchemy_crud_plus import CRUDPlus

from src.app.model import Product
from src.app.schema.product import CreateProductParam, UpdateProductParam


class CRUDProduct(CRUDPlus[Product]):
    async def get(self, db: AsyncSession, pk: int) -> Product:
        """Get product by id"""
        return await self.select_model(db, pk)

    async def get_list(self, db: AsyncSession, *, offset: int = 0, limit: int = 20) -> Sequence[Product]:
        """
        Get product list

        :param db:
        :param offset:
        :param limit:
        :return:
        """
        stmt = select(self.model).order_by(desc(self.model.created_time)).offset(offset).limit(limit)

        query = await db.execute(stmt)

        return query.scalars().all()

    async def get_total(self, db: AsyncSession) -> int:
        """
        Get total count of product

        :param db:
        :return:
        """
        stmt = select(count(self.model.id))
        query = await db.execute(stmt)

        return query.scalar()

    async def create(self, db: AsyncSession, obj: CreateProductParam) -> Product:
        """
        Create new product

        :param db:
        :param obj:
        :return:
        """
        return await self.create_model(db, obj)

    async def add_or_update(self, db: AsyncSession, obj: CreateProductParam) -> Product:
        """
        Add or update product

        :param db:
        :param obj:
        :return:
        """

        row = await self.select_model_by_column(db, external_id=obj.external_id)

        if row is None:
            return await self.create(db, obj)

        await self.update_model(db, row.id, obj)

        return row

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
