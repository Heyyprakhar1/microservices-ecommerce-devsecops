import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/" className="logo">🛍️ E-Shop</Link>
      </div>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/products">Products</Link>
        <Link to="/login">Login</Link>
        <Link to="/register" className="btn-register">Register</Link>  {/* ADD THIS */}
      </div>
    </nav>
  );
};

export default Navbar;

