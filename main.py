from datetime import UTC, datetime


from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import get_settings
from crud import (
    create_recipe,
    create_tag,
    create_user,
    delete_recipe,
    filter_recipes,
    get_recipe,
    get_recipes,
    get_unique_cuisines,
    get_unique_meal_types,
    list_tags,
    list_users,
    search_recipes,
    update_recipe,
)
from database import Base, SessionLocal, engine
from schemas import Recipe, RecipeCreate, Tag, TagCreate, User, UserCreate

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()
DEFAULT_PAGE_LIMIT = settings.recipes_page_size

app = FastAPI(
    title="Recipe Manager API",
    description="A simple API for managing recipes",
    version="1.0.0",
)


# Serve React static files only for non-API routes
from fastapi.responses import FileResponse

frontend_build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
if os.path.isdir(frontend_build_dir):
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(frontend_build_dir, "static")),
        name="static",
    )

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # If the path starts with 'api' or matches an API route, return 404 so FastAPI handles it
        api_prefixes = ["recipes", "users", "tags", "meal-types", "cuisines", "health"]
        if any(full_path.startswith(prefix) for prefix in api_prefixes):
            return HTTPException(status_code=404)
        index_path = os.path.join(frontend_build_dir, "index.html")
        return FileResponse(index_path)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Welcome to Recipe Manager API! Visit /docs for API documentation"
    }


@app.get("/health", tags=["Monitoring"])
def health_check(db: Session = Depends(get_db)):
    """Lightweight application and database health indicator."""

    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"

    overall_status = "ok" if db_status == "ok" else "degraded"
    return {
        "status": overall_status,
        "checks": {
            "database": db_status,
        },
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.post("/recipes/", response_model=Recipe)
def create_recipe_endpoint(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    return create_recipe(db, recipe)


@app.get("/recipes/", response_model=list[Recipe])
def read_recipes(
    skip: int = 0, limit: int = DEFAULT_PAGE_LIMIT, db: Session = Depends(get_db)
):
    """Get all recipes with pagination"""
    return get_recipes(db, skip=skip, limit=limit)


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    recipe = get_recipe(db, recipe_id=recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe_endpoint(
    recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)
):
    """Update an existing recipe"""
    updated_recipe = update_recipe(db, recipe_id=recipe_id, recipe=recipe)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe


@app.delete("/recipes/{recipe_id}")
def delete_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe"""
    deleted_recipe = delete_recipe(db, recipe_id=recipe_id)
    if deleted_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}


@app.get("/recipes/search/{query}")
def search_recipes_endpoint(query: str, db: Session = Depends(get_db)):
    """Search recipes by title, cuisine, or meal type"""
    recipes = search_recipes(db, query=query)
    return recipes


@app.get("/recipes/filter/", response_model=list[Recipe])
def filter_recipes_endpoint(
    meal_type: str = None, cuisine: str = None, db: Session = Depends(get_db)
):
    """Filter recipes by meal type and/or cuisine"""
    recipes = filter_recipes(db, meal_type=meal_type, cuisine=cuisine)
    return recipes


@app.get("/meal-types/")
def get_meal_types(db: Session = Depends(get_db)):
    """Get all unique meal types for filter dropdown"""
    meal_types = get_unique_meal_types(db)
    return [{"value": mt[0]} for mt in meal_types if mt[0]]


@app.get("/cuisines/")
def get_cuisines(db: Session = Depends(get_db)):
    """Get all unique cuisines for filter dropdown"""
    cuisines = get_unique_cuisines(db)
    return [{"value": c[0]} for c in cuisines if c[0]]


@app.post("/users/", response_model=User, tags=["Users"])
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@app.get("/users/", response_model=list[User], tags=["Users"])
def list_users_endpoint(db: Session = Depends(get_db)):
    return list_users(db)


@app.post("/tags/", response_model=Tag, tags=["Tags"])
def create_tag_endpoint(tag: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, tag)


@app.get("/tags/", response_model=list[Tag], tags=["Tags"])
def list_tags_endpoint(db: Session = Depends(get_db)):
    return list_tags(db)


instrumentator = (
    Instrumentator()
    .add(metrics.requests())
    .add(metrics.latency())
    .add(metrics.response_size())
    .add(metrics.request_size())
)

instrumentator.instrument(app).expose(
    app,
    include_in_schema=False,
    should_gzip=True,
    tags=["Monitoring"],
)
