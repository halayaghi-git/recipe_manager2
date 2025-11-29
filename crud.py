from sqlalchemy import or_
from sqlalchemy.orm import Session

from config import get_settings
from models import Recipe
from schemas import RecipeCreate

settings = get_settings()


class RecipeRepository:
    """Handles persistence for Recipe entities."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, recipe_id: int):
        return self._db.get(Recipe, recipe_id)

    def list(self, skip: int, limit: int):
        return self._db.query(Recipe).offset(skip).limit(limit).all()

    def create(self, payload: dict):
        recipe = Recipe(**payload)
        self._db.add(recipe)
        self._db.commit()
        self._db.refresh(recipe)
        return recipe

    def update(self, recipe: Recipe, payload: dict):
        for field, value in payload.items():
            setattr(recipe, field, value)
        self._db.commit()
        self._db.refresh(recipe)
        return recipe

    def delete(self, recipe: Recipe):
        self._db.delete(recipe)
        self._db.commit()
        return recipe

    def search(self, query: str):
        like_pattern = f"%{query}%"
        return (
            self._db.query(Recipe)
            .filter(
                or_(
                    Recipe.title.ilike(like_pattern),
                    Recipe.cuisine.ilike(like_pattern),
                    Recipe.meal_type.ilike(like_pattern),
                    Recipe.ingredients.ilike(like_pattern),
                )
            )
            .all()
        )

    def filter(self, meal_type: str | None = None, cuisine: str | None = None):
        query = self._db.query(Recipe)
        if meal_type:
            query = query.filter(Recipe.meal_type == meal_type)
        if cuisine:
            query = query.filter(Recipe.cuisine == cuisine)
        return query.all()

    def list_unique(self, column):
        return self._db.query(column).distinct().all()


class RecipeService:
    """Business logic orchestration for recipe operations."""

    def __init__(self, repository: RecipeRepository) -> None:
        self._repository = repository

    def get(self, recipe_id: int):
        return self._repository.get(recipe_id)

    def list(self, skip: int = 0, limit: int | None = None):
        resolved_limit = limit if limit is not None else settings.recipes_page_size
        return self._repository.list(skip=skip, limit=resolved_limit)

    def create(self, recipe: RecipeCreate):
        return self._repository.create(recipe.model_dump())

    def update(self, recipe_id: int, recipe: RecipeCreate):
        existing = self._repository.get(recipe_id)
        if existing is None:
            return None
        return self._repository.update(existing, recipe.model_dump())

    def delete(self, recipe_id: int):
        existing = self._repository.get(recipe_id)
        if existing is None:
            return None
        return self._repository.delete(existing)

    def search(self, query: str):
        return self._repository.search(query)

    def filter(self, meal_type: str | None = None, cuisine: str | None = None):
        return self._repository.filter(meal_type=meal_type, cuisine=cuisine)

    def get_unique_meal_types(self):
        return self._repository.list_unique(Recipe.meal_type)

    def get_unique_cuisines(self):
        return self._repository.list_unique(Recipe.cuisine)


def _service(db: Session) -> RecipeService:
    return RecipeService(RecipeRepository(db))


def get_recipe(db: Session, recipe_id: int):
    return _service(db).get(recipe_id)


def get_recipes(db: Session, skip: int = 0, limit: int | None = None):
    return _service(db).list(skip=skip, limit=limit)


def create_recipe(db: Session, recipe: RecipeCreate):
    return _service(db).create(recipe)


def update_recipe(db: Session, recipe_id: int, recipe: RecipeCreate):
    return _service(db).update(recipe_id, recipe)


def delete_recipe(db: Session, recipe_id: int):
    return _service(db).delete(recipe_id)


def search_recipes(db: Session, query: str):
    return _service(db).search(query)


def filter_recipes(
    db: Session, meal_type: str | None = None, cuisine: str | None = None
):
    return _service(db).filter(meal_type=meal_type, cuisine=cuisine)


def get_unique_meal_types(db: Session):
    return _service(db).get_unique_meal_types()


def get_unique_cuisines(db: Session):
    return _service(db).get_unique_cuisines()
