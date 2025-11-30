# schemas.py - Fix Pydantic v2 config
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    cuisine: Optional[str] = None
    meal_type: Optional[str] = None
    owner_id: Optional[int] = None


class RecipeCreate(RecipeBase):
    tags: list[str] = Field(default_factory=list)


class Recipe(RecipeBase):
    id: int
    tags: list[Tag] = Field(default_factory=list)
    owner: Optional[User] = None

    model_config = ConfigDict(from_attributes=True)


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
