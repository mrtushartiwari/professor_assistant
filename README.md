

## Prerequisites
Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/downloads)

## Setting Up PostgreSQL with Docker

To set up a PostgreSQL database using Docker, follow these steps:

Pull the PostgreSQL Docker image and run the container:

```
docker run --name my-postgres-db \
-e POSTGRES_USER=myuser \
-e POSTGRES_PASSWORD=mypassword \
-e POSTGRES_DB=student_management \
-p 5432:5432 \
-d postgres
```

This command will:

Create a container named my-postgres-db.

Set the PostgreSQL username to myuser and password to mypassword.

Create a database named student_management.

Expose PostgreSQL on port 5432.

- Verify that the container is running:

`docker ps`

You should see the my-postgres-db container in the list.


## Install Project dependency
Install the required Python packages using the requirements.txt file:

`pip install -r requirements.txt`

## Configure environment variables:

Create a .env file in the root of your project and add the following variables:
GEMINI_API_KEY= -------
use google AI studio to create the free keys here.

## Populating the Database
To populate the database with initial data, run the populate_database.py script:

`python populate_database.py`

This script will create tables and insert sample data into the database.

## Cleaning Up the Database
If you need to rerun the populate_database.py script, you should first clean up the existing tables using the delete_tables.py script:


`python delete_tables.py`

This script will drop all tables in the database, allowing you to start fresh.


## Run the FastAPI server 
Once the database is set up and populated, you can run your application. For example:

`uvicorn app:app`







