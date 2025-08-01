// src/components/GoalInput.tsx
import React, { useEffect, useState } from 'react';
import type { WeeklyPlanData } from '../types';
import { classifyGoal, getPlan } from '../services/api';

interface GoalInputProps {
  onPlanGenerated: (plan: WeeklyPlanData) => void;
  userGoal: string;
}

export const GoalInput: React.FC<GoalInputProps> = ({ onPlanGenerated, userGoal }) => {
  const [_isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const classifiedGoal = await classifyGoal(userGoal);
        console.log("Classified Goal:", classifiedGoal);

        const planRequest = {
          user_id: Number(localStorage.getItem("nutriplan_user_id")),
          goal_text: userGoal,
          calorie_target: 2200,
          dietary_preferences: [],
          allergies: [],
        };

        const finalPlan = await getPlan(planRequest);
        onPlanGenerated(finalPlan);
      } catch (err) {
        console.error("Error generating plan:", err);
        alert("Something went wrong generating your plan.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchPlan();
  }, [userGoal, onPlanGenerated]);

  return (
    <div className="p-8 max-w-lg mx-auto bg-white rounded-xl shadow-md text-center">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Generating Your Plan...</h2>
      <p className="text-gray-600">Based on your goal: <strong>{userGoal}</strong></p>
      <div className="mt-4 animate-pulse text-blue-500">Loading personalized plan...</div>
    </div>
  );
};