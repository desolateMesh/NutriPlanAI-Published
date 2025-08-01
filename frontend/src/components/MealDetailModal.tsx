// frontend/src/components/MealDetailModal.tsx
import React from 'react';
import type { PlannedMeal } from '../types';

interface MealDetailModalProps {
  meal: PlannedMeal;
  onClose: () => void;
}

export const MealDetailModal: React.FC<MealDetailModalProps> = ({ meal, onClose }) => {
  const ingredients = meal.ingredients || ['Ingredient data not available yet.'];
  const recipe = meal.recipe || 'Recipe data not available yet.';

  return (
    <div 
      onClick={onClose} 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-8 m-4"
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-3xl font-bold text-gray-800">{meal.title}</h2>
          <button 
            onClick={onClose} 
            className="text-gray-500 hover:text-gray-800 text-3xl font-bold"
            aria-label="Close modal"
          >
            &times;
          </button>
        </div>

        <div className="flex justify-around bg-gray-50 p-4 rounded-lg text-center mb-6">
          <div>
            <span className="text-2xl font-bold text-blue-600">{meal.calories}</span>
            <span className="text-sm text-gray-600 block">Calories</span>
          </div>
          <div>
            <span className="text-2xl font-bold text-blue-600">{meal.macros.protein}g</span>
            <span className="text-sm text-gray-600 block">Protein</span>
          </div>
          <div>
            <span className="text-2xl font-bold text-blue-600">{meal.macros.fat}g</span>
            <span className="text-sm text-gray-600 block">Fat</span>
          </div>
          <div>
            <span className="text-2xl font-bold text-blue-600">{meal.macros.carbs}g</span>
            <span className="text-sm text-gray-600 block">Carbs</span>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-700 mb-3 border-b-2 border-gray-200 pb-2">Ingredients</h3>
          <ul className="list-disc list-inside space-y-2 text-gray-600">
            {ingredients.map((item, index) => <li key={index}>{item}</li>)}
          </ul>
        </div>
        
        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-3 border-b-2 border-gray-200 pb-2">Directions</h3>
          <div className="prose max-w-none text-gray-600">
            <p>{recipe}</p>
          </div>
        </div>
      </div>
    </div>
  );
};