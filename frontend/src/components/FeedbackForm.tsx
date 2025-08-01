import React, { useState } from 'react';
import { submitFeedback } from '../services/api';

interface FeedbackFormProps {
  mealId: number;
  userId: number;
  onFeedbackSubmitted: () => void;
}

export const FeedbackForm: React.FC<FeedbackFormProps> = ({ mealId, userId, onFeedbackSubmitted }) => {
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (rating === 0) {
      alert('Please select a rating before submitting.');
      return;
    }
    setIsSubmitting(true);
    try {
      await submitFeedback({
        user_id: userId,
        meal_id: mealId,
        rating: rating,
        comment: comment,
      });
      onFeedbackSubmitted();
    } catch (error) {
      console.error('Failed to submit feedback', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 p-4 bg-gray-100 rounded-lg">
      <div className="mb-2">
        <p className="text-sm font-semibold text-gray-700 mb-1">Rate this meal:</p>
        <div className="flex items-center">
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              className={`text-2xl cursor-pointer ${
                (hoverRating || rating) >= star ? 'text-yellow-400' : 'text-gray-300'
              }`}
              onClick={() => setRating(star)}
              onMouseEnter={() => setHoverRating(star)}
              onMouseLeave={() => setHoverRating(0)}
            >
              ★
            </span>
          ))}
        </div>
      </div>

      <div className="mb-3">
        <label htmlFor={`comment-${mealId}`} className="text-sm font-semibold text-gray-700">
          Add a comment (optional):
        </label>
        <textarea
          id={`comment-${mealId}`}
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="mt-1 w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          rows={2}
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting || rating === 0}
        className="w-full px-4 py-2 bg-green-600 text-white font-semibold rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
      </button>
    </form>
  );
};