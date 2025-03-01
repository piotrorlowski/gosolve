# Makefile to set up the project environment

VENV_DIR = ./venv

SHELL := /bin/bash  # Use bash explicitly

# Set up the virtual environment and install dependencies
install-venv:
	@echo "Creating virtual environment in current directory..."
	@python3 -m venv venv
	@echo "Virtual environment created."

# Install Python dependencies using pip (inside virtual environment)
install-requirements: install-venv
	@echo "Installing Python dependencies..."
	@source $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	@echo "Python dependencies installed."

# Install frontend dependencies using npm (inside ui/)
install-frontend-deps:
	@echo "Installing frontend dependencies in ui/ directory..."
	@cd ui && npm install
	@echo "Frontend dependencies installed."

# Run full installation (create venv, install Python and frontend dependencies)
install: install-venv install-requirements install-frontend-deps
	@echo "Project setup complete!"

# Run the FastAPI backend (inside api/ directory)
run-api:
	@echo "Starting FastAPI server inside api/ directory..."
	@source $(VENV_DIR)/bin/activate && cd api && uvicorn main:app --reload

# Run the frontend (inside ui/ directory)
run-ui:
	@echo "Starting frontend development server inside ui/ directory..."
	@cd ui && npm run dev

# Run the entire project (backend + frontend)
run: run-api run-ui
	@echo "Project is running!"

# Run the backend tests (inside api/ directory)
test-api:
	@echo "Running backend tests with pytest in api/ directory..."
	@source $(VENV_DIR)/bin/activate && cd api && pytest
	@echo "Backend tests completed."

# Run the frontend tests (inside ui/ directory)
test-ui:
	@echo "Running frontend tests with vitest in ui/ directory..."
	@cd ui && npx vitest --run
	@echo "Frontend tests completed."

# Run all tests (backend + frontend)
test: test-api test-ui
	@echo "All tests completed!"
