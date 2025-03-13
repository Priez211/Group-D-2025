import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaGraduationCap, FaUser, FaChalkboardTeacher, FaUserTie } from 'react-icons/fa';
import '../static/css/SignUp.css';

const SignUp = () => {
  const [selectedRole, setSelectedRole] = useState('student');
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    studentNumber: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Password match validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    // If we pass password validation, submit the form
    console.log('Form Submitted with: ', formData);
    setError(''); // Reset error if successful submission
  };

  return (
    <div className="signup-page">
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

      <main className="signup-content">
        <div className="signup-card">
          <h1>Create Account</h1>
          
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

          {error && <p className="error-message">{error}</p>}  {/* Display error message */}

          <form onSubmit={handleSubmit} className="signup-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            {selectedRole === 'student' && (
              <div className="form-group">
                <label htmlFor="studentNumber">Student Number</label>
                <input
                  type="text"
                  id="studentNumber"
                  name="studentNumber"
                  value={formData.studentNumber}
                  onChange={handleChange}
                  placeholder="2400721333"
                  required
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>

            <button type="submit" className="signup-button">
              Create Account
            </button>

            <p className="login-link">
              Already have an account? <Link to="/login">Sign in</Link>
            </p>
          </form>
        </div>
      </main>
    </div>
  );
};

export default SignUp;

