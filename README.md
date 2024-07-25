# IoT Device Management API

Welcome to the IoT Device Management API! This project provides an API for managing IoT devices, users, and locations. Using `aiohttp`, `Peewee`, and PostgreSQL, it supports essential CRUD operations for managing users, devices, and locations. 

**IoT Device Management API:** Efficiently manage your IoT ecosystem with a straightforward API that simplifies operations and integrates seamlessly with your setup.

![IoT Device Management](https://your-image-url.com/image.png)
*Enhance your IoT management experience with our streamlined API solution.*

# Project Setup

The app provides several endpoints to manage IoT resources:

- **User Endpoints**: Create, retrieve, and delete user records.
- **Location Endpoints**: Manage locations where devices are installed.
- **Device Endpoints**: Perform operations on IoT devices, including create, update, and delete actions.

---

You can run the project locally or use Docker for containerized deployment. Instructions for both methods are provided below.

## Running the Project with Docker

### Prerequisites
- **Docker**: Ensure Docker is installed on your machine. Download it from [Docker's official website](https://www.docker.com/get-started).
- **Docker Compose**: Make sure it's installed as well. Installation instructions can be found [here](https://docs.docker.com/compose/install/).

### Getting Started

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/iot-device-management.git
    cd iot-device-management
    ```

2. **Create and Configure `.env` File**:
    - Create a `.env` file in the root directory with the following content:
    ```plaintext
    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```
    - Ensure PostgreSQL is running and accessible using these credentials.

3. **Build the Docker Images**:
    ```bash
    docker-compose build
    ```

4. **Run the Containers**:
    ```bash
    docker-compose up -d
    ```

## Running the Application Locally

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/iot-device-management.git
    cd iot-device-management
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    # On Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    python app.py
    ```
    By default, the application runs on port 8080. You can change this in the `app.py` file or through environment variables.

## API Endpoints

### User Endpoints

- **GET `/users`**: Retrieve a list of all users.
- **GET `/users/{id}`**: Retrieve a specific user by ID.
- **POST `/users`**: Create a new user.
- **DELETE `/users/{id}`**: Delete a user by ID.

### Location Endpoints

- **GET `/locations`**: Retrieve a list of all locations.
- **POST `/locations`**: Create a new location.
- **DELETE `/locations/{id}`**: Delete a location by ID.

### Device Endpoints

- **GET `/devices`**: Retrieve a list of all devices.
- **GET `/devices/{id}`**: Retrieve a specific device by ID.
- **POST `/devices`**: Create a new device.
- **PUT `/devices/{id}`**: Update an existing device.
- **DELETE `/devices/{id}`**: Delete a device by ID.
