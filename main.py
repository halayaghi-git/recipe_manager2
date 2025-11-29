from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import get_settings
from crud import (create_recipe, delete_recipe, filter_recipes, get_recipe,
                  get_recipes, get_unique_cuisines, get_unique_meal_types,
                  search_recipes, update_recipe)
from database import Base, SessionLocal, engine
from schemas import Recipe, RecipeCreate

# Create database tables
Base.metadata.create_all(bind=engine)

settings = get_settings()
DEFAULT_PAGE_LIMIT = settings.recipes_page_size

app = FastAPI(
    title="Recipe Manager API",
    description="A simple API for managing recipes",
    version="1.0.0",
)

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
