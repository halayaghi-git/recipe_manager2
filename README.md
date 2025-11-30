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

## Quick Start / Run Instructions

1. **Back-end API** (terminal #1):
  ```bash
  cd recipe_manager
  source venv/bin/activate
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
2. **Front-end UI** (terminal #2):
  ```bash
  cd recipe_manager/frontend
  npm start
  ```
3. **Visit** http://localhost:3000 and explore the app. Swagger docs live at http://localhost:8000/docs.

> Tip: stop both servers quickly with `pkill -f "uvicorn"` and `pkill -f "npm start"` (or `Ctrl+C` in each terminal).

## Running Locally (Details)

| Component | Command | Notes |
| --- | --- | --- |
| Backend | `uvicorn main:app --reload --host 0.0.0.0 --port 8000` | Requires virtualenv + `pip install -r requirements.txt`. |
| Frontend | `npm start` (inside `frontend/`) | Proxies API calls to port 8000. |
| Docs | http://localhost:8000/docs | Auto-updated OpenAPI. |
| Health | http://localhost:8000/health | Used by load balancers/synthetic checks. |
| Metrics | http://localhost:8000/metrics | Scraped by Prometheus / Grafana. |

### Docker (single command run)

```bash
docker build -t recipe-manager:local .
docker run -p 8000:8000 recipe-manager:local
```
Add `-e` flags for DB/Grafana overrides as needed. The React app can point to this container via `REACT_APP_API_URL`.

## Testing & Quality Gates

| Purpose | Command |
| --- | --- |
| Full test suite with coverage | `PYTHONPATH=. pytest --cov=. --cov-report=term-missing` |
| API-only tests | `PYTHONPATH=. pytest tests/test_api.py -v` |
| Lint/format checks | `black --check . && ruff check .` |
| Security scans | `bandit config.py crud.py database.py main.py models.py schemas.py` and `safety check --full-report` |

All of the above are enforced automatically in CI (see next section). Running them locally mirrors the GitHub Actions workflow.

## Deployment & CI/CD

The repository contains a multi-stage CD pipeline implemented in GitHub Actions (`.github/workflows/cd.yml`). Each push to a CD branch runs the following jobs in order:

1. **quality** – installs dependencies, runs Black, Ruff, Bandit, Safety, and the full pytest suite with coverage.
2. **docker_build** – builds the FastAPI image with Buildx, loads it locally, smoke-tests via `curl`, runs Trivy, and tears down the container.
3. **registry_push** – publishes the image to GitHub Container Registry at `ghcr.io/<owner>/recipe-manager` with both `sha` and `latest` tags.
4. **staging_deploy** – logs into Azure using `AZURE_CREDENTIALS`, points the staging Web App to the freshly pushed image, and restarts it.
5. **production_deploy** – performs the same operations against the production Web App.
6. **post_deploy_checks** – waits for warm-up, automatically discovers the production hostname, and performs HTTP smoke tests (5 retries). Any failure halts the pipeline.
7. **rollback_production** – conditional job that reverts production back to the `latest` image if either the deploy or the post-deploy checks fail, then restarts the site.
8. **cd_success** – simple confirmation job that only runs when everything above passes.

### Triggering the pipeline

- **Branch-based**: push to a CD branch (e.g., `cd-06-complete-cd`) to run the workflow. `main` intentionally keeps the workflow file removed to honour branch-only execution.
- **Manual**: in GitHub’s Actions UI choose the *CD Pipeline* workflow and use **Run workflow** to specify a ref.
- **CLI**: `gh workflow run cd.yml --ref cd-06-complete-cd` (after `gh auth login`).

### Required GitHub secrets

| Secret | Description |
| --- | --- |
| `AZURE_CREDENTIALS` | JSON output from `az ad sp create-for-rbac`, used by `azure/login@v2`. |
| `AZURE_RESOURCE_GROUP` / `AZURE_LOCATION` | Resource metadata shared by staging & production Web Apps. |
| `AZURE_WEBAPP_NAME` | Target Web App name (staging + production if shared). |

### What gets deployed?

- **Image registry**: `ghcr.io/<org-or-user>/recipe-manager` (configured via env vars in the workflow).
- **Azure Web App**: container configuration is updated in-place; no ZIP deploys.
- **Monitoring hooks**: `/health` and `/metrics` are used for smoke/rollback logic.

> To rerun a pipeline without code changes, push an empty commit (e.g., `git commit --allow-empty -m "chore: rerun cd" && git push`).

## Using the Application

1. **Open your browser** and go to: http://localhost:3000
2. **Add recipes** using the "Add Recipe" button
3. **Search recipes** using the search bar
4. **Filter recipes** by meal type or cuisine using the dropdown filters
5. **Edit recipes** by clicking on any recipe card
6. **Delete recipes** using the delete button on recipe cards

If the UI cannot reach the API, ensure both servers are running or that your deployed endpoints are reachable.

### Project Structure
```
recipe_manager/
├── main.py                   # FastAPI application & routes (/health, /metrics)
├── crud.py                   # Database operations
├── database.py               # SQLAlchemy engine/session helpers
├── models.py                 # ORM models
├── schemas.py                # Pydantic request/response models
├── convert_to_md/            # Utility scripts for docs
├── monitoring/
│   ├── README.md             # Prometheus/Grafana setup notes
│   └── grafana/dashboard.json# Starter dashboard
├── frontend/                 # React SPA
│   ├── src/components/       # UI building blocks
│   ├── src/services/api.js   # Axios wrapper to backend
│   └── package.json
├── tests/                    # Pytest suite (API/CRUD/models/config/services)
│   ├── conftest.py           # Fixtures incl. test DB + FastAPI client
│   ├── test_api.py           # End-to-end API + health/metrics checks
│   ├── test_config.py        # Runtime settings + env overrides
│   ├── test_crud.py          # Repository layer unit tests
│   ├── test_models.py        # Model coverage + constraints
│   └── test_services.py      # Service helpers / validation logic
├── requirements.txt          # Runtime + tooling deps
├── requirements-test.txt     # Test-only deps
├── README.md                 # This guide
├── codebase.md               # High-level architecture notes
└── __init__.py
```

### Testing Strategy

Pytest backs the project with fast, isolated runs using an in-memory SQLite database and the FastAPI TestClient. The suite covers:

- **API flow** (`tests/test_api.py`): root and CRUD endpoints, search/filter metadata, validation errors, and the `/health` + `/metrics` observability surfaces.
- **Runtime config** (`tests/test_config.py`): env var parsing, default fallbacks, and any helper utilities that feed settings into the app.
- **CRUD layer** (`tests/test_crud.py`): repository helpers, pagination, and failure modes around missing rows.
- **Models** (`tests/test_models.py`): SQLAlchemy mappings and schema defaults.
- **Service helpers** (`tests/test_services.py`): pure functions used by the React API layer or backend service utilities.

Running `pytest --cov=. --cov-report=term-missing` consistently yields ~97% line coverage.

### Installing Test Dependencies

From the repo root:

```bash
pip install -r requirements-test.txt

# Targeted suites
PYTHONPATH=. pytest tests/test_api.py -v
PYTHONPATH=. pytest tests/test_config.py -v
PYTHONPATH=. pytest tests/test_crud.py -v
PYTHONPATH=. pytest tests/test_models.py -v
PYTHONPATH=. pytest tests/test_services.py -v

# Full run with coverage
PYTHONPATH=. pytest --cov=. --cov-report=term-missing -v
```

### Dependencies

**Backend + Tooling (`requirements.txt`):**
```
fastapi==0.117.1                 # Web framework
uvicorn[standard]==0.37.0         # ASGI server
SQLAlchemy==2.0.43                # ORM / DB engine
pydantic==2.11.9                  # Validation
prometheus-fastapi-instrumentator==7.1.0  # Metrics export

# Developer experience / quality tools
black==24.10.0
ruff==0.6.9
isort==5.13.2
bandit==1.7.7
safety==3.2.4
typer==0.12.1                     # Helper scripts
click==8.1.7                      # Typer dependency
marshmallow==3.21.2               # Legacy schema support
```

**Test-only (`requirements-test.txt`):**
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
- Grafana: import `monitoring/grafana/dashboard.json` to visualise request rate, latency percentiles, and 5xx error rate. The JSON expects a Prometheus data source variable named `DS_PROMETHEUS` (Grafana prompts you to map it during import).

### Exposing Metrics
1. Run the FastAPI backend so `/metrics` is reachable (default `http://localhost:8000/metrics`).
2. Add the endpoint to your Prometheus `scrape_configs`:

   ```yaml
   scrape_configs:
     - job_name: recipe-manager
       static_configs:
         - targets: ['host.docker.internal:8000']
   ```

   Replace the host with whatever load balancer/DNS your deployment uses. If you are scraping from the same machine, `localhost:8000` works fine.

### Grafana Dashboard
1. In Grafana, go to **Dashboards → Import**.
2. Upload `monitoring/grafana/dashboard.json` (lives in this repo) or paste its raw JSON.
3. When prompted, pick your Prometheus data source (Grafana will bind it to the `DS_PROMETHEUS` variable used in the dashboard).
4. Optional: mount `monitoring/` into a Grafana container and use provisioning to auto-load the dashboard for local demos.

### One-command demo stack (Docker Compose)

Prefer to spin everything up locally? Use the ready-made compose bundle under `monitoring/`:

```bash
docker compose -f monitoring/docker-compose.yml up --build
```

This launches three containers:

- `api`: builds the FastAPI app from the repo root and exposes it on `localhost:8000`.
- `prometheus`: uses `monitoring/prometheus.yml` to scrape the API container via service discovery (`api:8000`).
- `grafana`: listens on `http://localhost:3001`, stores state in a local volume, and automatically mounts the `monitoring/grafana` folder so you can import the dashboard JSON without copying files around.

Stop the stack with `docker compose -f monitoring/docker-compose.yml down`.

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