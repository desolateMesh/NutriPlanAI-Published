// frontend/src/components/FavoriteMealsModal.tsx
import React from 'react';
import type { LikedMeal } from '../services/api';

interface FavoriteMealsModalProps {
  likedMeals: LikedMeal[];
  ratingFilter: number;
  setRatingFilter: (rating: number) => void;
  onClose: () => void;
}

export const FavoriteMealsModal: React.FC<FavoriteMealsModalProps> = ({ likedMeals, ratingFilter, setRatingFilter, onClose }) => {
  return (
    <div 
      onClick={onClose} 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
    >
      <div 
        onClick={(e) => e.stopPropagation()} 
        className="bg-white rounded-lg shadow-xl w-full max-w-lg p-6 m-4"
      >
        <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-800">❤️ Your Favorite Meals</h2>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-800 text-3xl font-bold">&times;</button>
        </div>

        <div className="flex items-center mb-4">
          <span className="text-sm font-medium mr-2">Show meals rated:</span>
          <div className="flex">
            {[5, 4, 3].map(rating => (
              <button key={rating} onClick={() => setRatingFilter(rating)} className={`px-3 py-1 text-sm border rounded-sm ${ratingFilter === rating ? 'bg-blue-600 text-white' : 'bg-white'}`}>
                {rating}★+
              </button>
            ))}
          </div>
        </div>

        <div className="max-h-80 overflow-y-auto pr-2 border-t pt-4">
          {likedMeals.length > 0 ? (
            <ul className="space-y-2 text-gray-600 list-disc list-inside">
              {likedMeals.map(meal => (
                <li key={meal.id} className="truncate" title={meal.title}>
                  {meal.title} ({meal.rating}★)
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic text-center py-4">Rate some meals {ratingFilter} stars or higher to see them here!</p>
          )}
        </div>
      </div>
    </div>
  );
};