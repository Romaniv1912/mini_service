from httpx import AsyncClient


class ExternalAsyncClient(AsyncClient):
    """External client to fetch data from external service"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._base_url = 'https://dummyjson.com'

    async def fetch_product(self, pk: int):
        resp = await self.get(f'{self._base_url}/products/{pk}')

        resp.raise_for_status()

        return resp.json()
