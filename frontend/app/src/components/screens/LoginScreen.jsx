import React, { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import axios from "axios";

function LoginScreen() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/auth/login/",
        { username, password },
        { headers: { "Content-Type": "application/json" } }
      );

      // Save JWT Access Token
      localStorage.setItem("token", response.data.access);
      localStorage.setItem("user", username);

      console.log("Login Success:", response.data);

      // Redirect to dashboard after login
      window.location.href = "/";
    } catch (error) {
      console.error("Login Error:", error);
      setErrorMsg("Invalid username or password");
    }

    setUsername("");
    setPassword("");
  };

  return (
    <div className="container" style={{ maxWidth: "450px", marginTop: "50px" }}>
      <h2 className="text-center mb-3">Login</h2>

      {errorMsg && <Alert variant="danger">{errorMsg}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formUsername" className="mb-3">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group controlId="formPassword" className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>

        <Button variant="dark" type="submit" style={{ width: "100%" }}>
          Login
        </Button>
      </Form>

      <p className="text-center mt-3">
        Don't have an account?{" "}
        <a href="/signup" style={{ textDecoration: "none" }}>
          Sign up
        </a>
      </p>
    </div>
  );
}

export default LoginScreen;
