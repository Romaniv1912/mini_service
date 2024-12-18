from fastapi import APIRouter, Depends
from sqlalchemy import Select

from src.app.schema.product import GetProductInfoDetails, GetProductListDetails
from src.app.service.product import product_service
from src.common.pagination import Page, paging_data
from src.database import CurrentSession

router = APIRouter()


@router.get('/{pk}', summary='Product details', description='Get product details')
def get_product(product: GetProductInfoDetails = Depends(product_service.get)) -> GetProductInfoDetails:
    return product


@router.get('', summary='Product list', description='Get list of products')
async def get_product_list(
    db: CurrentSession, select: Select = Depends(product_service.get_select)
) -> Page[GetProductListDetails]:
    return await paging_data(db, select, GetProductListDetails)


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
