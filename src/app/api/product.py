from typing import List

from fastapi import APIRouter, Depends, Query

from src.app.schema.product import CreateRefreshResponse, GetProductInfoDetails, GetProductListDetails
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


@router.post(
    '/fetch_all/',
    summary='Fetch products',
    description='Fetch all products by external id',
)
def fetch_external_products(
    products: List[GetProductListDetails] = Depends(product_service.fetch_external),
) -> GetList[GetProductListDetails]:
    return GetList(products)


@router.post(
    '/refresh_all/',
    summary='Refresh products',
    description='Refresh all products',
)
def refresh_all_products(status=Depends(product_service.refresh_all)) -> CreateRefreshResponse:
    return CreateRefreshResponse(status=status)
