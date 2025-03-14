import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaQuestionCircle, FaUsers, FaCog } from 'react-icons/fa';
import '../static/css/LecturerDashboard.css';

const LecturerDashboard = () => {
  const issues = [
    {
      id: 1,
      issue: 'Mark Issue',
      status: 'Pending',
      priority: 'High',
      submissionDate: 'Jun 14'
    },
    {
      id: 2,
      issue: 'Request for a re-do',
      status: 'Resolved',
      priority: 'Low',
      submissionDate: 'Jul 29'
    },
    {
      id: 3,
      issue: 'Wrong marks',
      status: 'Pending',
      priority: 'Medium',
      submissionDate: 'Sep 12'
    },
    {
      id: 4,
      issue: 'Missing mark',
      status: 'Pending',
      priority: 'High',
      submissionDate: 'Oct 20'
    }
  ];

  return (
    <div className="lecturer-dashboard">
      <nav className="top-nav">
        <div className="nav-logo">
          <Link to="/">
            <img src="/graduation-cap.png" alt="AiTs Logo" className="logo-icon" />
            <span>AiTs</span>
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
            <Link to="/lecturer-dashboard" className="nav-item active">
              <FaHome />
              <span>Home</span>
            </Link>
            <Link to="/lecturer-issues" className="nav-item">
              <FaQuestionCircle />
              <span>Issues</span>
            </Link>
            <Link to="/lecturer-students" className="nav-item">
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
          <div className="dashboard-header">
            <h1>Lecturer Dashboard</h1>
          </div>

          <section className="issues-section">
            <h2>Issues</h2>
            <div className="filter-tabs">
              <button className="filter-tab active">All</button>
            </div>

            <div className="issues-table">
              <table>
                <thead>
                  <tr>
                    <th>Issue</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Submission Date</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {issues.map(issue => (
                    <tr key={issue.id}>
                      <td>{issue.issue}</td>
                      <td>
                        <span className={`status-badge ${issue.status.toLowerCase()}`}>
                          {issue.status}
                        </span>
                      </td>
                      <td>
                        <span className={`priority-badge ${issue.priority.toLowerCase()}`}>
                          {issue.priority}
                        </span>
                      </td>
                      <td>{issue.submissionDate}</td>
                      <td>
                        <Link to={`/issue/${issue.id}`} className="view-details">
                          View details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default LecturerDashboard; 
