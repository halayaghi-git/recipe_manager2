from sqlalchemy.orm import Session

from models import Recipe


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
