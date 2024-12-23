from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, Field

from src.common.schema import SchemaBase


class ProductSchemaBase(SchemaBase):
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    price: float = Field(gt=0)
    external_id: int


class CreateProductParam(ProductSchemaBase):
    pass


class UpdateProductParam(SchemaBase):
    name: str | None = Field(max_length=100, default=None)
    description: str | None = Field(max_length=255, default=None)
    price: float | None = None
    external_id: int | None = None


class GetProductListDetails(ProductSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


class GetProductInfoDetails(GetProductListDetails):
    model_config = ConfigDict(from_attributes=True)


class CreateRefreshResponse(SchemaBase):
    status: Literal['started', 'running'] = 'started'
