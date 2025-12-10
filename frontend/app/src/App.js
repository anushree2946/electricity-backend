import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/screens/Home";
import Header from "./components/Header";
import EditApplicant from "./components/screens/EditApplicant";
import Stats from "./components/screens/Stats";
import LoginScreen from "./components/screens/LoginScreen";
import Signup from "./components/screens/Signup";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/editApplicant/:id" element={<EditApplicant />} />
        <Route path="/StatisticsCollection" element={<Stats />} />
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
