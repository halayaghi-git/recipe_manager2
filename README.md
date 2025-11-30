# Recipe Manager

A web application for managing recipes, built with FastAPI (backend) and React (frontend).

## Features
- CRUD Operations:
    - Add new recipes with ingredients and instructions (Create)
    - Read existing recipes (Read)
    - Edit existing recipes (Update)
    - Delete recipes (Delete)
- Search Functionality: 
    - Search recipes by title, ingredients, or instructions
- Filter Functionality:
    - Filter by meal type (breakfast, lunch, dinner, snack, dessert)
    - Filter by cuisine (Italian, Chinese, Mexican, Indian, etc.)
- SQLite Database: Stores recipes persistently with SQLAlchemy ORM
- Interactive API Docs: Automatic OpenAPI/Swagger documentation for backend endpoints
- Comprehensive Tests: 97% test coverage with 14 focused backend tests
- Web Interface: User-friendly React frontend for browsing, searching, filtering, adding, editing, and deleting recipes.
- Observability: `/health` status endpoint, Prometheus `/metrics`, and a starter Grafana dashboard.

## Prerequisites
Before starting, ensure you have the following installed on your system:
- **Python 3+**
- **Node.js 18+** (includes npm)
  - Download from: https://nodejs.org/
  - Verify install
- **npm** (comes with Node.js)

## Technologies Used
- **Framework**: FastAPI 0.117.1
- **Database**: SQLite with SQLAlchemy 2.0.43
- **Validation**: Pydantic 2.11.9
- **Server**: Uvicorn 0.37.0
- **Testing**: Pytest with coverage reporting

## Installation

### 1. Clone

```bash
git clone https://github.com/halayaghi-git/recipe_manager.git
cd recipe_manager

```
### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Go back to project root
cd ..
```

## How to Run the Application

You need to run **both** the backend and frontend servers simultaneously.

### Terminal 1 - Start Backend Server

```bash
# Navigate to project root
cd recipe_manager

# Activate virtual environment
source venv/bin/activate

# Start backend server (KEEP RUNNING)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Start Frontend Server

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory
cd recipe_manager/frontend

# Start React development server (KEEP RUNNING)
npm start
```
### Stopping the Servers Quickly

To stop both backend and frontend servers at once, you can use the following commands in a terminal:

```bash
pkill -f "uvicorn"
pkill -f "npm start"
```

This will terminate any running FastAPI (uvicorn) and React (npm start) processes.

## Important Notes

- **Both servers must run simultaneously** 
- The frontend connects to the backend to fetch recipe data
- If you see "Failed to fetch recipes", make sure the backend is running

## Using the Application

1. **Open your browser** and go to: http://localhost:3000
2. **Add recipes** using the "Add Recipe" button
3. **Search recipes** using the search bar
4. **Filter recipes** by meal type or cuisine using the dropdown filters
5. **Edit recipes** by clicking on any recipe card
6. **Delete recipes** using the delete button on recipe cards


When the backend is running, you can view the interactive API documentation at:
**http://localhost:8000/docs**

## Stopping the Application

To stop the servers:
- Press `Ctrl+C` in each terminal window
- Or run: `pkill -f "uvicorn"` and `pkill -f "npm start"`

### Project Structure
```
recipe_manager/
├── main.py                  # FastAPI application & routes
├── models.py                # SQLAlchemy database models
├── schemas.py               # Pydantic data schemas
├── crud.py                  # Database operations
├── database.py              # Database configuration
├── requirements.txt         # Backend dependencies
├── requirements-test.txt    # Test dependencies
├── recipes.db               # SQLite database file (auto-generated)
├── README.md                # Project documentation & running/installation instruction
├── .gitignore               # Git ignore file
├── __init__.py              
├── .coverage                # Test coverage report (auto-generated)
├── frontend/                # React frontend application
│   ├── public/              # Static files (index.html, favicon, etc.)
│   │   ├── index.html
│   │   └── ...
│   ├── src/                
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   ├── package.json         # Frontend dependencies
│   ├── package-lock.json    # Locked dependency versions
│   └── node_modules/        # Frontend dependencies (auto-generated)
├── venv/                    # Python virtual environment (auto-generated)
├── .pytest_cache/           # Pytest cache (auto-generated)
└── tests/                   # Backend tests (97% coverage)
    ├── __init__.py          # Makes tests a Python package
    ├── conftest.py          # Test fixtures & configuration 
    ├── test_api.py          # API endpoint tests (8 tests)
    ├── test_crud.py         # Database operation tests (5 tests)
    └── test_models.py       # Database models tests (1 test)
```

### Testing Strategy

**14 comprehensive tests** achieve **97% code coverage**:

- **API Tests (8)**: Complete CRUD lifecycle, error handling, search/filter
- **CRUD Tests (5)**: Database operations, pagination, edge cases  
- **Model Tests (1)**: SQLAlchemy model validation

### Installing Test Dependencies

To install the testing dependencies, run (in the project root):

```bash
pip install -r requirements-test.txt

# Running specific test categories
PYTHONPATH=. pytest tests/test_api.py -v  
PYTHONPATH=. pytest tests/test_crud.py -v  
PYTHONPATH=. pytest tests/test_models.py -v

# Running all tests with coverage reporting
PYTHONPATH=. pytest --cov=. --cov-report=term-missing -v
```

### Dependencies

**Project (`requirements.txt`):**
```
fastapi==0.117.1
uvicorn[standard]==0.37.0
SQLAlchemy==2.0.43
pydantic==2.11.9
prometheus-fastapi-instrumentator==7.1.0
```

**Testing (`requirements-test.txt`):**
```
pytest==7.4.0
pytest-cov==4.1.0
httpx==0.24.1
pytest-asyncio==0.21.1
```
---

## Monitoring & Health Checks

- `GET /health`: lightweight endpoint that reports application and database status. It is safe to expose to load balancers for liveness/readiness checks.
- `GET /metrics`: Prometheus exposition endpoint powered by `prometheus-fastapi-instrumentator`. It publishes request counts (`http_requests_total`), request/response sizes, latency histograms (`http_request_duration_seconds`), and error status codes.
- Grafana: import `monitoring/grafana/dashboard.json` (see `monitoring/README.md`) to visualise request rate, latency percentiles, and 5xx error rate. Point your Prometheus data source at the backend's `/metrics` endpoint.

Example Prometheus scrape config:

```yaml
scrape_configs:
  - job_name: recipe-manager
    static_configs:
      - targets: ['localhost:8000']
```

With Prometheus scraping in place, the provided Grafana dashboard works out-of-the-box and can be extended with additional metrics as needed.

---

**Happy cooking!**