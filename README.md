# Project Setup and Management

This repository uses a Makefile to manage the environment setup, dependencies, and running the project (both frontend and backend). It handles the creation of a Python virtual environment, installs necessary dependencies, and manages backend and frontend commands.

## Prerequisites

Before using the Makefile, ensure that the following tools are installed on your system:

- [Python 3](https://www.python.org/downloads/) (including `python3` and `pip`)
- [Node.js](https://nodejs.org/en/) (for managing frontend dependencies)
- [Make](https://www.gnu.org/software/make/) (for running the Makefile commands)

## Project installation and running:
1. `make install`
2. `make run`

To run tests:
1. `make test`

## Available Makefile Commands

The Makefile defines several commands to help set up and manage your project. Below is a detailed description of each command and its purpose.

### `make install`

This command runs a full installation process for the project. It will:
- Create a Python virtual environment in the current directory.
- Install Python dependencies from the `requirements.txt` file.
- Install frontend dependencies inside the `ui/` directory.

This is the command to run when setting up the entire project from scratch.

### `make install-venv`

This command creates a Python virtual environment in the `./venv` directory. It uses `python3 -m venv` to set up the environment. This step is required before installing any Python dependencies. Run this command when you need to create a fresh virtual environment.

### `make install-requirements`

After the virtual environment is created, this command installs the Python dependencies listed in the `requirements.txt` file. It ensures that all the necessary Python packages are available for the backend. You need to run this command after creating the virtual environment or whenever the `requirements.txt` is updated.

### `make install-frontend-deps`

This command installs all JavaScript dependencies for the frontend application (located in the `ui/` directory) using `npm install`. It is essential for running the frontend development server and tests. Run this command to install the necessary dependencies in the `ui/` directory before starting the frontend.

### `make create-env-file`
This command creates .env file with default configuration PORT=8000 and LOG_LEVEL=Debug

### `make run-api`

This command starts the FastAPI backend server using `uvicorn`. The virtual environment is activated before running the server. It runs the server in "reload" mode, meaning the server will automatically restart on code changes. Use this command to run the backend server.

### `make run-ui`

This command starts the frontend development server (using `npm run dev`). It assumes the frontend application is located inside the `ui/` directory and that the necessary dependencies are already installed. This command is used to run the frontend server during development.

### `make run`

This command runs both the FastAPI backend (`make run-api`) and the frontend development server (`make run-ui`) simultaneously. It is useful for running the full stack during development. Use this command when you want both the backend and frontend servers running at the same time.

### `make test`

This command runs both the backend and frontend tests:
- It activates the virtual environment.
- It runs the backend tests using `pytest` inside the `api/` directory.
- It runs the frontend tests using `vitest` inside the `ui/` directory.

This is the command to use when you want to run all the tests for both backend and frontend.

### `make test-api`

This command runs the backend tests using `pytest`. It ensures that the backend logic is working as expected. The tests are located inside the `api/` directory. Use this command to run only the backend tests.

### `make test-ui`

This command runs the frontend tests using `vitest` (or a similar JavaScript testing framework). The tests are located inside the `ui/` directory. Use this command to run only the frontend tests.

---

## Folder Structure

```plaintext
.
├── api/                # Backend directory (FastAPI)
│   ├── main.py         # Entry point for the FastAPI application
│   ├── utils.py        # Utility functions, including an algorithm to find the index of a value in a list
│   ├── data.py         # Function responsible for loading data into memory
│   ├── routers/        # Directory containing API endpoints
│   │   └── index.py    # Endpoint for retrieving the index of a value in a list
├── ui/                 # Frontend directory (React.js)
│   └── package.json    # Frontend dependencies and scripts
├── venv/               # Python virtual environment
├── requirements.txt    # Python dependencies
├── Makefile            # Makefile for managing setup, installation, and execution
└── README.md           # This README file
