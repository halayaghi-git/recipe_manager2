# schemas.py - Fix Pydantic v2 config
from pydantic import BaseModel, ConfigDict
from typing import Optional


class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    cuisine: Optional[str] = None
    meal_type: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # Replace old Config class


# # in this file i define the schemas (data validation)
# from pydantic import BaseModel

# class RecipeBase(BaseModel): # this is a class that is like the base of a recipe
#     title: str
#     ingredients: str
#     cuisine: str
#     meal_type: str
#     instructions: str

# class RecipeCreate(RecipeBase): # to create a new recipe, we refer to the base class
#     pass

# class Recipe(RecipeBase): # to read a recipe from the db, refer to base class schema and id
#     id: int
#     class Config:
#         from_attributes = True
