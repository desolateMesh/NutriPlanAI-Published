import React, { useState } from "react";
import { getDemoPlan } from "../services/api";
import type { DemoPlanResponse } from "../types";
import { WeeklyPlan } from "./WeeklyPlan";

export const DemoMealPage: React.FC = () => {
    const [demoData, setDemoData] = useState<DemoPlanResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const runDemo = async () => {
        setIsLoading(true);
        setError(null);
        setDemoData(null);
        try {
            const data = await getDemoPlan();
            setDemoData(data);
        } catch (err) {
            setError("Failed to run demo. Please ensure the backend is running.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-8 bg-gray-50 min-h-screen">
            <header className="text-center mb-10">
                <h1 className="text-4xl font-bold text-gray-800">Feedback Loop Demo</h1>
                <p className="text-gray-600 mt-2">
                    This demonstrates how the meal planner adapts to user feedback.
                </p>
                <button
                    onClick={runDemo}
                    disabled={isLoading}
                    className="mt-6 bg-blue-600 text-white font-bold py-3 px-8 rounded-lg text-lg shadow-lg hover:bg-blue-700 disabled:opacity-50"
                >
                    {isLoading ? "Running Simulation..." : "🚀 Run Live Demo"}
                </button>
            </header>

            {error && <div className="text-center text-red-500 font-semibold">{error}</div>}
            
            {demoData && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    <div>
                        <h2 className="text-2xl font-bold text-center mb-4">Plan #1 (Before Feedback)</h2>
                        <p className="text-center mb-4 text-sm text-gray-500">A plan generated for a new user with no ratings.</p>
                        <WeeklyPlan plan={demoData.before_plan} userProfile={null} />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-center mb-4">Plan #2 (After Feedback)</h2>
                        <p className="text-center mb-4 text-sm text-gray-500">Simulated loving 'chicken' and hating 'salmon'. Note the changes.</p>
                        <WeeklyPlan plan={demoData.after_plan} userProfile={null} />
                    </div>
                </div>
            )}
        </div>
    );
};