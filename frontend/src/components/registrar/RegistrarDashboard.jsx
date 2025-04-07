import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';

const RegistrarDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'registrar') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="logo">
          <span className="graduation-icon">👨‍💼</span>
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
            <li className="active">
              <span>🏠</span>
              Home
            </li>
            <li onClick={() => navigate('/registrar/students')}>
              <span>👨‍🎓</span>
              Students
            </li>
            <li onClick={() => navigate('/registrar/lecturers')}>
              <span>👨‍🏫</span>
              Lecturers
            </li>
            <li onClick={() => navigate('/registrar/departments')}>
              <span>🏛️</span>
              Departments
            </li>
            <li onClick={() => navigate('/registrar/issues')}>
              <span>📝</span>
              Issues
            </li>
            <li onClick={() => navigate('/notifications')} className="notification-item">
              <span>🔔</span>
              Notifications
              <NotificationBadge />
            </li>
            <li>
              <span>⚙️</span>
              Settings
            </li>
          </ul>
        </nav>

        {/* Main Content */}
        <main className="dashboard-main">
          <h1 className="welcome-message">Welcome back, {user?.fullName?.split(' ')[0] || 'Registrar'}!</h1>
          
          <section className="quick-actions">
            <h2>Quick Actions</h2>
            <div className="actions-grid">
              <div className="action-card" onClick={() => navigate('/registrar/students')}>
                <span className="action-icon">👨‍🎓</span>
                <h3>Manage Students</h3>
                <p>View and manage student records</p>
              </div>
              <div className="action-card" onClick={() => navigate('/registrar/lecturers')}>
                <span className="action-icon">👨‍🏫</span>
                <h3>Manage Lecturers</h3>
                <p>View and manage lecturer profiles</p>
              </div>
              <div className="action-card" onClick={() => navigate('/registrar/departments')}>
                <span className="action-icon">🏛️</span>
                <h3>Departments</h3>
                <p>Manage academic departments</p>
              </div>
              <div className="action-card notification-item" onClick={() => navigate('/notifications')}>
                <span className="action-icon">🔔</span>
                <h3>Notifications</h3>
                <p>View updates and alerts</p>
                <NotificationBadge />
              </div>
            </div>
          </section>
          
          <section className="statistics-section">
            <h2>System Overview</h2>
            <div className="statistics-grid">
              <div className="stat-card">
                <h3>Total Students</h3>
                <p className="stat-number">1,245</p>
              </div>
              <div className="stat-card">
                <h3>Total Lecturers</h3>
                <p className="stat-number">87</p>
              </div>
              <div className="stat-card">
                <h3>Departments</h3>
                <p className="stat-number">12</p>
              </div>
              <div className="stat-card">
                <h3>Open Issues</h3>
                <p className="stat-number">24</p>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default RegistrarDashboard; 