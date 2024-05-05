[![TestWorks CI](https://github.com/chrlyons/TestWorks/actions/workflows/run_build_and_tests.yml/badge.svg?branch=main)](https://github.com/chrlyons/TestWorks/actions/workflows/run_build_and_tests.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6431d5283aa242da2953/test_coverage)](https://codeclimate.com/github/chrlyons/TestWorks/test_coverage)

# TestWorks

Just a project to play around with some testing concepts. More to come...

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a **modern version of Python** installed, ideally Python 3.10 or newer.
- You have **Node.js** installed, ideally the latest LTS version.
- You have **Docker** and **Docker Compose** installed for managing containers and dependencies.

## Setting Up the Development Environment

### Backend Setup

1. **Install Poetry**:
   Poetry is used for managing dependencies and virtual environments in Python projects. To install Poetry, run the following command from the root of the project:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   > Ensure that Poetry's bin directory is in your `PATH`. The installer will provide instructions.

2. **Install Backend Dependencies**:
   Navigate to the project's root directory and run:

   ```bash
   poetry install
   ```

   This will install all necessary Python dependencies as specified in the `pyproject.toml` file.

### Frontend Setup

1. **Install Frontend Dependencies**:
   Navigate to the `frontend/` directory:

   ```bash
   cd frontend
   ```

   Then run:

   ```bash
   npm install
   ```

   This will install all necessary Node.js dependencies as specified in the `package.json` file.

## Configuration

Set the following environment variables in your development environment:

```plaintext
DATABASE_URL = <Your_Database_URL>
REDIS_URL = <Your_Redis_URL>
ALGORITHM = <Your_JWT_Algorithm>
SECRET_KEY = <Your_Secret_Key>
frontend/REACT_APP_API_URL= <http://localhost | http://localhost:8000>
```

Replace `<Your_Database_URL>`, `<Your_Redis_URL>`, `<Your_JWT_Algorithm>`, and `<Your_Secret_Key>` with your actual configuration values. These variables are essential for connecting to your database, configuring Redis, and setting up JWT authentication.

## Running the Application

### Starting Services with Docker Compose

To start the database and Redis services, navigate to the project's root directory and run:

```bash
docker-compose up
```

This command starts the configured services like the database and Redis as defined in your `docker-compose.yml` file.

### Starting the Backend Server

To start the backend server using FastAPI with `uvicorn`, run:

```bash
uvicorn backend.main:app --reload
```

### Launching the Frontend

Navigate to the `frontend/` directory and run `npm start`:

```bash
cd frontend/
npm start
```

This will start the frontend development server and open the application in your default web browser.
