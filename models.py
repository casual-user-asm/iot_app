import uuid
from dotenv import dotenv_values
from peewee import *

config = dotenv_values()
db = PostgresqlDatabase(
    config.get('DATABASE_NAME'), 
    user=config.get('DATABASE_USER'), 
    password=config.get('DATABASE_PASSWORD'), 
    host=config.get('DATABASE_HOST'), 
    port=config.get('DATABASE_PORT')
    )


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
    api_user = ForeignKeyField(ApiUser, backref='devices', on_delete='CASCADE')


def create_tables():
    with db:
        db.create_tables([ApiUser, Location, Device])
