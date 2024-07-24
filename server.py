from models import ApiUser, Location, Device, db
import json
from aiohttp import web
from argon2 import PasswordHasher

ph = PasswordHasher()
routes = web.RouteTableDef()

def html_response(document):
    page = open(document, 'r')
    return web.Response(text=page.read(), content_type='text/html')

@routes.get('/')
async def home(request):
    return html_response('home.html')

@routes.get('/users')
async def users(request):
    users = ApiUser.select()
    users_list = [{'id': str(user.id), 'name': user.name, 'email': user.email} for user in users]
    return web.json_response(users_list)

@routes.get('/users/{id}')
async def single_users(request):
    user_id = request.match_info.get('id')
    user = ApiUser.get(ApiUser.id == user_id)
    devices = list(Device.select().where(Device.api_user == user))
    user_info = [{'id': str(user.id), 'name': user.name, 'email': user.email, 'devices': [{'id': str(device.id), 'name': device.name, 'type': device.type, 'location': device.location_id} for device in devices]}]
    return web.json_response(user_info)

@routes.post('/users')
async def create_user(request):
    data = await request.json()
    pass_hash = ph.hash(data['password'])
    user = ApiUser.create(name=data['name'], email=data['email'], password=pass_hash)
    return web.json_response({'id': str(user.id)}, status=201)

@routes.delete('/users/{id}')
async def delete_user(request):
    user_id = request.match_info.get('id')
    delete_user = ApiUser.delete().where(ApiUser.id == user_id)
    delete_user.execute()
    return web.json_response({'status': 'deleted'})

@routes.get('/locations')
async def locations(request):
    locations = Location.select()
    locations_list = [{'id': str(location.id), 'name': location.name} for location in locations]
    return web.json_response(locations_list)

@routes.post('/locations')
async def add_location(request):
    data = await request.json()
    new_location = Location.create(name=data['name'])
    return web.json_response({'status': f'{new_location.id} created'})

@routes.delete('/locations/{id}')
async def delete_location(request):
    location_id = request.match_info.get('id')
    delete_location = Location.delete().where(Location.id == location_id)
    delete_location.execute()
    return web.json_response({'status': 'deleted'})

@routes.get('/devices')
async def devices(request):
    devices = Device.select()
    devices_list = [{'id': str(device.id), 'name': device.name, 'type': device.type, 'location_id': str(device.location_id), 'api_user_id': str(device.api_user), 'login': device.login} for device in devices]
    return web.json_response(devices_list)

@routes.get('/devices/{id}')
async def single_device(request):
    device_id = request.match_info.get('id')
    device = Device.get(Device.id == device_id)
    device_info = [{'name': device.name, 'type': device.type, 'login': device.login, 'location': str(device.location_id), 'user': str(device.api_user)}]
    return web.json_response(device_info)

@routes.post('/devices')
async def add_new_device(request):
    data = await request.json()
    pass_hash = ph.hash(data['password'])
    location_id = data.get('location_id')
    location_id = None if location_id == '' else location_id
    
    new_device = Device.create(name=data['name'], type=data['type'], login=data['login'], password=pass_hash, location_id=Location.get_or_none(Location.id == location_id), api_user=data['api_user'])
    return web.json_response({'status': f'{new_device.id} created'})

@routes.put('/devices/{id}')
async def update_device(request):
    device_id = request.match_info.get('id')
    try:
        device = Device.get(Device.id == device_id)
    except Device.DoesNotExist:
        return web.json_response({'error': 'device not found'}, status=404)

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
    device_id = request.match_info.get('id')
    delete_device = Device.delete().where(Device.id == device_id)
    delete_device.execute()
    return web.json_response({'status': 'deleted'})

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)