import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { isLoggedIn } from './api';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

function PrivateRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />;
}

function PublicRoute({ children }) {
  // If already logged in, send to dashboard
  return isLoggedIn() ? <Navigate to="/dashboard" replace /> : children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/login" element={
          <PublicRoute><Login /></PublicRoute>
        } />

        <Route path="/register" element={
          <PublicRoute><Register /></PublicRoute>
        } />

        <Route path="/dashboard" element={
          <PrivateRoute><Dashboard /></PrivateRoute>
        } />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
