import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaQuestionCircle, FaUsers, FaCog } from 'react-icons/fa';
import '../static/css/RegistrarDashboard.css';

const RegistrarDashboard = () => {
  const [activeFilter, setActiveFilter] = useState('All');
  
  const issues = [
    {
      id: 1,
      issue: 'Mark issue',
      status: 'Open',
      priority: 'High',
      submissionDate: 'Jan 14'
    },
    {
      id: 2,
      issue: 'GRM-560',
      status: 'Open',
      priority: 'Low',
      submissionDate: 'Jul 29'
    },
    {
      id: 3,
      issue: 'SYS-301',
      status: 'Open',
      priority: 'Medium',
      submissionDate: 'Sep 12'
    },
    {
      id: 4,
      issue: 'QA-482',
      status: 'Open',
      priority: 'High',
      submissionDate: 'Oct 20'
    },
    {
      id: 5,
      issue: 'UX-578',
      status: 'Open',
      priority: 'Low',
      submissionDate: 'Nov 1'
    }
  ];

  const filters = ['All', 'Pending', 'Resolved', 'High Priority', 'Medium Priority', 'Low Priority'];

  return (
    <div className="registrar-dashboard">
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
            <Link to="/registrar-dashboard" className="nav-item active">
              <FaHome />
              <span>Home</span>
            </Link>
            <Link to="/registrar-issues" className="nav-item">
              <FaQuestionCircle />
              <span>Issues</span>
            </Link>
            <Link to="/registrar-students" className="nav-item">
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
            <h1>Registrar's Dashboard</h1>
          </div>

          <section className="issues-section">
            <h2>Issues</h2>
            <p className="subtitle">All reported issues are listed below.</p>
            
            <div className="filter-tabs">
              {filters.map(filter => (
                <button
                  key={filter}
                  className={`filter-tab ${activeFilter === filter ? 'active' : ''}`}
                  onClick={() => setActiveFilter(filter)}
                >
                  {filter}
                </button>
              ))}
            </div>

            <div className="issues-table">
              <table>
                <thead>
                  <tr>
                    <th>Issue</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Submission Date</th>
                    <th>Actions</th>
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

export default RegistrarDashboard; 
