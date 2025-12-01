# in this file we define the database models using SQLAlchemy ORM
# we have recipes.db as our database file

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)

    recipes = relationship("Recipe", back_populates="owner", cascade="all,delete")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    recipes = relationship(
        "Recipe", secondary=recipe_tags, back_populates="tags", lazy="joined"
    )


class Recipe(Base):  # this Recipe class represents the recipes table in the db
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(String)
    cuisine = Column(String, index=True)
    meal_type = Column(String, index=True)
    instructions = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="recipes")
    tags = relationship("Tag", secondary=recipe_tags, back_populates="recipes")
