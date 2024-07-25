import unittest
from models import *
from peewee import SqliteDatabase
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
test_db = SqliteDatabase(':memory:')


class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_db.connect()
        test_db.create_tables([ApiUser, Location, Device])
        logger.info("Test database setup")

    @classmethod
    def tearDownClass(cls):
        test_db.drop_tables([ApiUser, Location, Device])
        test_db.close()
        logger.info("Test database torn down")
    
    def test_create_api_user(self):
        user = ApiUser.create(name='John', email='john23@example.com', password='123')
        self.assertIsNotNone(user.id)
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.email, 'john23@example.com')
        logger.info(f"Created user: {user.id}")

    def test_delete_api_user(self):
        user = ApiUser.create(name='Pavlo', email='pavlo@example.com', password='password123')
        user_id = user.id
        user.delete_instance()
        with self.assertRaises(ApiUser.DoesNotExist):
            ApiUser.get(ApiUser.id == user_id)
        logger.info(f"Deleted user: {user_id}")

    def test_create_location(self):
        location = Location.create(name='Living Room')
        self.assertIsNotNone(location.id)
        self.assertEqual(location.name, 'Living Room')
        logger.info(f"Created location: {location.id}")

    def test_create_device(self):
        location = Location.create(name='Bathroom')
        user = ApiUser.create(name='Andriy', email='adnriy@example.com', password='password123')
        device = Device.create(name='Thermostat', type='Temperature', login='thermo', password='devicepass', location_id=location.id, api_user=user.id)
        self.assertIsNotNone(device.id)
        self.assertEqual(device.name, 'Thermostat')
        self.assertEqual(device.type, 'Temperature')
        self.assertEqual(device.login, 'thermo')
        self.assertEqual(str(device.api_user), str(user.id))
        self.assertEqual(str(device.location_id), str(location.id))
        logger.info(f"Created device: {device.id}")

    def test_delete_api_user(self):
        location = Location.create(name='Kitchen')
        user = ApiUser.create(name='Susan', email='susan@example.com', password='password123')
        device = Device.create(name='Kettle', type='Temperature', login='thermo', password='devicepass', location_id=location.id, api_user=user.id)
        device_id = device.id
        user.delete_instance()
        with self.assertRaises(Device.DoesNotExist):
            Device.get(Device.id == device_id)
        logger.info(f"Deleted device: {device.id}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
