from peewee import *
import uuid

db = PostgresqlDatabase('iot_app', user='postgres', password='4254648', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db
    
class ApiUser(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(max_length=128)
    email = CharField(unique=True)
    password = CharField()

class Location(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(max_length=256)

class Device(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(max_length=256)
    type = CharField(max_length=128)
    login = CharField(max_length=128)
    password = CharField()
    location_id = ForeignKeyField(Location, backref='location', null=True)
    api_user = ForeignKeyField(ApiUser, backref='devices')

def create_tables():
    with db:
        db.create_tables([ApiUser, Location, Device])
