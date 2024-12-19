import pytest

from starlette.testclient import TestClient


@pytest.mark.order(1)
def test_create_product(client: TestClient, products):
    for product in products:
        resp = client.post('/products', json=product)

        assert resp.status_code == 201, "Can't create product"

        data = resp.json()
        for key, val in product.items():
            assert data.get(key) == val, 'Product created with errors'


@pytest.mark.order(2)
def test_fetch_product(client: TestClient, products):
    resp = client.post('/products/fetch_all', params={'external_id': [x['external_id'] for x in products]})

    assert resp.status_code == 200, "Can't fetch product"

    data = resp.json()['items']

    for product in products:
        updated_product = next((x for x in data if x['external_id'] == product['external_id']), None)

        for key, val in product.items():
            if key == 'external_id':
                continue

            assert updated_product.get(key) != val, 'Product fetched with errors'
