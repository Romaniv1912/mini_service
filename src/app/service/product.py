import asyncio

from typing import Annotated, List, Sequence, Tuple

from fastapi import HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.product import product_dao
from src.app.model import Product
from src.app.schema.product import CreateProductParam, UpdateProductParam
from src.common.schema import GetPageParams
from src.database import async_db_session
from src.utils.external_client import ExternalAsyncClient


class ProductService:
    max_concurrent = 10

    @staticmethod
    async def get(*, pk: int) -> Product:
        async with async_db_session() as db:
            product = await product_dao.get(db, pk)
            if not product:
                raise HTTPException(404, 'Product not found')
            return product

    @staticmethod
    async def get_page(params: GetPageParams, *, with_total=True) -> Sequence[Product] | Tuple[Sequence[Product], int]:
        limit, offset = params.get_raw()

        async with async_db_session() as db:
            page = await product_dao.get_list(db, offset=offset, limit=limit)

            if not with_total:
                return page

            total = await product_dao.get_total(db)

            return page, total

    @staticmethod
    async def create(*, obj: CreateProductParam) -> Product:
        async with async_db_session.begin() as db:
            return await product_dao.create(db, obj)

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

        if not count:
            raise HTTPException(404, 'Product not found')

        return count

    @staticmethod
    async def fetch_external(
        external_id: Annotated[List[int], Query(min_length=1, max_length=100)],
    ) -> Sequence[Product]:
        """Fetch data from external service by ids"""
        semaphore = asyncio.Semaphore(product_service.max_concurrent)

        async def fetch(cli: ExternalAsyncClient, database: AsyncSession, pk: int):
            """Fetch data for single external id"""

            async with semaphore:
                product = await cli.fetch_product(pk)

                return await product_dao.add_or_update(
                    database,
                    CreateProductParam(
                        name=product['title'],
                        description=product['description'],
                        price=product['price'],
                        external_id=product['id'],
                    ),
                )

        # Gather data with <max_concurrent> number
        async with ExternalAsyncClient() as client:
            async with async_db_session.begin() as db:
                products = await asyncio.gather(*(fetch(client, db, pk) for pk in external_id))

        return products

    @staticmethod
    async def refresh_all():
        pass


product_service = ProductService()
