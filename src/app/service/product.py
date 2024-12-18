from fastapi import HTTPException
from sqlalchemy import Select

from src.app.crud.product import product_dao
from src.app.model import Product
from src.app.schema.product import CreateProductParam, UpdateProductParam
from src.database import async_db_session


class ProductService:
    @staticmethod
    async def get(*, pk: int) -> Product:
        async with async_db_session() as db:
            product = await product_dao.get(db, pk)
            if not product:
                raise HTTPException(404, 'Product not found')
            return product

    @staticmethod
    async def get_select() -> Select:
        return product_dao.get_list()

    @staticmethod
    async def create(*, obj: CreateProductParam) -> None:
        async with async_db_session.begin() as db:
            await async_db_session.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateProductParam) -> Product:
        async with async_db_session.begin() as db:
            await product_dao.update(db, pk, obj)

            product = await product_dao.get(db, pk)

        if not product:
            raise HTTPException(404, 'Product not found')

        return product

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            count = await product_dao.delete(db, pk)

        return count


product_service = ProductService()
