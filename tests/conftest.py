from typing import Generator

import pytest
from starlette.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as client:
        yield client