import axios from "axios";
// --- FIX: 'PlannedMeal' has been removed from this import line ---
import type { PlanRequest, WeeklyPlanData, UserOut, UserCreatePayload } from "../types";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api",
});

export function registerUser(payload: UserCreatePayload) {
    return api
        .post<UserOut>("/users", payload)
        .then(res => res.data);
}

export const fetchUserByUsername = async (username: string): Promise<UserOut> => {
    const res = await api.get<UserOut>(`/users/by-username/${encodeURIComponent(username)}`);
    return res.data;
};

export const updateUser = async (id: number, data: UserCreatePayload): Promise<UserOut> => {
    const res = await api.put<UserOut>(`/users/${id}`, data);
    return res.data;
};

export interface DemoPlanResponse {
    before_plan: WeeklyPlanData;
    after_plan: WeeklyPlanData;
}

export const getDemoPlan = async (): Promise<DemoPlanResponse> => {
    const response = await api.post<DemoPlanResponse>("/plan/demo");
    return response.data;
};

export const classifyGoal = async (goalText: string): Promise<any> => {
    const res = await api.post("/classify", { text: goalText });
    return res.data;
};


export const getPlan = async (requestData: PlanRequest): Promise<WeeklyPlanData> => {
    const res = await api.post<WeeklyPlanData>("/plan", requestData);
    return res.data;
};

export interface FeedbackCreatePayload {
    user_id: number;
    meal_id: number;
    rating: number;
    comment?: string;
}

export const submitFeedback = async (payload: FeedbackCreatePayload) => {
    const { data } = await api.post('/feedback', payload);
    return data;
};

export interface LikedMeal {
    id: number;
    title: string;
    rating: number;
}

export const getLikedMeals = async (userId: number, minRating: number): Promise<LikedMeal[]> => {
    const params = { min_rating: minRating };
    const { data } = await api.get<LikedMeal[]>(`/users/${userId}/liked-meals`, { params });
    return data;
};

export const fetchUser = fetchUserByUsername;