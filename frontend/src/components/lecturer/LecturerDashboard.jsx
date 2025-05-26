import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getLecturerIssues } from '../../services/api';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';
import '../../styles/Lecturer.css';

const API_URL = 'http://localhost:8000';

const LecturerDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'lecturer') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    setLoading(true);
    try {
      const data = await getLecturerIssues();
      setIssues(Array.isArray(data) ? data : data.issues || []);
      setError('');
    } catch (err) {
      console.error('Error fetching issues:', err);
      setError('Failed to fetch issues. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusClass = (status) => {
    if (!status) return 'unknown';
    return status.toLowerCase().replace(/\s+/g, '_');
  };

  const filteredIssues = issues.filter(issue => {
    if (filter === 'all') return true;
    return issue.status?.toLowerCase() === filter;
  }).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="logo">
          <h1>AITs - Lecturer Dashboard</h1>
        </div>
        <div className="user-menu">
          <UserProfile user={user} />
        </div>
      </header>

      <div className="dashboard-layout">
        <nav className="dashboard-nav">
          <ul>
            <li className="active">
              <span>🏠</span>
              Home
            </li>
            <li onClick={() => navigate('/lecturer/issues')}>
              <span>📝</span>
              Issues
            </li>
            <li onClick={() => navigate('/lecturer/notifications')} className="notification-item">
              <span>🔔</span>
              Notifications
              <NotificationBadge />
            </li>
            <li onClick={() => navigate('/settings')}>
              <span>⚙️</span>
              Settings
            </li>
          </ul>
        </nav>

        <main className="dashboard-main">
          {loading ? (
            <div className="loading-spinner">Loading...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : (
            <>
              <div className="welcome-section">
                <h2>Welcome, {user?.first_name || 'Lecturer'}</h2>
                <p>Here's an overview of issues assigned to you</p>
              </div>

              <div className="dashboard-stats">
                <div className="stat-card">
                  <div className="stat-header">
                    <h3>Total Issues</h3>
                    <span className="stat-number">{issues.length}</span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <h3>Open Issues</h3>
                    <span className="stat-number">
                      {issues.filter(issue => issue.status?.toLowerCase() === 'open').length}
                    </span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <h3>In Progress</h3>
                    <span className="stat-number">
                      {issues.filter(issue => issue.status?.toLowerCase() === 'in_progress').length}
                    </span>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <h3>Resolved</h3>
                    <span className="stat-number">
                      {issues.filter(issue => issue.status?.toLowerCase() === 'resolved').length}
                    </span>
                  </div>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default LecturerDashboard; 
