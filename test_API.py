import unittest
from models import *
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        def html_response(document):

            with open(document, 'r') as page:
                return web.Response(text=page.read(), content_type='text/html')

        async def home(request):
            return html_response('home.html')

        async def create_device(request):
            data = await request.json()
            return web.json_response({'id': '1', 'name': data['name']}, status=201)

        async def update_device(request):
            data = await request.json()
            return web.json_response({'id': request.match_info['id'], 'name': data['name']})

        async def delete_device(request):
            return web.json_response(status=204)

        app = web.Application()
        app.router.add_get('/', home)
        app.router.add_post('/devices', create_device)
        app.router.add_put('/devices/{id}', update_device)
        app.router.add_delete('/devices/{id}', delete_device)
        return app

    async def test_get_home(self):
        async with self.client.request("GET", "/") as resp:
            self.assertEqual(resp.status, 200)
            logger.info(f"TEST: Connected to Home Page")

    async def test_post_device(self):
        data = {
            "name": 'iphone',
            "type": 'garbage',
            "login": 'admin',
            "password": '1234',
            "location_id": '1',
            "api_user": '2'
    }
        async with self.client.post('/devices', json=data) as resp:
            self.assertEqual(resp.status, 201)
            response_json = await resp.json()
            self.assertEqual(response_json['name'], 'iphone')
            self.assertEqual(response_json['id'], '1')
            logger.info(f"TEST: Create new device")

    async def test_put_device(self):
        data = {
            "name": 'laptop',
            "type": 'acer',
            "login": 'admin',
            "password": '1234'
    }
        async with self.client.put('/devices/1', json=data) as resp:
            self.assertEqual(resp.status, 200)
            response_json = await resp.json()
            self.assertEqual(response_json['id'], '1')
            self.assertEqual(response_json['name'], 'laptop')
            logger.info(f"TEST: Update device")

    async def test_delete_device(self):
        async with self.client.delete('/devices/1') as resp:
            self.assertEqual(resp.status, 204)
            logger.info(f"TEST: Delete device")


if __name__ == "__main__":
    unittest.main()
