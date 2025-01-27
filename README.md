# Professor Assistant

This project demonstrates an AI-powered assistant built using LangChain (or Llama) and a FastAPI backend to interact with a PostgreSQL database. The assistant processes natural language instructions from a professor, extracts intent, and performs database operations such as adding students, recording scores, retrieving data, and summarizing information.

#### Key Features:

- Natural language understanding to execute professor instructions.
- Seamless API integration with PostgreSQL for CRUD operations.

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


## How to Run the Query:
To execute a query, run the following command:

`python query_runner.py`

To change the query update the line 
`run_query(query= "Average marks in Maths")`


## Drawbacks
1. Spelling Mistakes or Variations in Subject Names

    The assistant may fail to recognize or map subject names if there are typos or inconsistencies (e.g., "Mathematics" vs. "Maths").

2. Handling of Summary Queries and API Exceptions from the Database

    Some complex summary queries or database API errors may not be handled gracefully, requiring better exception management.

3. Limited Tool Use by LLM (Not Explored)

    The current implementation may not fully leverage the tool-use functionality of LLMs, which could enhance its ability to interact with APIs dynamically.





