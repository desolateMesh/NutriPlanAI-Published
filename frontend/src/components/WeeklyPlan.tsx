import React, { useState } from 'react';
import type { WeeklyPlanData, PlannedMeal, UserOut } from '../types';
import { FeedbackForm } from './FeedbackForm';
import { MealDetailModal } from './MealDetailModal';

const MealCard: React.FC<{
    meal: PlannedMeal | null;
    mealType: string;
    userId?: number;
    onClick: () => void;
}> = ({ meal, mealType, userId, onClick }) => {
    const [showFeedback, setShowFeedback] = useState(false);

    if (!meal) {
        return (
            <div className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 opacity-50">
                <h4 className="font-semibold text-gray-500 capitalize">{mealType}</h4>
                <p className="text-gray-400 italic">No meal planned.</p>
            </div>
        );
    }

    const handleFeedbackSuccess = () => {
        setShowFeedback(false);
    };

    return (
        <div
            onClick={onClick}
            className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 cursor-pointer hover:shadow-md hover:border-blue-400 transition-all"
        >
            <div className="flex justify-between items-start">
                <div>
                    <h4 className="font-semibold text-gray-600 capitalize">{mealType}</h4>
                    <p className="text-gray-800 font-medium" title={meal.title}>{meal.title}</p>
                </div>
                {userId && (
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            setShowFeedback(!showFeedback);
                        }}
                        className="text-xs text-blue-600 hover:text-blue-800 font-semibold z-10"
                        aria-expanded={showFeedback}
                    >
                        {showFeedback ? 'Cancel' : 'Rate'}
                    </button>
                )}
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-2">
                <span>🔥 {meal.calories} kcal</span>
                <div className="flex gap-2">
                    <span>P: {meal.macros.protein}g</span>
                    <span>F: {meal.macros.fat}g</span>
                    <span>C: {meal.macros.carbs}g</span>
                </div>
            </div>
            {showFeedback && userId && (

                <div onClick={(e) => e.stopPropagation()}>
                    <FeedbackForm
                        mealId={meal.id}
                        userId={userId}
                        onFeedbackSubmitted={handleFeedbackSuccess}
                    />
                </div>
            )}
        </div>
    );
};

export const WeeklyPlan: React.FC<{ plan: WeeklyPlanData; userProfile?: UserOut | null }> = ({ plan, userProfile }) => {
    const [selectedMeal, setSelectedMeal] = useState<PlannedMeal | null>(null);
    const dailyPlans = Object.entries(plan);

    if (!dailyPlans || dailyPlans.length === 0) {
        return <p className="text-center text-gray-500">Sorry, we couldn't generate a plan. Please try again.</p>;
    }

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <h2 className="text-3xl lg:text-4xl font-extrabold text-center text-gray-800 mb-8">Your 7-Day Meal Plan</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {dailyPlans.map(([day, dayPlan]) => (
                    <div key={day} className="bg-gray-50 p-5 rounded-xl border-2 border-gray-200 flex flex-col transform transition-transform hover:scale-105 hover:shadow-lg">
                        <h3 className="text-2xl font-bold text-gray-700 mb-4 capitalize">{day}</h3>
                        <div className="space-y-3">
                            <MealCard meal={dayPlan.breakfast} mealType="breakfast" userId={userProfile?.id} onClick={() => setSelectedMeal(dayPlan.breakfast)} />
                            <MealCard meal={dayPlan.lunch} mealType="lunch" userId={userProfile?.id} onClick={() => setSelectedMeal(dayPlan.lunch)} />
                            <MealCard meal={dayPlan.dinner} mealType="dinner" userId={userProfile?.id} onClick={() => setSelectedMeal(dayPlan.dinner)} />
                        </div>
                    </div>
                ))}
            </div>

            {selectedMeal && (
                <MealDetailModal
                    meal={selectedMeal}
                    onClose={() => setSelectedMeal(null)}
                />
            )}
        </div>
    );
};