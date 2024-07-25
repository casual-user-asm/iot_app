from aiohttp import web
from argon2 import PasswordHasher
import logging

from models import ApiUser, Device, Location

ph = PasswordHasher()
routes = web.RouteTableDef()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def html_response(document):
    """
    Helper function to create an HTML response from a file.
    
    Parameters:
    document (str): Path to the HTML file.
    """
    with open(document, 'r') as page:
        return web.Response(text=page.read(), content_type='text/html')


@routes.get('/')
async def home(request):
    """
    Route handler for the home page.
    """
    logger.info("Request to /")
    return html_response('home.html')


@routes.get('/users')
async def users(request):
    """
    Route handler to get a list of all users.
    """
    logger.info("Request to /users")
    users = ApiUser.select()
    users_list = [{'id': str(user.id), 'name': user.name, 'email': user.email} for user in users]
    return web.json_response(users_list)


@routes.get('/users/{id}')
async def single_users(request):
    """
    Route handler to get information about a single user by ID.
    """
    user_id = request.match_info.get('id')
    try:
        logger.info(f"Request to /users/{user_id}")
        user = ApiUser.get(ApiUser.id == user_id)
        devices = list(Device.select().where(Device.api_user == user))
        user_info = [{'id': str(user.id), 'name': user.name, 'email': user.email, 'devices': [{'id': str(device.id), 'name': device.name, 'type': device.type, 'location': device.location_id} for device in devices]}]
        return web.json_response(user_info)
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({
            "message": "Error: User not found",
        }, status=404)


@routes.post('/users')
async def create_user(request):
    """
    Route handler to create a new user.
    
    Request Body:
    {
        "name": str,
        "email": str,
        "password": str
    }
    """
    try:
        logger.info("Request to create user")
        data = await request.json()
        pass_hash = ph.hash(data['password'])
        user = ApiUser.create(name=data['name'], email=data['email'], password=pass_hash)
        return web.json_response({'status': f'User {user.name} created'}, status=201)
    except Exception as e:
        logger.warning(f'Error - {e}')
        return web.json_response({'message': 'Email already used'})


@routes.delete('/users/{id}')
async def delete_user(request):
    """
    Route handler to delete a user by ID.
    """
    user_id = request.match_info.get('id')
    try:
        logger.info(f"Request to delete user {user_id}")
        delete_user = ApiUser.delete().where(ApiUser.id == user_id)
        delete_user.execute()
        return web.json_response({'status': 'User deleted'})
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({
            "message": "Can't delete: Wrong User ID",
        }, status=404)


@routes.get('/locations')
async def locations(request):
    """
    Route handler to get a list of all locations.
    """
    logger.info("Request to all locations")
    locations = Location.select()
    locations_list = [{'id': str(location.id), 'name': location.name} for location in locations]
    return web.json_response(locations_list)


@routes.post('/locations')
async def add_location(request):
    """
    Route handler to add a new location.
    
    Request Body:
    {
        "name": str
    }
    """
    logger.info("Request to add location")
    data = await request.json()
    new_location = Location.create(name=data['name'])
    return web.json_response({'status': f'{new_location.name} added'})


@routes.delete('/locations/{id}')
async def delete_location(request):
    """
    Route handler to delete a location by ID.
    """
    location_id = request.match_info.get('id')
    try:
        logger.info(f"Request to delete location {location_id}")
        delete_location = Location.delete().where(Location.id == location_id)
        delete_location.execute()
        return web.json_response({'status': 'Location deleted'})
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({'message': "Can't delete location: Wrong location ID"}, status=404)


@routes.get('/devices')
async def devices(request):
    """
    Route handler to get a list of all devices.
    """
    logger.info(f"Request to all devices")
    devices = Device.select()
    devices_list = [{'id': str(device.id), 'name': device.name, 'type': device.type, 'location_id': str(device.location_id), 'api_user_id': str(device.api_user), 'login': device.login} for device in devices]
    return web.json_response(devices_list)


@routes.get('/devices/{id}')
async def single_device(request):
    """
    Route handler to get information about a single device by ID.
    """
    device_id = request.match_info.get('id')
    try:
        logger.info(f"Request to device {device_id}")
        device = Device.get(Device.id == device_id)
        device_info = [{'name': device.name, 'type': device.type, 'login': device.login, 'location': str(device.location_id), 'user': str(device.api_user)}]
        return web.json_response(device_info)
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({"message": 'Error: Device not found'}, status=404)


@routes.post('/devices')
async def add_new_device(request):
    """
    Route handler to create a new device.
    
    Request Body:
    {
        "name": str,
        "type": str,
        "login": str,
        "password": str,
        "location_id": str,
        "api_user": str
    }
    """
    logger.info(f"Request to create device")
    data = await request.json()
    pass_hash = ph.hash(data['password'])
    location_id = data.get('location_id')
    location_id = None if location_id == '' else location_id

    new_device = Device.create(name=data['name'], type=data['type'], login=data['login'], password=pass_hash, location_id=Location.get_or_none(Location.id == location_id), api_user=data['api_user'])
    return web.json_response({'status': f'{new_device.name} created'})


@routes.put('/devices/{id}')
async def update_device(request):
    """
    Route handler to update an existing device by ID.
    
    Request Body:
    {
        "name": str,
        "type": str,
        "login": str,
        "password": str
    }
    """
    device_id = request.match_info.get('id')
    try:
        logger.info(f"Request to update device {device_id}")
        device = Device.get(Device.id == device_id)
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({'message': 'Error: Device Not Found'}, status=404)

    data = await request.json()

    device.name = data.get('name', device.name)
    device.type = data.get('type', device.type)
    device.login = data.get('login', device.login)
    device.password = data.get(ph.hash('password'), device.password)

    device.save()

    return web.json_response({
        'id': str(device.id),
        'name': device.name,
        'type': device.type,
        'login': device.login,
        'location_id': str(device.location_id) if device.location_id else None,
        'user_id': str(device.api_user),
    })


@routes.delete('/devices/{id}')
async def delete_device(request):
    """
    Route handler to delete a device by ID.
    """
    device_id = request.match_info.get('id')
    try:
        logger.info(f"Request to delete device {device_id}")
        delete_device = Device.delete().where(Device.id == device_id)
        delete_device.execute()
        return web.json_response({'status': 'Device deleted'})
    except Exception as e:
        logger.warning(f"Error - {e}")
        return web.json_response({"message": "Error: Wrong Device ID"})

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)
