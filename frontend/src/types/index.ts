// C:\Users\jrochau\projects\NutriPlanAI-Published\frontend\src\types\index.ts
export interface PlannedMeal {
  id: number;
  title: string;
  calories: number;
  macros: {
    protein: number;
    fat: number;
    carbs: number;
  };
  ingredients?: string[];
  recipe?: string;
}

export interface DailyPlan {
  breakfast: PlannedMeal | null;
  lunch: PlannedMeal | null;
  dinner: PlannedMeal | null;
}

export type WeeklyPlanData = {
  [day: string]: DailyPlan;
};



export interface PlanRequest {
  user_id: number;
  dietary_preferences?: string[];
  allergies?: string[];
  calorie_target?: number;
  goal_text: string;
}

export interface UserCreatePayload {
  username: string;
  name: string;
  age: number;
  weight_kg?: number;
  height_cm?: number;
  sex?: string;
  activity_level?: string;
  preferences?: { [key: string]: boolean };
  goal_text: string;
}

export interface UserOut {
  id: number;
  username: string;
  name: string;
  age: number;
  weight_kg?: number;
  height_cm?: number;
  sex?: string;
  activity_level?: string;
  preferences: { [key: string]: boolean };
  goal_text: string;
}

export interface DemoPlanResponse {
  before_plan: WeeklyPlanData;
  after_plan: WeeklyPlanData;
}