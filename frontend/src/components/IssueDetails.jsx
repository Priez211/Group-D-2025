import React from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { FaHome, FaQuestionCircle, FaUsers, FaCog, FaGraduationCap } from 'react-icons/fa';
import '../static/css/IssueDetails.css';

const IssueDetails = ({ userRole = 'lecturer' }) => {
  const { issueId } = useParams();
  const navigate = useNavigate();

  // This would normally come from your API/backend
  const issueDetails = {
    issue: 'Missing marks',
    issueTitle: 'Missing marks',
    detailedDescription: 'My marks for coursework and mid-semester exams are missing but i did them',
    priority: 'High',
    submissionDate: 'Jun 21',
    status: 'Open'
  };

  const handleResolveIssue = () => {
    // Handle issue resolution logic here
    console.log('Resolving issue:', issueId);
  };

  const handleBackToIssues = () => {
    const route = userRole === 'lecturer' ? '/lecturer-dashboard' : 
                 userRole === 'registrar' ? '/registrar-dashboard' : '/dashboard';
    navigate(route);
  };

  return (
    <div className="issue-details-page">
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

      <div className="page-content">
        <aside className="sidebar">
          <nav className="side-nav">
            <Link to="/dashboard" className="nav-item">
              <FaHome />
              <span>Home</span>
            </Link>
            <Link to="/issues" className="nav-item active">
              <FaQuestionCircle />
              <span>Issues</span>
            </Link>
            <Link to="/students" className="nav-item">
              <FaUsers />
              <span>Students</span>
            </Link>
            <Link to="/settings" className="nav-item">
              <FaCog />
              <span>Settings</span>
            </Link>
          </nav>
        </aside>

        <main className="main-content">
          <div className="content-header">
            <h1>Issue Details</h1>
            <p className="subtitle">Detailed view of the selected issue.</p>
          </div>

          <div className="issue-details">
            <div className="detail-group">
              <h2>Issue</h2>
              <p>{issueDetails.issue}</p>
            </div>

            <div className="detail-group">
              <h2>Issue Title</h2>
              <p>{issueDetails.issueTitle}</p>
            </div>

            <div className="detail-group">
              <h2>Detailed Description</h2>
              <p>{issueDetails.detailedDescription}</p>
            </div>

            <div className="detail-group">
              <h2>Priority</h2>
              <span className={`priority-badge ${issueDetails.priority.toLowerCase()}`}>
                {issueDetails.priority}
              </span>
            </div>

            <div className="detail-group">
              <h2>Submission Date</h2>
              <p>{issueDetails.submissionDate}</p>
            </div>

            <div className="detail-group">
              <h2>Status</h2>
              <span className={`status-badge ${issueDetails.status.toLowerCase()}`}>
                {issueDetails.status}
              </span>
            </div>

            <div className="action-buttons">
              {(userRole === 'lecturer' || userRole === 'registrar') && (
                <button 
                  className="resolve-button"
                  onClick={handleResolveIssue}
                >
                  Resolve Issue
                </button>
              )}
              <button 
                className="back-button"
                onClick={handleBackToIssues}
              >
                Back to Issues
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default IssueDetails; 