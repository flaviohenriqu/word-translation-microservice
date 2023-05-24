# Word Translation Microservice

The Word Translation Microservice is an API-based application that provides word translations using data fetched from Google Translate. The microservice allows you to retrieve word details, manage the word database, and perform various operations.

## Features

- Get details about a word including translations.
- List all words stored in the database with pagination, sorting, and filtering options.
- Delete a word from the database.

## Technologies Used

- Python 3.10
- FastAPI
- Docker
- PostgreSQL (as the database)
- SQLAlchemy (ORM)
- SQLModel
- Alembic (for database migrations)
- Pydantic (for input/output models)
- Poetry (for dependency management)
- pytest (for unit testing)

## Getting Started

### Prerequisites

- Python 3.10
- Docker (if running the application using Docker)
- PostgreSQL (if running the application without Docker)

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/flaviohenriqu/word-translation-microservice.git
   ```
### Configuration
1. Create a .env file in the project root directory and set the following environment variables:

  ```shell
  DATABASE_URL=postgresql://username:password@localhost:5432/word_translation
  ```
  Replace username and password with your PostgreSQL credentials.

2. Update the database configuration in the alembic.ini file (if necessary).

### Database Setup
1. If running the application without Docker, make sure you have a PostgreSQL database instance set up and running.

2. Run the database migrations using Alembic:
```shell
make migrate
```

### Running the Application
```shell
make run
```

### API Documentation
  Once the application is running, you can access the API documentation at http://localhost:8000/docs in your browser. 
The API documentation provides details about the available endpoints, request/response models, and allows you to interact with the API.

### NOTES:
- I still need to add more unit tests.
- I used a different url to get the google translate data because the web address generates the HTML dynamically
- Change word field to be unique and add validations