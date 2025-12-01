import axios from 'axios';

const API_BASE_URL = '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const recipeAPI = {
  // Get all recipes
  getRecipes: () => api.get('/recipes/'),
  
  // Get a specific recipe by ID
  getRecipe: (id) => api.get(`/recipes/${id}`),
  
  // Create a new recipe
  createRecipe: (recipe) => api.post('/recipes/', recipe),
  
  // Update an existing recipe
  updateRecipe: (id, recipe) => api.put(`/recipes/${id}`, recipe),
  
  // Delete a recipe
  deleteRecipe: (id) => api.delete(`/recipes/${id}`),
  
  // Search recipes
  searchRecipes: (query) => api.get(`/recipes/search/${query}`),
  
  // Filter recipes by meal type and/or cuisine
  filterRecipes: (params) => {
    const searchParams = new URLSearchParams();
    if (params.meal_type) searchParams.append('meal_type', params.meal_type);
    if (params.cuisine) searchParams.append('cuisine', params.cuisine);
    return api.get(`/recipes/filter/?${searchParams.toString()}`);
  },
  
  // Get unique meal types for filter dropdown
  getMealTypes: () => api.get('/meal-types/'),
  
  // Get unique cuisines for filter dropdown
  getCuisines: () => api.get('/cuisines/'),
};

export default api;