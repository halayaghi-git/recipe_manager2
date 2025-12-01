import React, { useState, useEffect } from 'react';
import { recipeAPI } from '../services/api';
import './RecipeFilters.css';

const RecipeFilters = ({ onFilter, onClear }) => {
  const [mealTypes, setMealTypes] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [selectedMealType, setSelectedMealType] = useState('');
  const [selectedCuisine, setSelectedCuisine] = useState('');

  useEffect(() => {
    fetchFilterOptions();
  }, []);

  const fetchFilterOptions = async () => {
    try {
      const [mealTypesResponse, cuisinesResponse] = await Promise.all([
        recipeAPI.getMealTypes(),
        recipeAPI.getCuisines()
      ]);
      
      setMealTypes(mealTypesResponse.data);
      setCuisines(cuisinesResponse.data);
    } catch (error) {
      console.error('Error fetching filter options:', error);
    }
  };

  const handleFilter = () => {
    const filters = {};
    if (selectedMealType) filters.meal_type = selectedMealType;
    if (selectedCuisine) filters.cuisine = selectedCuisine;
    
    onFilter(filters);
  };

  const handleClear = () => {
    setSelectedMealType('');
    setSelectedCuisine('');
    onClear();
  };

  return (
    <div className="recipe-filters">
      <div className="filter-section">
        <h3>Filter Recipes</h3>
        <div className="filter-row">
          <div className="filter-group">
            <label htmlFor="meal-type">Meal Type:</label>
            <select
              id="meal-type"
              value={selectedMealType}
              onChange={(e) => setSelectedMealType(e.target.value)}
            >
              <option value="">All Meal Types</option>
              {(Array.isArray(mealTypes) ? mealTypes : []).map((type, index) => (
                <option key={index} value={type.value}>
                  {type.value}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="cuisine">Cuisine:</label>
            <select
              id="cuisine"
              value={selectedCuisine}
              onChange={(e) => setSelectedCuisine(e.target.value)}
            >
              <option value="">All Cuisines</option>
              {(Array.isArray(cuisines) ? cuisines : []).map((cuisine, index) => (
                <option key={index} value={cuisine.value}>
                  {cuisine.value}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="filter-actions">
          <button 
            className="filter-btn" 
            onClick={handleFilter}
            disabled={!selectedMealType && !selectedCuisine}
          >
            Apply Filters
          </button>
          <button 
            className="clear-btn" 
            onClick={handleClear}
            disabled={!selectedMealType && !selectedCuisine}
          >
            Clear Filters
          </button>
        </div>

        {(selectedMealType || selectedCuisine) && (
          <div className="active-filters">
            <span>Active filters:</span>
            {selectedMealType && (
              <span className="filter-tag">
                Meal Type: {selectedMealType}
                <button onClick={() => setSelectedMealType('')}>×</button>
              </span>
            )}
            {selectedCuisine && (
              <span className="filter-tag">
                Cuisine: {selectedCuisine}
                <button onClick={() => setSelectedCuisine('')}>×</button>
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeFilters;