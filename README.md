IoT Device Management API

This project provides an API for managing IoT devices, users, and locations. Built using aiohttp, Peewee, and PostgreSQL, it supports basic CRUD operations for users, devices, and locations.
Table of Contents

    Installation
    Configuration
    Running the Application
    API Endpoints
        User Endpoints
        Location Endpoints
        Device Endpoints
    Testing
    Logging
    Troubleshooting
    License

Installation

    Clone the Repository:

    bash

git clone https://github.com/your-repository/iot-device-management.git
cd iot-device-management

Create and Activate a Virtual Environment:

bash

python -m venv venv
# On Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

Install Dependencies:

bash

pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory of the project with the following content:

makefile

    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

Configuration

Ensure PostgreSQL is running and configured as specified in your .env file.

Docker Configuration (Optional):
If using Docker, ensure the docker-compose.yml file is correctly set up. Run the following commands to build and start the containers:

bash

docker-compose build
docker-compose up

Running the Application

To start the application, run:

bash

python app.py

By default, the application will run on port 8080. You can change this in the app.py file or via environment variables.
API Endpoints

User Endpoints:

    GET /users: Retrieve a list of all users.
    GET /users/{id}: Retrieve a single user by ID.
    POST /users: Create a new user.
    DELETE /users/{id}: Delete a user by ID.

Location Endpoints:

    GET /locations: Retrieve a list of all locations.
    POST /locations: Create a new location.
    DELETE /locations/{id}: Delete a location by ID.

Device Endpoints:

    GET /devices: Retrieve a list of all devices.
    GET /devices/{id}: Retrieve a single device by ID.
    POST /devices: Create a new device.
    PUT /devices/{id}: Update an existing device.
    DELETE /devices/{id}: Delete a device by ID.

Testing

Unit Tests:
Unit tests for the models are located in test_models.py. To run the unit tests:

bash

python -m unittest discover -s tests

API Tests:
API tests are located in test_API.py. To run the API tests:

bash

python -m unittest test_API.py

Test Coverage:
To ensure code coverage, you can use coverage.py. Install it with:

bash

pip install coverage

Then run:

bash

coverage run -m unittest discover -s tests
coverage report
coverage html  # For an HTML report

Logging

Logging is configured using the logging module. The log messages will be output based on the logging level set. For more detailed logging, you can adjust the logging.basicConfig settings in the app.py file.

Example logging configuration:

python

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

Troubleshooting

    500 Internal Server Error: Check the server logs for detailed error messages. Ensure all dependencies are correctly configured and that database connections are valid.
    Database Connection Errors: Verify that PostgreSQL is running and that the database credentials in the .env file are correct.
    File Not Found: Ensure that files like home.html are present in the correct directory.

License

This project is licensed under the MIT License - see the LICENSE file for details.
