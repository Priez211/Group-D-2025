import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaPlus, FaBell, FaCog, FaGraduationCap } from 'react-icons/fa';
import '../static/css/NotificationsDashboard.css';

const NotificationsDashboard = () => {
  // This would normally come from your API/backend
  const notifications = {
    inbox: 0,
    unread: 0,
    list: [] // Empty list for now, would be populated with actual notifications
  };

  return (
    <div className="notifications-page">
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
            <Link to="/" className="nav-item">
              <FaHome />
              <span>Home</span>
            </Link>
            <Link to="/add-issue" className="nav-item">
              <FaPlus />
              <span>Add New Issue</span>
            </Link>
            <Link to="/notifications" className="nav-item active">
              <FaBell />
              <span>Notifications</span>
            </Link>
            <Link to="/settings" className="nav-item">
              <FaCog />
              <span>Settings</span>
            </Link>
          </nav>
        </aside>

        <main className="main-content">
          <div className="content-header">
            <h1>Notifications</h1>
          </div>

          <div className="notifications-grid">
            <div className="notification-card">
              <h2>Inbox</h2>
              <div className="notification-count">{notifications.inbox}</div>
            </div>
            <div className="notification-card">
              <h2>Unread</h2>
              <div className="notification-count">{notifications.unread}</div>
            </div>
          </div>

          <div className="notifications-list">
            {notifications.list.length === 0 ? (
              <div className="notifications-placeholder">
                <div className="placeholder-line"></div>
                <div className="placeholder-line"></div>
                <div className="placeholder-line"></div>
                <div className="placeholder-line"></div>
                <div className="placeholder-line short"></div>
              </div>
            ) : (
              notifications.list.map(notification => (
                <div key={notification.id} className="notification-item">
                  {/* Notification content would go here */}
                </div>
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default NotificationsDashboard; 