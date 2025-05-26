import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStudentIssues } from '../services/api';
import UserProfile from './UserProfile';
import NotificationBadge from './NotificationBadge';
import '../styles/Dashboard.css';

const MyIssues = () => {
  // State variables
  const navigate = useNavigate();
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);

  // Load user data and issues on component mount
  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData) {
      navigate('/login');
      return;
    }
    setUser(userData);
    fetchIssues();
  }, [navigate]);

  // API Functions
  const fetchIssues = async () => {
    try {
      setLoading(true);
      const data = await getStudentIssues();
      
      // Handle API response
      if (Array.isArray(data)) {
        setIssues(data);
      } else if (data && typeof data === 'object') {
        const issuesArray = data.issues || data.data || [];
        setIssues(issuesArray);
      } else {
        setIssues([]);
      }
      setError('');
    } catch (err) {
      setError('Failed to fetch issues. Please try again later.');
      console.error('Error fetching issues:', err);
    } finally {
      setLoading(false);
    }
  };

  // Navigation handlers
  const handleAddNewIssue = () => navigate('/add-issue');
  const handleIssueClick = (issueId) => {
    if (!issueId) {
      console.error('No issue ID provided');
      return;
    }
    navigate(`/issue/${issueId}`);
  };

  // Helper functions
  const getStatusColor = (status) => {
    const colors = {
      open: 'gray',
      in_progress: 'blue',
      resolved: 'green',
      closed: 'red'
    };
    return colors[status?.toLowerCase()] || 'gray';
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatCategory = (text) => {
    if (!text) return '';
    return text
      .split(/[_\s]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  // Render component
  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="logo">
          <h1>AITs</h1>
        </div>
        <div className="user-menu">
          <UserProfile user={user} />
        </div>
      </header>

      <div className="dashboard-layout">
        {/* Navigation Menu */}
        <nav className="dashboard-nav">
          <ul>
            <li onClick={() => navigate('/dashboard')}>
              <span>Home</span>
            </li>
            <li className="active">
              <span>My Issues</span>
            </li>
            <li onClick={() => navigate('/notifications')} className="notification-item">
              <span>Notifications</span>
              <NotificationBadge />
            </li>
            <li onClick={() => navigate('/settings')}>
              <span>Settings</span>
            </li>
          </ul>
        </nav>

        {/* Main Content */}
        <main className="dashboard-main">
          {/* Page Header */}
          <div className="page-header">
            <h1>My Issues</h1>
            <button className="add-issue-button" onClick={handleAddNewIssue}>
              Add New Issue
            </button>
          </div>
          
          {/* Issues List */}
          <section className="all-issues">
            {loading ? (
              <div className="loading-spinner">Loading...</div>
            ) : error ? (
              <div className="error-message">{error}</div>
            ) : (
              <div className="issues-list">
                {issues.length === 0 ? (
                  // Empty state
                  <div className="no-issues">
                    <p>No issues found.</p>
                    <button className="add-issue-button" onClick={handleAddNewIssue}>
                      Create your first issue
                    </button>
                  </div>
                ) : (
                  // Issues grid
                  issues
                    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    .map((issue) => {
                      const issueId = issue.issue_id || issue._id || issue.id;
                      return (
                        <div 
                          key={issueId} 
                          className="issue-card"
                          onClick={() => handleIssueClick(issueId)}
                        >
                          <div className="issue-content">
                            {/* Issue header */}
                            <div className="issue-header">
                              <h3>{issue.title || formatCategory(issue.category)}</h3>
                              <div className="issue-metadata">
                                <div className={`issue-status-circle ${getStatusColor(issue.status)}`} />
                                <span className="issue-date">{formatDate(issue.created_at)}</span>
                              </div>
                            </div>
                            
                            {/* Issue details */}
                            <p className="issue-description">{issue.description}</p>
                            <div className="issue-status">
                              <span className={`status-badge ${issue.status?.toLowerCase()}`}>
                                {formatCategory(issue.status) || 'Open'}
                              </span>
                            </div>
                          </div>
                        </div>
                      );
                    })
                )}
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
};

export default MyIssues;