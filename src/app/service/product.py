import asyncio

from typing import Annotated, Awaitable, Callable, Iterable, List, Literal, Sequence, Tuple, TypeVar

from fastapi import BackgroundTasks, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.product import product_dao
from src.app.model import Product
from src.app.schema.product import CreateProductParam, UpdateProductParam
from src.common.schema import GetPageParams
from src.database import async_db_session
from src.utils.external_client import ExternalAsyncClient

TVal = TypeVar('TVal')


class ProductService:
    max_concurrent: int = 10
    is_refresh_all_run: bool = False
    refresh_all_lock = asyncio.Lock()

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
    async def _fetch_external(
        db: AsyncSession,
        external_id: Iterable[int],
        update_call: Callable[[AsyncSession, CreateProductParam], Awaitable[TVal]],
    ) -> Sequence[TVal]:
        """Fetch data from external service by ids"""
        semaphore = asyncio.Semaphore(product_service.max_concurrent)

        async def fetch(cli: ExternalAsyncClient, database: AsyncSession, pk: int):
            """Fetch data for single external id"""

            async with semaphore:
                product = await cli.fetch_product(pk)

                return await update_call(
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
            products = await asyncio.gather(*(fetch(client, db, pk) for pk in external_id))

        return products

    @staticmethod
    async def fetch_external(
        external_id: Annotated[List[int], Query(min_length=1, max_length=100)],
    ) -> Sequence[Product]:
        async with async_db_session.begin() as db:
            return await product_service._fetch_external(db, external_id, product_dao.add_or_update)

    @staticmethod
    async def refresh_all(bg: BackgroundTasks) -> Literal['running', 'started']:
        # Ensure task is done
        async with product_service.refresh_all_lock:
            if product_service.is_refresh_all_run:
                return 'running'

            product_service.is_refresh_all_run = True

        async def fetch():
            try:
                offset, limit = 0, 50

                async with async_db_session() as db:
                    total = await product_dao.get_total(db)

                    while offset < total:
                        products = await product_dao.get_list(db, offset=offset, limit=limit)

                        await product_service._fetch_external(
                            db, (x.external_id for x in products), product_dao.update_by_external_id
                        )
                        await db.commit()

                        offset += limit
            except:
                raise
            finally:
                # Release <is_refresh_all_run>
                async with product_service.refresh_all_lock:
                    product_service.is_refresh_all_run = False

        bg.add_task(fetch)

        return 'started'


product_service = ProductService()
