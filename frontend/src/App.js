import React, { useState, useEffect } from 'react';
import './App.css';
import { recipeAPI } from './services/api';
import RecipeCard from './components/RecipeCard';
import RecipeForm from './components/RecipeForm';
import RecipeDetail from './components/RecipeDetail';
import RecipeFilters from './components/RecipeFilters';

function App() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingRecipe, setEditingRecipe] = useState(null);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilters, setActiveFilters] = useState({});
  const [isFiltered, setIsFiltered] = useState(false);

  // Fetch recipes on component mount
  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      const response = await recipeAPI.getRecipes();
      setRecipes(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch recipes. Make sure the backend server is running.');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRecipe = async (recipeData) => {
    try {
      const response = await recipeAPI.createRecipe(recipeData);
      setRecipes([response.data, ...recipes]);
      setShowForm(false);
      setError(null);
    } catch (err) {
      setError('Failed to create recipe');
      console.error('Error creating recipe:', err);
    }
  };

  const handleUpdateRecipe = async (recipeData) => {
    try {
      const response = await recipeAPI.updateRecipe(editingRecipe.id, recipeData);
      setRecipes(recipes.map(recipe => 
        recipe.id === editingRecipe.id ? response.data : recipe
      ));
      setEditingRecipe(null);
      setShowForm(false);
      setSelectedRecipe(null);
      setError(null);
    } catch (err) {
      setError('Failed to update recipe');
      console.error('Error updating recipe:', err);
    }
  };

  const handleDeleteRecipe = async (recipeId) => {
    if (!window.confirm('Are you sure you want to delete this recipe?')) {
      return;
    }

    try {
      await recipeAPI.deleteRecipe(recipeId);
      setRecipes(recipes.filter(recipe => recipe.id !== recipeId));
      setSelectedRecipe(null);
      setError(null);
    } catch (err) {
      setError('Failed to delete recipe');
      console.error('Error deleting recipe:', err);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      // If no search query, return to filtered results or all recipes
      if (isFiltered) {
        handleFilter(activeFilters);
      } else {
        fetchRecipes();
      }
      return;
    }

    try {
      setLoading(true);
      const response = await recipeAPI.searchRecipes(searchQuery);
      setRecipes(response.data);
      // Clear filters when searching
      setActiveFilters({});
      setIsFiltered(false);
      setError(null);
    } catch (err) {
      setError('Failed to search recipes');
      console.error('Error searching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditRecipe = (recipe) => {
    setEditingRecipe(recipe);
    setShowForm(true);
    setSelectedRecipe(null);
  };

  const handleSaveRecipe = (recipeData) => {
    if (editingRecipe) {
      handleUpdateRecipe(recipeData);
    } else {
      handleCreateRecipe(recipeData);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingRecipe(null);
  };

  const handleFilter = async (filters) => {
    try {
      setLoading(true);
      const response = await recipeAPI.filterRecipes(filters);
      setRecipes(response.data);
      setActiveFilters(filters);
      setIsFiltered(true);
      setSearchQuery(''); // Clear search when filtering
      setError(null);
    } catch (err) {
      setError('Failed to filter recipes');
      console.error('Error filtering recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearFilters = () => {
    setActiveFilters({});
    setIsFiltered(false);
    fetchRecipes();
  };

  const filteredRecipes = Array.isArray(recipes) ? recipes : [];

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍳 Recipe Manager</h1>
        <div className="header-actions">
          <div className="search-container">
            <input
              type="text"
              placeholder="Search recipes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button onClick={handleSearch} className="search-btn">Search</button>
            <button onClick={() => {
              setSearchQuery('');
              if (isFiltered) {
                handleFilter(activeFilters);
              } else {
                fetchRecipes();
              }
            }} className="clear-btn">Clear Search</button>
          </div>
          <button 
            onClick={() => setShowForm(true)}
            className="add-recipe-btn"
          >
            Add Recipe
          </button>
        </div>
      </header>

      <main className="App-main">
        <RecipeFilters 
          onFilter={handleFilter}
          onClear={handleClearFilters}
        />
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">Loading recipes...</div>
        ) : (
          <div className="recipes-container">
            {filteredRecipes.length === 0 ? (
              <div className="no-recipes">
                <p>
                  No recipes found. 
                  {searchQuery && ' Try a different search term or'}
                  {isFiltered && ' Try different filter options or'}
                  {!searchQuery && !isFiltered && ' Add your first recipe to get started!'}
                  {(searchQuery || isFiltered) && ' clear your search/filters to see all recipes.'}
                </p>
              </div>
            ) : (
              <div className="recipes-grid">
                {filteredRecipes.map(recipe => (
                  <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onEdit={handleEditRecipe}
                    onDelete={handleDeleteRecipe}
                    onClick={setSelectedRecipe}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {showForm && (
        <RecipeForm
          recipe={editingRecipe}
          onSave={handleSaveRecipe}
          onCancel={handleCancelForm}
        />
      )}

      {selectedRecipe && (
        <RecipeDetail
          recipe={selectedRecipe}
          onClose={() => setSelectedRecipe(null)}
          onEdit={handleEditRecipe}
        />
      )}
    </div>
  );
}

export default App;
