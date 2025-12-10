import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [message, setMessage] = useState(null);

  // Handle field changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle Form Submit
  const handleSignup = async (e) => {
    e.preventDefault();

    if (!formData.username || !formData.password) {
      setMessage("⚠ Please fill all required fields.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/register/",
        formData,
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      setMessage("✔ Account created successfully!");

      setTimeout(() => {
        navigate("/login");
      }, 1500);

    } catch (error) {
      setMessage(error.response?.data?.error || "❌ Signup failed. Try again.");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "420px", marginTop: "60px" }}>
      <h2 className="text-center mb-4">Create Your Account</h2>

      {message && (
        <div className="alert alert-warning text-center p-2">{message}</div>
      )}

      <form onSubmit={handleSignup}>
        <div className="mb-3">
          <label className="form-label fw-bold">Username</label>
          <input
            type="text"
            name="username"
            className="form-control"
            placeholder="Enter username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label className="form-label fw-bold">Password</label>
          <input
            type="password"
            name="password"
            className="form-control"
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>

        <button type="submit" className="btn btn-dark w-100">
          Sign Up
        </button>
      </form>

      <p className="text-center mt-3">
        Already have an account?{" "}
        <Link to="/login" style={{ textDecoration: "none" }}>
          Login here
        </Link>
      </p>
    </div>
  );
}
