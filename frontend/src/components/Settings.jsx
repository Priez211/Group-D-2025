import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UserProfile from './UserProfile';
import '../styles/Dashboard.css';
import '../styles/Settings.css';

const Settings = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData) {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleHomeNavigation = () => {
    switch (user?.role) {
      case 'registrar':
        return navigate('/registrar');
      case 'lecturer':
        return navigate('/lecturer-dashboard');
      default:
        return navigate('/dashboard');
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="logo">
          <h1>AITs</h1>
        </div>
        <div className="user-menu">
          <UserProfile user={user} />
        </div>
      </header>

      <div className="dashboard-layout">
        {/* Sidebar Navigation */}
        <nav className="dashboard-nav">
          <ul>
            <li onClick={handleHomeNavigation}>
              <span>🏠</span>
              Home
            </li>
            <li onClick={() => navigate('/notifications')} className="notification-item">
              <span>🔔</span>
              Notifications
            </li>
            <li className="active">
              <span>⚙️</span>
              Settings
            </li>
          </ul>
        </nav>

        <main className="dashboard-main">
          <div className="settings-container">
            <h1>Settings</h1>
            
            <section className="settings-section">
              <h2>Account Settings</h2>
              <div className="settings-info">
                <div className="info-item">
                  <label>Name:</label>
                  <span>{user?.fullName}</span>
                </div>
                <div className="info-item">
                  <label>Email:</label>
                  <span>{user?.email}</span>
                </div>
                <div className="info-item">
                  <label>Role:</label>
                  <span>{user?.role}</span>
                </div>
              </div>
            </section>

            <section className="settings-section">
              <h2>Actions</h2>
              <div className="settings-actions">
                <button onClick={handleLogout} className="logout-button">
                  <span>🚪</span>
                  Logout
                </button>
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Settings; 