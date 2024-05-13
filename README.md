[![TestWorks CI](https://github.com/chrlyons/TestWorks/actions/workflows/run_build_and_tests.yml/badge.svg)](https://github.com/chrlyons/TestWorks/actions/workflows/run_build_and_tests.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/28689e7e39f54942aee95cd8c850766f)](https://app.codacy.com/gh/chrlyons/TestWorks/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/28689e7e39f54942aee95cd8c850766f)](https://app.codacy.com/gh/chrlyons/TestWorks/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

# TestWorks

Just a project to play around with some testing concepts. More to come...

## Disclaimer

🚧 Caution: Construction Zone Ahead! 🚧

This project is in perpetual tinkering mode, which means:

- **It's perfect for your test environments**, where chaos is expected and encouraged.
- **It's not quite ready for the big leagues.** Like a toddler at a wedding, it’s best kept away from production environments where grown-up data lives.

So, go ahead and push it, test it, and break it - but please, oh please, don't let it anywhere near your real-world operations unless you enjoy living on the edge... of a very steep cliff.

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

### Launching Docker Test Instances

```bash
docker compose -f test.yml build
docker compose -f test.yml up -d --scale backend=2
```
Navigate to `http://localhost`
