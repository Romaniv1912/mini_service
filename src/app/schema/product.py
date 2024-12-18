from datetime import datetime

from pydantic import ConfigDict, Field

from src.common.schema import SchemaBase


class ProductSchemaBase(SchemaBase):
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    price: float
    external_id: int | None


class CreateProductParam(ProductSchemaBase):
    pass


class UpdateProductParam(ProductSchemaBase):
    name: str | None = Field(max_length=100)
    description: str | None = Field(max_length=255)
    price: float | None
    external_id: int | None


class GetProductListDetails(ProductSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


class GetProductInfoDetails(GetProductListDetails):
    model_config = ConfigDict(from_attributes=True)
