from sqlalchemy.orm import Session

from models import Recipe, Tag, User


class TestModels:

    def test_recipe_model_comprehensive(self, db_session: Session):
        """Test Recipe model creation with all scenarios"""
        # Test with all fields
        recipe = Recipe(
            title="Model Test Recipe",
            ingredients="test ingredients",
            instructions="test instructions",
            cuisine="Test Cuisine",
            meal_type="test_meal",
        )

        db_session.add(recipe)
        db_session.commit()
        db_session.refresh(recipe)

        assert recipe.id is not None
        assert recipe.title == "Model Test Recipe"

        # Test with minimal fields (optional fields as None)
        minimal_recipe = Recipe(
            title="Minimal Recipe",
            ingredients="minimal ingredients",
            instructions="minimal instructions",
        )

        db_session.add(minimal_recipe)
        db_session.commit()

        assert minimal_recipe.id is not None
        assert minimal_recipe.cuisine is None
        assert minimal_recipe.meal_type is None

    def test_user_and_tag_relationships(self, db_session: Session):
        user = User(email="model@example.com", name="Model User")
        vegan = Tag(name="vegan")
        quick = Tag(name="quick")
        db_session.add_all([user, vegan, quick])
        db_session.commit()

        recipe = Recipe(
            title="Tagged Recipe",
            ingredients="test",
            instructions="test",
            owner_id=user.id,
        )
        recipe.tags.extend([vegan, quick])
        db_session.add(recipe)
        db_session.commit()
        db_session.refresh(recipe)

        assert recipe.owner.id == user.id
        assert {tag.name for tag in recipe.tags} == {"vegan", "quick"}
