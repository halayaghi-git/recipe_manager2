# in this file we define the database models using SQLAlchemy ORM
# we have recipes.db as our database file

from sqlalchemy import Column, Integer, String
from database import Base


class Recipe(Base):  # this Recipe class represents the recipes table in the db
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(String)
    cuisine = Column(String, index=True)
    meal_type = Column(String, index=True)
    instructions = Column(String)
