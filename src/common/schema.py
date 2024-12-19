import math

from typing import Generic, List, Tuple, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)


TSchema = TypeVar('TSchema')


class GetPageParams(BaseModel):
    page: int = Query(1, ge=1, description='Page number')
    size: int = Query(20, gt=0, le=100, description='Page size')  # Default 20 records

    def get_raw(self) -> Tuple[int, int]:
        return self.size, self.size * (self.page - 1)


class GetList(SchemaBase, Generic[TSchema]):
    items: List[TSchema]  # data
    total: int  # total number of data

    def __init__(self, items: List[TSchema], **kwargs):
        total = kwargs.pop('total', len(items))
        super().__init__(items=items, total=total, **kwargs)


class GetListPage(GetList):
    page: int  # page n
    size: int  # quantity per page
    total_pages: int  # total pages

    @classmethod
    def create(cls, items: List[TSchema], total: int, params: GetPageParams):
        return cls(
            items=items,  # type: ignore
            total=total,  # type: ignore
            page=params.page,
            size=params.size,
            total_pages=math.ceil(total / params.size),
        )
