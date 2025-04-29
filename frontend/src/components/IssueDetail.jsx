//the issue details page
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIssueById } from '../services/api';
import UserProfile from './UserProfile';
import NotificationBadge from './NotificationBadge';
import '../styles/Dashboard.css';
import '../styles/IssueDetail.css';

const IssueDetail = () => {
  const { issueId } = useParams();
  const navigate = useNavigate();
  const [issue, setIssue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [selectedLecturer, setSelectedLecturer] = useState('');
  const [statusUpdate, setStatusUpdate] = useState('');
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [lecturers, setLecturers] = useState([]);
  const [loadingLecturers, setLoadingLecturers] = useState(true);


  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData) {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  useEffect(() => {
    const fetchIssueDetails = async () => {
      try {
        const data = await getIssueById(issueId);
        setIssue(data);
        setError('');
      } catch (err) {
        setError(err.message || 'Failed to load issue details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (issueId) {
      fetchIssueDetails();
    } else {
      setError('No issue ID provided');
      setLoading(false);
    }
  }, [issueId]);

  const handleEditIssue = () => {
    if (!user) {
      navigate('/login');
      return;
    }
    // Check if the user is authorized to edit this issue
    if (issue.student_id === user.id) {
      navigate(`/add-issue/${issueId}`);
    } else {
      setError('You are not authorized to edit this issue.');
    }
  };

  const handleMyIssues = () => {
    navigate('/my-issues');
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div className="logo">
            <span className="graduation-icon">👨‍🎓</span>
            <h1>AITs</h1>
          </div>
          <div className="user-menu">
            <UserProfile user={user} />
          </div>
        </header>
        <div className="loading">Loading issue details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div className="logo">
            <span className="graduation-icon">👨‍🎓</span>
            <h1>AITs</h1>
          </div>
          <div className="user-menu">
            <UserProfile user={user} />
          </div>
        </header>
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => navigate(-1)} className="back-button">
            Back to Issues
          </button>
        </div>
      </div>
    );
  }

  if (!issue) {
    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div className="logo">
            <span className="graduation-icon">👨‍🎓</span>
            <h1>AITs</h1>
          </div>
          <div className="user-menu">
            <UserProfile user={user} />
          </div>
        </header>
        <div className="not-found">
          <h2>Issue Not Found</h2>
          <p>The requested issue could not be found.</p>
          <button onClick={() => navigate(-1)} className="back-button">
            Back to Issues
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="logo">
          <span className="graduation-icon">👨‍🎓</span>
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
            <li onClick={() => navigate('/dashboard')}>
              <span>🏠</span>
              Home
            </li>
            <li onClick={handleMyIssues}>
              <span>📝</span>
              My Issues
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
          <div className="issue-container">
            <h1>Issue Details</h1>
            <p className="subtitle">Detailed view of the selected issue.</p>

            {error && <div className="error-message">{error}</div>}

            <div className="issue-section">
              <h2>Issue Category</h2>
              <p>{issue.category}</p>
            </div>

            <div className="issue-section">
              <h2>Issue Title</h2>
              <p>{issue.title}</p>
            </div>

            <div className="issue-section">
              <h2>Detailed Description</h2>
              <p>{issue.description}</p>
            </div>

            <div className="issue-section">
              <h2>Priority</h2>
              <p>{issue.priority}</p>
            </div>

            <div className="issue-section">
              <h2>Submission Date</h2>
              <p>{new Date(issue.created_at).toLocaleDateString()}</p>
            </div>

            <div className="issue-section">
              <h2>Status</h2>
              <p>{issue.status}</p>
            </div>

            <div className="issue-actions">
              {issue.student_id === user?.id && (
                <button 
                  onClick={handleEditIssue} 
                  className="edit-button"
                >
                  Edit Issue
                </button>
              )}
              <button onClick={() => navigate(-1)} className="back-button">
                Back to Issues
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default IssueDetail; 
