import React, { useState } from "react";
import "./App.css";
import DocumentParser from "./DocumentParser";

const ADMIN_EMAIL = "admin@gmail.com";
const ADMIN_ID = "admin";
const ADMIN_PASSWORD = "admin@123";

function App() {
  const [mode, setMode] = useState("signin");
  const [email, setEmail] = useState("");
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedInUser, setLoggedInUser] = useState(null);

  const resetForm = () => {
    setEmail("");
    setUserId("");
    setPassword("");
    setMessage("");
  };

  const handleSignIn = (e) => {
    e.preventDefault();
    if (
      (email === ADMIN_EMAIL || userId === ADMIN_ID) &&
      password === ADMIN_PASSWORD
    ) {
      setLoggedInUser({ email: ADMIN_EMAIL, userId: ADMIN_ID, role: "admin" });
      setMessage("");
    } else {
      setMessage("Invalid credentials");
    }
  };

  const handleSignUp = (e) => {
    e.preventDefault();
    setMessage("Signup is demo only. Use admin credentials to sign in.");
  };

  const handleGoogleLogin = () => {
    setLoggedInUser({
      email: "google.user@example.com",
      userId: "googleUser",
      role: "user",
    });
    setMessage("");
  };

  const handleGithubLogin = () => {
    setLoggedInUser({
      email: "github.user@example.com",
      userId: "githubUser",
      role: "user",
    });
    setMessage("");
  };

  const handleLogout = () => {
    setLoggedInUser(null);
    resetForm();
  };

  // If logged in, show your main project UI
  if (loggedInUser) {
    return (
      <div>
        {/* Compact Header with Logout */}
        <div
          style={{
            background:
              "linear-gradient(90deg, #4A90E2 0%, #7B68EE 50%, #FF6B9D 100%)",
            padding: "12px 20px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            position: "sticky",
            top: 0,
            zIndex: 100,
          }}
        >
          <div style={{ color: "white", fontSize: "14px", fontWeight: "500" }}>
            👤 {loggedInUser.userId}
          </div>
          <button
            onClick={handleLogout}
            style={{
              background: "rgba(255, 255, 255, 0.25)",
              color: "white",
              border: "1px solid rgba(255, 255, 255, 0.4)",
              padding: "6px 16px",
              borderRadius: "20px",
              cursor: "pointer",
              fontSize: "13px",
              fontWeight: "500",
              transition: "all 0.3s",
            }}
            onMouseEnter={(e) => {
              e.target.style.background = "rgba(255, 255, 255, 0.35)";
            }}
            onMouseLeave={(e) => {
              e.target.style.background = "rgba(255, 255, 255, 0.25)";
            }}
          >
            Logout
          </button>
        </div>

        {/* Main Content */}
        <DocumentParser />
      </div>
    );
  }

  // Otherwise show login / signup page
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}
    >
      <div
        style={{
          background: "white",
          borderRadius: "16px",
          padding: "40px",
          maxWidth: "420px",
          width: "100%",
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.15)",
        }}
      >
        <h1
          style={{
            margin: "0 0 10px 0",
            fontSize: "1.8rem",
            textAlign: "center",
            background:
              "linear-gradient(90deg, #4A90E2 0%, #7B68EE 50%, #FF6B9D 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          LexScan-Auto
        </h1>
        <p
          style={{
            textAlign: "center",
            color: "#999",
            marginBottom: "30px",
            fontSize: "14px",
          }}
        >
          Financial Document Parser
        </p>

        <div
          style={{
            display: "flex",
            marginBottom: "24px",
            borderRadius: "999px",
            background: "#f0f2f5",
            padding: "4px",
            gap: "0",
          }}
        >
          <button
            onClick={() => {
              setMode("signin");
              resetForm();
            }}
            style={{
              flex: 1,
              border: "none",
              background:
                mode === "signin"
                  ? "linear-gradient(90deg, #4A90E2 0%, #7B68EE 100%)"
                  : "transparent",
              color: mode === "signin" ? "white" : "#666",
              padding: "10px 0",
              borderRadius: "999px",
              cursor: "pointer",
              fontWeight: "500",
              transition: "all 0.3s",
            }}
          >
            Sign In
          </button>
          <button
            onClick={() => {
              setMode("signup");
              resetForm();
            }}
            style={{
              flex: 1,
              border: "none",
              background:
                mode === "signup"
                  ? "linear-gradient(90deg, #FF8A80 0%, #FF6B9D 100%)"
                  : "transparent",
              color: mode === "signup" ? "white" : "#666",
              padding: "10px 0",
              borderRadius: "999px",
              cursor: "pointer",
              fontWeight: "500",
              transition: "all 0.3s",
            }}
          >
            Sign Up
          </button>
        </div>

        {mode === "signin" && (
          <form
            onSubmit={handleSignIn}
            style={{ display: "flex", flexDirection: "column", gap: "12px" }}
          >
            <div>
              <label
                style={{
                  fontSize: "12px",
                  color: "#666",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Email or User ID
              </label>
              <input
                type="text"
                placeholder="admin or admin@gmail.com"
                value={userId || email}
                onChange={(e) => {
                  setUserId(e.target.value);
                  setEmail(e.target.value);
                }}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  fontSize: "14px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#4A90E2")}
                onBlur={(e) => (e.target.style.borderColor = "#ddd")}
              />
            </div>
            <div>
              <label
                style={{
                  fontSize: "12px",
                  color: "#666",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Password
              </label>
              <input
                type="password"
                placeholder="admin@123"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  fontSize: "14px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#4A90E2")}
                onBlur={(e) => (e.target.style.borderColor = "#ddd")}
              />
            </div>
            <button
              type="submit"
              style={{
                marginTop: "8px",
                width: "100%",
                padding: "11px",
                border: "none",
                borderRadius: "8px",
                background: "linear-gradient(90deg, #4A90E2 0%, #7B68EE 100%)",
                color: "white",
                fontWeight: "600",
                fontSize: "15px",
                cursor: "pointer",
                transition: "all 0.3s",
              }}
              onMouseEnter={(e) =>
                (e.target.style.transform = "translateY(-2px)")
              }
              onMouseLeave={(e) => (e.target.style.transform = "translateY(0)")}
            >
              Sign In
            </button>
          </form>
        )}

        {mode === "signup" && (
          <form
            onSubmit={handleSignUp}
            style={{ display: "flex", flexDirection: "column", gap: "12px" }}
          >
            <div>
              <label
                style={{
                  fontSize: "12px",
                  color: "#666",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                User ID
              </label>
              <input
                type="text"
                placeholder="Choose a user id"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  fontSize: "14px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#FF6B9D")}
                onBlur={(e) => (e.target.style.borderColor = "#ddd")}
              />
            </div>
            <div>
              <label
                style={{
                  fontSize: "12px",
                  color: "#666",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Email
              </label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  fontSize: "14px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#FF6B9D")}
                onBlur={(e) => (e.target.style.borderColor = "#ddd")}
              />
            </div>
            <div>
              <label
                style={{
                  fontSize: "12px",
                  color: "#666",
                  display: "block",
                  marginBottom: "6px",
                }}
              >
                Password
              </label>
              <input
                type="password"
                placeholder="Choose a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  fontSize: "14px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border 0.3s",
                }}
                onFocus={(e) => (e.target.style.borderColor = "#FF6B9D")}
                onBlur={(e) => (e.target.style.borderColor = "#ddd")}
              />
            </div>
            <button
              type="submit"
              style={{
                marginTop: "8px",
                width: "100%",
                padding: "11px",
                border: "none",
                borderRadius: "8px",
                background: "linear-gradient(90deg, #FF8A80 0%, #FF6B9D 100%)",
                color: "white",
                fontWeight: "600",
                fontSize: "15px",
                cursor: "pointer",
                transition: "all 0.3s",
              }}
              onMouseEnter={(e) =>
                (e.target.style.transform = "translateY(-2px)")
              }
              onMouseLeave={(e) => (e.target.style.transform = "translateY(0)")}
            >
              Sign Up
            </button>
          </form>
        )}

        <div
          style={{
            display: "flex",
            alignItems: "center",
            margin: "20px 0 14px",
            fontSize: "13px",
            color: "#999",
          }}
        >
          <div style={{ flex: 1, height: "1px", background: "#e0e0e0" }}></div>
          <span style={{ padding: "0 8px" }}>or continue with</span>
          <div style={{ flex: 1, height: "1px", background: "#e0e0e0" }}></div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          <button
            onClick={handleGoogleLogin}
            style={{
              width: "100%",
              padding: "9px 14px",
              border: "1px solid #e0e0e0",
              borderRadius: "8px",
              background: "white",
              color: "#333",
              fontSize: "13px",
              fontWeight: "500",
              cursor: "pointer",
              transition: "all 0.3s",
            }}
            onMouseEnter={(e) => {
              e.target.style.background = "#f8f9fa";
              e.target.style.borderColor = "#4A90E2";
            }}
            onMouseLeave={(e) => {
              e.target.style.background = "white";
              e.target.style.borderColor = "#e0e0e0";
            }}
          >
            🔵 Google
          </button>
          <button
            onClick={handleGithubLogin}
            style={{
              width: "100%",
              padding: "9px 14px",
              border: "1px solid #e0e0e0",
              borderRadius: "8px",
              background: "white",
              color: "#333",
              fontSize: "13px",
              fontWeight: "500",
              cursor: "pointer",
              transition: "all 0.3s",
            }}
            onMouseEnter={(e) => {
              e.target.style.background = "#f8f9fa";
              e.target.style.borderColor = "#7B68EE";
            }}
            onMouseLeave={(e) => {
              e.target.style.background = "white";
              e.target.style.borderColor = "#e0e0e0";
            }}
          >
            ⚫ GitHub
          </button>
        </div>

        {message && (
          <p
            style={{
              marginTop: "14px",
              fontSize: "13px",
              color: "#FF6B9D",
              textAlign: "center",
              background: "#FFF5F7",
              padding: "10px",
              borderRadius: "6px",
            }}
          >
            {message}
          </p>
        )}

        <div
          style={{
            marginTop: "16px",
            padding: "12px",
            background: "#F5F7FF",
            borderRadius: "8px",
            fontSize: "12px",
            color: "#666",
          }}
        >
          <strong style={{ color: "#4A90E2" }}>Demo Credentials:</strong>
          <div>
            ID:{" "}
            <code
              style={{
                background: "white",
                padding: "1px 4px",
                borderRadius: "3px",
              }}
            >
              admin
            </code>
          </div>
          <div>
            Pass:{" "}
            <code
              style={{
                background: "white",
                padding: "1px 4px",
                borderRadius: "3px",
              }}
            >
              admin@123
            </code>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
