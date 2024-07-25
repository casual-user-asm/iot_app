IoT Device Management App

This project provides an API for managing IoT devices, users, and locations. Built using aiohttp, Peewee, and PostgreSQL, it supports basic CRUD operations for users, devices, and locations.

Running the Project with Docker
Prerequisites

    Docker: Ensure Docker is installed on your machine. You can download it from Docker's official website.
    Docker Compose: Make sure it's installed as well. You can find installation instructions here.

Getting Started

    Clone the Repository:

    git clone https://github.com/casual-user-asm/iot_app.git
    cd yourproject

    Create and Configure .env File:

        Create the .env file to add any necessary configuration values (database URLs).

        Below are the common configuration fields you may need to set in your .env file.
        Debug mode (set to True for development)

        PostgreSQL database settings
            DATABASE_NAME=postgres
            DATABASE_USER=postgres
            DATABASE_PASSWORD=postgres
            DATABASE_HOST=my_postgres
            DATABASE_PORT=5432


    Build the Docker Images:
        Using docker-compose.yml:

        docker-compose build

    Run the Containers:
        Using Docker Compose:

        docker-compose up -d

