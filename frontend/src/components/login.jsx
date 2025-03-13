import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaGraduationCap, FaUser, FaChalkboardTeacher, FaUserTie } from 'react-icons/fa';
import '../static/css/Login.css';

const Login = () => {
  const [selectedRole, setSelectedRole] = useState('student');
  const [studentNumber, setStudentNumber] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here
  };

  return (
    <div className="login-page">
      <nav className="top-nav">
        <div className="nav-logo">
          <Link to="/">
            <FaGraduationCap className="logo-icon" />
            <span>AITs</span>
          </Link>
        </div>
        <div className="nav-profile">
          <Link to="/profile">
            <img src="/profile-placeholder.png" alt="Profile" />
          </Link>
        </div>
      </nav>

      <main className="login-content">
        <div className="login-card">
          <h1>Welcome</h1>
          
          <div className="role-tabs">
            <button
              className={`role-tab ${selectedRole === 'student' ? 'active' : ''}`}
              onClick={() => setSelectedRole('student')}
            >
              <FaUser className="role-icon" />
              <span>Student</span>
            </button>
            <button
              className={`role-tab ${selectedRole === 'lecturer' ? 'active' : ''}`}
              onClick={() => setSelectedRole('lecturer')}
            >
              <FaChalkboardTeacher className="role-icon" />
              <span>Lecturer</span>
            </button>
            <button
              className={`role-tab ${selectedRole === 'registrar' ? 'active' : ''}`}
              onClick={() => setSelectedRole('registrar')}
            >
              <FaUserTie className="role-icon" />
              <span>Registrar</span>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="studentNumber">Student number</label>
              <input
                type="text"
                id="studentNumber"
                value={studentNumber}
                onChange={(e) => setStudentNumber(e.target.value)}
                placeholder="2400721333"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <Link to="/forgot-password" className="forgot-password">
              Forgot your username or password?
            </Link>

            <button type="submit" className="login-button">
              Log In
            </button>
          </form>
        </div>
      </main>
    </div>
  );
};

export default Login; 
