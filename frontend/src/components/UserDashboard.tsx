import React, { useEffect, useState } from "react";
import { fetchUser, getPlan, getLikedMeals, LikedMeal } from "../services/api";
import type { WeeklyPlanData, UserOut } from "../types";
import { useNavigate } from "react-router-dom";
import { WeeklyPlan } from "./WeeklyPlan";
import { PreferencesModal } from "./PreferencesModal";
import { FavoriteMealsModal } from "./FavoriteMealsModal";

export const UserDashboard: React.FC = () => {
    const username = localStorage.getItem("nutriplan_username") || "";
    const [profile, setProfile] = useState<UserOut | null>(null);
    const [plan, setPlan] = useState<WeeklyPlanData | null>(null);
    const [busy, setBusy] = useState(false);
    const [likedMeals, setLikedMeals] = useState<LikedMeal[]>([]);
    const [ratingFilter, setRatingFilter] = useState(4);
    
    const [isPrefsModalOpen, setPrefsModalOpen] = useState(false);
    const [isFavsModalOpen, setFavsModalOpen] = useState(false);

    const nav = useNavigate();

    useEffect(() => {
        if (!username) { nav("/"); return; }
        fetchUser(username)
            .then(setProfile)
            .catch(() => {
                localStorage.removeItem("nutriplan_username");
                nav("/");
            });
    }, [username, nav]);

    useEffect(() => {
        if (profile) {
            getLikedMeals(profile.id, ratingFilter)
                .then(setLikedMeals)
                .catch(console.error);
        }
    }, [profile, ratingFilter]);

    const generatePlan = async () => {
        if (!profile) return;
        setBusy(true);
        const dietaryPreferences = Object.keys(profile.preferences).filter(k => profile.preferences[k as keyof typeof profile.preferences]);
        try {
            const res = await getPlan({
                user_id: profile.id,
                calorie_target: 2200,
                dietary_preferences: dietaryPreferences,
                allergies: [],
                goal_text: profile.goal_text,
            });
            setPlan(res);
        } finally {
            setBusy(false);
        }
    };

    if (!profile) {
        return <div className="flex justify-center items-center h-screen"><p className="text-lg">Loading profile…</p></div>;
    }

    return (
        <div className="bg-gray-100 min-h-screen">
            <header className="bg-white shadow-sm p-4 sticky top-0 z-40">
                <div className="max-w-screen-xl mx-auto flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">Welcome, {profile.name}!</h1>
                        <p className="text-gray-600 text-sm italic mt-1">
                            <strong>Your Goal:</strong> "{profile.goal_text}"
                        </p>
                    </div>
                    
                    <nav className="flex items-center gap-4">
                        <button onClick={() => setPrefsModalOpen(true)} className="font-semibold text-gray-600 hover:text-blue-600">⚙️ Preferences</button>
                        <button onClick={() => setFavsModalOpen(true)} className="font-semibold text-gray-600 hover:text-blue-600">❤️ Favorites</button>
                        
                        {plan && (
                            <button onClick={generatePlan} disabled={busy} className="font-semibold text-blue-600 hover:text-blue-800 disabled:opacity-50">
                                {busy ? "..." : "🔄 New Plan"}
                            </button>
                        )}

                    </nav>

                    <div className="text-right text-sm text-gray-600 border-l pl-4">
                        <p><strong>Age:</strong> {profile.age}</p>
                        <p><strong>Height:</strong> {profile.height_cm ?? "N/A"} cm</p>
                        <p><strong>Weight:</strong> {profile.weight_kg ?? "N/A"} kg</p>
                    </div>
                </div>
            </header>

            <main className="p-4 sm:p-6 lg:p-8 max-w-screen-xl mx-auto">
                {!plan ? (
                    <div className="text-center flex flex-col justify-center items-center h-[60vh]">
                        <h2 className="text-2xl font-bold text-gray-700 mb-2">Your Plan Awaits</h2>
                        <p className="text-gray-500 mb-6 max-w-md">Click the button to generate your personalized 7-day meal plan based on your goals and preferences.</p>
                        <button onClick={generatePlan} disabled={busy} className="bg-blue-600 text-white font-bold py-3 px-8 rounded-lg text-lg shadow-lg hover:bg-blue-700 transition-transform transform hover:scale-105">
                            {busy ? "Generating…" : "✨ Generate Meal Plan"}
                        </button>
                    </div>
                ) : (
                    <WeeklyPlan plan={plan} userProfile={profile} />
                )}
            </main>

            {isPrefsModalOpen && <PreferencesModal profile={profile} onClose={() => setPrefsModalOpen(false)} />}
            {isFavsModalOpen && <FavoriteMealsModal likedMeals={likedMeals} ratingFilter={ratingFilter} setRatingFilter={setRatingFilter} onClose={() => setFavsModalOpen(false)} />}
        </div>
    );
};