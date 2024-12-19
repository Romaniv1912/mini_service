import asyncio

from typing import Any, Dict, Generator, List

import pytest

from starlette.testclient import TestClient

from main import app
from src.app.schema.product import CreateProductParam
from tests.utils.database import init_table

asyncio.run(init_table())


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def products() -> List[Dict[str, Any]]:
    return [
        CreateProductParam(name=f'name{i}', description=f'desc{i}', price=1, external_id=i).model_dump()
        for i in range(1, 5)
    ]
