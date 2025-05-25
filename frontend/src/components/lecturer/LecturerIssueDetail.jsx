import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getIssueById, updateIssueStatus } from '../../services/api';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';
import '../../styles/Lecturer.css';

const LecturerIssueDetail = () => {
  const { issueId } = useParams();
  const navigate = useNavigate();
  const [issue, setIssue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'lecturer') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  useEffect(() => {
    fetchIssueDetails();
  }, [issueId]);

  const fetchIssueDetails = async () => {
    try {
      const data = await getIssueById(issueId);
      setIssue(data);
      setError('');
    } catch (err) {
      console.error('Error fetching issue details:', err);
      setError('Failed to fetch issue details. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (newStatus) => {
    try {
      await updateIssueStatus(issueId, newStatus);
      await fetchIssueDetails();
    } catch (err) {
      setError('Failed to update issue status. Please try again.');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="logo">
          <h1>AITs</h1>
        </div>
        <div className="user-menu">
          <UserProfile user={user} onLogout={handleLogout} />
        </div>
      </header>

      <div className="dashboard-layout">
        <nav className="dashboard-nav">
          <ul>
            <li onClick={() => navigate('/lecturer')}>
              <span>🏠</span>
              Dashboard
            </li>
            <li onClick={() => navigate('/lecturer/issues')}>
              <span>📝</span>
              Manage Issues
            </li>
            <li onClick={() => navigate('/lecturer/notifications')}>
              <span>🔔</span>
              Notifications
              <NotificationBadge />
            </li>
            <li onClick={() => navigate('/lecturer/settings')}>
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
          ) : issue ? (
            <div className="issue-detail-container">
              <div className="issue-detail-header">
                <button className="back-button" onClick={() => navigate('/lecturer/issues')}>
                  ← Back to Issues
                </button>
                <h1>{issue.title}</h1>
                <div className="issue-meta">
                  <span className={`status-badge ${issue.status?.toLowerCase()}`}>
                    {issue.status}
                  </span>
                  <span className={`priority-badge ${issue.priority?.toLowerCase()}`}>
                    {issue.priority}
                  </span>
                </div>
              </div>

              <div className="issue-detail-content">
                <div className="issue-info-section">
                  <div className="info-group">
                    <label>Submitted by:</label>
                    <p>{issue.student?.fullName || 'N/A'}</p>
                  </div>
                  <div className="info-group">
                    <label>Course Unit:</label>
                    <p>{issue.courseUnit}</p>
                  </div>
                  <div className="info-group">
                    <label>Submitted on:</label>
                    <p>{formatDate(issue.created_at)}</p>
                  </div>
                  <div className="info-group">
                    <label>Last updated:</label>
                    <p>{formatDate(issue.updated_at)}</p>
                  </div>
                </div>

                <div className="issue-description-section">
                  <h2>Description</h2>
                  <p>{issue.description}</p>
                </div>

                {issue.attachment && (
                  <div className="issue-attachment-section">
                    <h2>Attachments</h2>
                    <a href={issue.attachment} target="_blank" rel="noopener noreferrer" className="attachment-link">
                      📎 View Attachment
                    </a>
                  </div>
                )}

                <div className="issue-actions-section">
                  <h2>Take Action</h2>
                  <div className="action-buttons">
                    <button
                      className={`action-button ${issue.status === 'open' ? 'active' : ''}`}
                      onClick={() => handleStatusUpdate('open')}
                    >
                      Mark as Open
                    </button>
                    <button
                      className={`action-button ${issue.status === 'in_progress' ? 'active' : ''}`}
                      onClick={() => handleStatusUpdate('in_progress')}
                    >
                      Mark In Progress
                    </button>
                    <button
                      className={`action-button ${issue.status === 'resolved' ? 'active' : ''}`}
                      onClick={() => handleStatusUpdate('resolved')}
                    >
                      Mark as Resolved
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="error-message">Issue not found</div>
          )}
        </main>
      </div>
    </div>
  );
};

export default LecturerIssueDetail; 