import React, { useState } from "react";
import { registerUser, fetchUserByUsername } from "../services/api";
import { useNavigate } from "react-router-dom";
import axios from "axios";

type Step = 0 | 1 | 2 | 3;

export const LandingPage: React.FC = () => {
    const nav = useNavigate();

    const [username, setUsername] = useState("");
    const [loginError, setLoginError] = useState<string | null>(null);

    const [step, setStep] = useState<Step>(0);
    const [name, setName] = useState("");
    const [age, setAge] = useState<number | "">("");
    const [weight, setWeight] = useState<number | "">("");
    const [height, setHeight] = useState<number | "">("");
    const [sex, setSex] = useState("other");
    const [activity, setAct] = useState("sedentary");
    const [prefs, setPrefs] = useState<{ [k: string]: boolean }>({});
    const [goal, setGoal] = useState("");

    const togglePref = (p: string) =>
        setPrefs((prev) => ({ ...prev, [p]: !prev[p] }));

    const handleLogin = async (loginUsername: string) => {
        setLoginError(null);
        if (!loginUsername.trim()) {
            setLoginError("Please enter a username.");
            return;
        }
        try {
            const user = await fetchUserByUsername(loginUsername.trim());
            localStorage.setItem("nutriplan_username", user.username);
            nav(`/dashboard/${encodeURIComponent(user.username)}`);
        } catch {
            setLoginError("User not found. Please register or use the demo login.");
        }
    };

    const next = () => setStep((s) => (s + 1) as Step);
    const back = () => setStep((s) => (s - 1) as Step);

    const finish = async () => {
        try {
            const user = await registerUser({
                username, name, age: Number(age),
                weight_kg: weight === "" ? undefined : Number(weight),
                height_cm: height === "" ? undefined : Number(height),
                sex, activity_level: activity, preferences: prefs, goal_text: goal,
            });
            localStorage.setItem("nutriplan_username", user.username);
            nav(`/dashboard/${encodeURIComponent(user.username)}`);
        } catch (error) {
            console.error("Registration failed:", error);
            if (axios.isAxiosError(error)) {
                if (error.response) {
                    alert(`Error: ${error.response.data.detail || "Server error"}`);
                } else if (error.request) {
                    alert("Could not connect to the server. Please ensure the backend is running.");
                } else {
                    alert("An error occurred while setting up the request.");
                }
            } else {
                alert("An unexpected error occurred.");
            }
        }
    };

    const canProceed = () => {
        if (step === 0) return username.trim() !== "" && name.trim() !== "" && age !== "" && Number(age) >= 13;
        if (step === 1) return weight !== "" && height !== "";
        if (step === 2) return true;
        if (step === 3) return goal.trim() !== "";
        return false;
    };

    const inputCls = "w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500";
    const btnPrimary = "bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-40";
    const btnGhost = "px-4 py-2 text-blue-600 hover:underline";

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <h1 className="text-4xl font-bold mb-8 text-center text-blue-700">NutriPlan AI</h1>
            <div className="bg-white shadow-md rounded-lg p-6 mb-8 w-full max-w-sm">
                <h2 className="text-xl font-semibold mb-4">Log In</h2>
                <input
                    className={inputCls}
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                {loginError && <div className="text-red-500 text-sm mb-2">{loginError}</div>}
                
                <button
                    className={`${btnPrimary} w-full mb-2`}
                    onClick={() => handleLogin(username)}
                >
                    Log In
                </button>

                <button
                    className="w-full text-sm text-blue-600 hover:underline"
                    onClick={() => handleLogin("demo_user")}
                >
                    Or, log in as a Demo User
                </button>
            </div>

            <div className="bg-white shadow-lg rounded-lg w-full max-w-lg p-8">
                <div className="mb-6 text-sm text-gray-500">Or Register - Step {step + 1} / 4</div>
                {step === 0 && (
                    <>
                        <h2 className="text-xl font-semibold mb-4">Basic Info</h2>
                        <input className={inputCls} placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                        <input className={inputCls} placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                        <input className={inputCls} type="number" placeholder="Age" value={age} onChange={(e) => setAge(e.target.value === "" ? "" : Number(e.target.value))} />
                        <div className="flex justify-end">
                            <button className={btnPrimary} disabled={!canProceed()} onClick={next}>Next</button>
                        </div>
                    </>
                )}
                {step === 1 && (
                    <>
                        <h2 className="text-xl font-semibold mb-4">Body Metrics</h2>
                        <input className={inputCls} type="number" placeholder="Weight (kg)" value={weight} onChange={(e) => setWeight(e.target.value === "" ? "" : Number(e.target.value))} />
                        <input className={inputCls} type="number" placeholder="Height (cm)" value={height} onChange={(e) => setHeight(e.target.value === "" ? "" : Number(e.target.value))} />
                        <select className={inputCls} value={sex} onChange={(e) => setSex(e.target.value)}>
                            <option value="other">Sex (choose)</option>
                            <option value="female">Female</option>
                            <option value="male">Male</option>
                            <option value="nonbinary">Non-binary</option>
                        </select>
                        <div className="flex justify-between mt-4">
                            <button className={btnGhost} onClick={back}>Back</button>
                            <button className={btnPrimary} disabled={!canProceed()} onClick={next}>Next</button>
                        </div>
                    </>
                )}
                {step === 2 && (
                    <>
                        <h2 className="text-xl font-semibold mb-4">Lifestyle & Preferences</h2>
                        <select className={inputCls} value={activity} onChange={(e) => setAct(e.target.value)}>
                            <option value="sedentary">Sedentary</option>
                            <option value="lightly_active">Lightly Active</option>
                            <option value="moderately_active">Moderately Active</option>
                            <option value="very_active">Very Active</option>
                        </select>
                        <h3 className="font-medium mt-4 mb-2">Dietary Preferences</h3>
                        {["vegetarian", "vegan", "gluten_free", "dairy_free", "no_red_meat"].map((p) => (
                            <label key={p} className="block mb-1"><input type="checkbox" checked={!!prefs[p]} onChange={() => togglePref(p)} className="mr-2" />{p.replace(/_/g, " ")}</label>
                        ))}
                        <div className="flex justify-between mt-4">
                            <button className={btnGhost} onClick={back}>Back</button>
                            <button className={btnPrimary} onClick={next}>Next</button>
                        </div>
                    </>
                )}
                {step === 3 && (
                    <>
                        <h2 className="text-xl font-semibold mb-4">Primary Goal</h2>
                        <textarea className={`${inputCls} h-28 resize-none`} placeholder="E.g. I want to build lean muscle…" value={goal} onChange={(e) => setGoal(e.target.value)} />
                        <div className="flex justify-between mt-4">
                            <button className={btnGhost} onClick={back}>Back</button>
                            <button className={btnPrimary} disabled={!canProceed()} onClick={finish}>Create Profile</button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};