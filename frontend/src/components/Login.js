import React, { useState } from 'react';
import { authAPI } from '../services/api';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await authAPI.post('/login', {email, password});
      localStorage.setItem('token', response.data.token);
      setMessage('Login successful! ✅');
    } catch (error) {
      setMessage('Login failed! ❌');
      console.error(error);
    }
  };

  // NEW: Handle Google Login
  const handleGoogleLogin = () => {
    // Redirect to your backend's Google OAuth endpoint
    window.location.href = '/api/auth/google';
  };

  return (
    <div className="login-container">
      <h2>Welcome Back! 👋</h2>
      
      {/* Google Login Button - NEW */}
      <button 
        className="btn-google" 
        onClick={handleGoogleLogin}
        type="button"
      >
        <img 
          src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" 
          alt="Google" 
          className="google-icon"
        />
        Continue with Google
      </button>

      <div className="divider">
        <span>OR</span>
      </div>

      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="btn-primary">Login with Email</button>
      </form>
      
      {message && <p className="message">{message}</p>}
      
      <p className="register-link">
        Don't have an account? <a href="/register">Register here</a>
      </p>
    </div>
  );
};

export default Login;
