import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const email = localStorage.getItem("email");
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div style={{ maxWidth: 600, margin: "100px auto", textAlign: "center", fontFamily: "sans-serif" }}>
      <h1>Welcome, {email} 👋</h1>
      <button onClick={logout} style={{ marginTop: 20, padding: "10px 20px", background: "#ef4444", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer" }}>
        Logout
      </button>
    </div>
  );
}
