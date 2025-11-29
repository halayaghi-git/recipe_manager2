import pytest


class TestAPI:

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200

    def test_recipe_crud_lifecycle(self, client, sample_recipe):
        """Test complete CRUD lifecycle in one test"""
        # CREATE
        create_response = client.post("/recipes/", json=sample_recipe)
        assert create_response.status_code in [200, 201]
        recipe_id = create_response.json()["id"]

        # READ by ID
        get_response = client.get(f"/recipes/{recipe_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == recipe_id

        # UPDATE
        updated_recipe = {**sample_recipe, "title": "Updated Recipe"}
        update_response = client.put(f"/recipes/{recipe_id}", json=updated_recipe)
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Recipe"

        # DELETE
        delete_response = client.delete(f"/recipes/{recipe_id}")
        assert delete_response.status_code == 200
        assert "deleted successfully" in delete_response.json()["message"]

    def test_recipe_not_found_scenarios(self, client, sample_recipe):
        """Test all 404 scenarios in one test"""
        # GET non-existent
        assert client.get("/recipes/999").status_code == 404

        # UPDATE non-existent
        assert client.put("/recipes/999", json=sample_recipe).status_code == 404

        # DELETE non-existent
        assert client.delete("/recipes/999").status_code == 404

    def test_get_recipes_and_pagination(self, client, sample_recipe):
        """Test getting recipes with pagination"""
        # Create a recipe
        client.post("/recipes/", json=sample_recipe)

        # Test get all
        response = client.get("/recipes/")
        assert response.status_code == 200

        # Test with pagination
        paginated = client.get("/recipes/?skip=0&limit=10")
        assert paginated.status_code == 200

    def test_search_functionality(self, client, sample_recipe):
        """Test search endpoint with various scenarios"""
        # Create recipe
        client.post("/recipes/", json=sample_recipe)

        # Test search endpoint exists
        response = client.get("/recipes/search/")
        assert response.status_code in [200, 422]

        # Test search with query
        search_response = client.get("/recipes/search/", params={"query": "Pasta"})
        assert search_response.status_code in [200, 422]

    def test_filter_functionality(self, client, sample_recipe):
        """Test filter endpoint with various scenarios"""
        # Create recipe
        client.post("/recipes/", json=sample_recipe)

        # Test filter endpoint
        response = client.get("/recipes/filter/")
        assert response.status_code in [200, 422]

        # Test filter by cuisine
        cuisine_response = client.get("/recipes/filter/", params={"cuisine": "Italian"})
        assert cuisine_response.status_code in [200, 422]

        # Test filter by meal type
        meal_response = client.get("/recipes/filter/", params={"meal_type": "dinner"})
        assert meal_response.status_code in [200, 422]

    def test_metadata_endpoints(self, client, sample_recipe):
        """Test cuisines and meal-types endpoints"""
        # Test empty state
        cuisines_empty = client.get("/cuisines/")
        assert cuisines_empty.status_code == 200

        meal_types_empty = client.get("/meal-types/")
        assert meal_types_empty.status_code == 200

        # Create recipe and test with data
        client.post("/recipes/", json=sample_recipe)

        cuisines_with_data = client.get("/cuisines/")
        assert cuisines_with_data.status_code == 200

        meal_types_with_data = client.get("/meal-types/")
        assert meal_types_with_data.status_code == 200

    def test_validation_errors(self, client):
        """Test validation error scenarios"""
        # Invalid recipe data
        invalid_recipe = {"title": ""}  # Empty title
        response = client.post("/recipes/", json=invalid_recipe)
        assert response.status_code == 422
