from typing import List

import crud
from config import Settings
from schemas import RecipeCreate


def _make_recipe_payload(
    title: str,
    cuisine: str = "Cuisine",
    meal_type: str = "dinner",
) -> RecipeCreate:
    return RecipeCreate(
        title=title,
        ingredients=f"ingredients for {title}",
        instructions=f"instructions for {title}",
        cuisine=cuisine,
        meal_type=meal_type,
    )


def _create_service(db_session) -> crud.RecipeService:
    repository = crud.RecipeRepository(db_session)
    return crud.RecipeService(repository)


def _list_titles(recipes: List) -> List[str]:
    return [recipe.title for recipe in recipes]


def test_repository_crud_roundtrip(db_session):
    repository = crud.RecipeRepository(db_session)
    payload = _make_recipe_payload("Repo Flow")

    created = repository.create(payload.model_dump())
    assert created.id is not None

    fetched = repository.get(created.id)
    assert fetched.title == "Repo Flow"

    listing = repository.list(skip=0, limit=10)
    assert _list_titles(listing) == ["Repo Flow"]

    repository.delete(created)
    assert repository.get(created.id) is None


def test_repository_search_is_case_insensitive(db_session):
    repository = crud.RecipeRepository(db_session)
    repository.create(_make_recipe_payload("SPICY CURRY", cuisine="Thai").model_dump())

    results = repository.search("spicy")
    assert len(results) == 1
    assert results[0].title == "SPICY CURRY"


def test_service_respects_default_page_size(monkeypatch, db_session):
    monkeypatch.setattr(crud, "settings", Settings(recipes_page_size=1))

    service = _create_service(db_session)
    service.create(_make_recipe_payload("First"))
    service.create(_make_recipe_payload("Second"))

    default_page = service.list(limit=None)
    assert len(default_page) == 1

    specific_limit = service.list(limit=5)
    assert len(specific_limit) == 2


def test_service_filter_unique_and_update_flow(db_session):
    service = _create_service(db_session)

    breakfast = service.create(
        _make_recipe_payload("Pancakes", cuisine="American", meal_type="breakfast")
    )
    service.create(_make_recipe_payload("Sushi", cuisine="Japanese", meal_type="lunch"))

    breakfast_results = service.filter(meal_type="breakfast")
    assert _list_titles(breakfast_results) == ["Pancakes"]

    cuisines = {item[0] for item in service.get_unique_cuisines()}
    assert {"American", "Japanese"}.issubset(cuisines)

    update_payload = _make_recipe_payload(
        "Pancakes Deluxe", cuisine="American", meal_type="brunch"
    )
    updated = service.update(breakfast.id, update_payload)
    assert updated.meal_type == "brunch"

    deleted = service.delete(breakfast.id)
    assert deleted.title == "Pancakes Deluxe"
    assert service.get(breakfast.id) is None
