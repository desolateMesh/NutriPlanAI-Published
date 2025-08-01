// frontend/src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./components/LandingPage";
import { UserDashboard } from "./components/UserDashboard";

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard/:username" element={<UserDashboard />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
