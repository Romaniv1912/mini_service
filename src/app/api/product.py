from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from src.app.schema.product import GetProductInfoDetails, GetProductListDetails
from src.app.service.product import product_service
from src.common.schema import GetList, GetListPage, GetPageParams

router = APIRouter()


@router.get('/{pk}', summary='Product details', description='Get product details')
def get_product(product: GetProductInfoDetails = Depends(product_service.get)) -> GetProductInfoDetails:
    return product


@router.get('', summary='Product page', description='Get page with products')
async def get_product_page(params: GetPageParams = Query()) -> GetListPage[GetProductListDetails]:
    page, total = await product_service.get_page(params)
    return GetListPage.create(page, total, params)


@router.post('', summary='New product', description='Create new product')
def create_product(product: GetProductInfoDetails = Depends(product_service.create)) -> GetProductInfoDetails:
    return product


@router.put('/{pk}', summary='Update product', description='Update the product by PK')
def update_product(product: GetProductInfoDetails = Depends(product_service.update)) -> GetProductInfoDetails:
    return product


@router.delete(
    '/{pk}',
    summary='Delete product',
    description='Delete the product by PK',
    dependencies=[Depends(product_service.delete)],
)
def delete_product() -> None:
    pass
