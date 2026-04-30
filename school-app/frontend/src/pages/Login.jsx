import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) { setError(data.detail); return; }
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("email", email);
    navigate("/dashboard");
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input placeholder="School email" value={email}
          onChange={e => setEmail(e.target.value)} style={styles.input} />
        <input type="password" placeholder="Password" value={password}
          onChange={e => setPassword(e.target.value)} style={styles.input} />
        {error && <p style={styles.error}>{error}</p>}
        <button type="submit" style={styles.button}>Login</button>
      </form>
      <p>No account? <Link to="/register">Register</Link></p>
    </div>
  );
}

const styles = {
  container: { maxWidth: 400, margin: "100px auto", textAlign: "center", fontFamily: "sans-serif" },
  form: { display: "flex", flexDirection: "column", gap: 12 },
  input: { padding: "10px", fontSize: 16, borderRadius: 6, border: "1px solid #ccc" },
  button: { padding: "10px", background: "#4f46e5", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 16 },
  error: { color: "red" }
};
