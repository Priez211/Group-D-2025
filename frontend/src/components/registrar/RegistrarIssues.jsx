import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getRegistrarIssues } from '../../services/api';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';
import '../../styles/ManagementPage.css';

// List of departments in the system
const DEPARTMENTS = [
  'All Departments',
  'Department of Computer Science',
  'Department Of Software Engineering',
  'Department of Library And Information System',
  'Department Of Information Technology'
];

const RegistrarIssues = () => {
  const navigate = useNavigate();
  
  // State variables
  const [user, setUser] = useState(null);
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Filter states
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('All Departments');

  // Load user data and fetch issues when component mounts
  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'registrar') {
      navigate('/login');
      return;
    }
    setUser(userData);
    fetchIssues();
  }, [navigate]);

  // Get all issues from the backend
  const fetchIssues = async () => {
    try {
      const data = await getRegistrarIssues();
      setIssues(Array.isArray(data) ? data : []);
      setError('');
    } catch (err) {
      setError('Failed to fetch issues. Please try again later.');
      console.error('Error fetching issues:', err);
    } finally {
      setLoading(false);
    }
  };

  // Format date to readable string
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Navigate to issue details page
  const handleViewIssue = (issue) => {
    const issueId = issue.issue_id || issue.id || issue._id;
    if (!issueId) {
      console.error('No issue ID found:', issue);
      return;
    }
    navigate(`/registrar/issues/${issueId}`);
  };

  // Filter issues based on search, status and department
  const filteredIssues = issues.filter(issue => {
    const matchesFilter = filter === 'all' || issue.status.toLowerCase() === filter;
    
    const matchesSearch = searchQuery === '' || 
      issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      issue.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (issue.student_name && issue.student_name.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (issue.student_department && issue.student_department.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const matchesDepartment = selectedDepartment === 'All Departments' || 
      issue.student_department === selectedDepartment;
    
    return matchesFilter && matchesSearch && matchesDepartment;
  });

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
        {/* Navigation Menu */}
        <nav className="dashboard-nav">
          <ul>
            <li onClick={() => navigate('/registrar')}>
              <span>🏠</span>
              Home
            </li>
            <li className="active">
              <span>📝</span>
              Issues
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
            <li onClick={() => navigate('/registrar/notifications')} className="notification-item">
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

        {/* Main Content */}
        <main className="dashboard-main">
          <div className="page-header">
            <h1>Issue Management</h1>
          </div>

          {/* Search and Filter Section */}
          <div className="filters-section">
            <div className="search-box">
              <input
                type="text"
                placeholder="Search issues..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            
            <div className="filter-dropdowns">
              <select 
                value={selectedDepartment} 
                onChange={(e) => setSelectedDepartment(e.target.value)}
                className="filter-select"
              >
                {DEPARTMENTS.map(dept => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </select>
            </div>
            
            <div className="filter-tabs">
              <button 
                className={filter === 'all' ? 'active' : ''} 
                onClick={() => setFilter('all')}
              >All</button>
              <button 
                className={filter === 'open' ? 'active' : ''} 
                onClick={() => setFilter('open')}
              >Open</button>
              <button 
                className={filter === 'in_progress' ? 'active' : ''} 
                onClick={() => setFilter('in_progress')}
              >In Progress</button>
              <button 
                className={filter === 'resolved' ? 'active' : ''} 
                onClick={() => setFilter('resolved')}
              >Resolved</button>
              <button 
                className={filter === 'closed' ? 'active' : ''} 
                onClick={() => setFilter('closed')}
              >Closed</button>
            </div>
          </div>

          {/* Issues Table */}
          {loading ? (
            <div className="loading-spinner">Loading issues...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : (
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Student</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredIssues.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="no-data">No issues found</td>
                    </tr>
                  ) : (
                    filteredIssues.map(issue => (
                      <tr key={issue.issue_id}>
                        <td>{issue.issue_id}</td>
                        <td>{issue.title}</td>
                        <td>{issue.student_name || 'N/A'}</td>
                        <td>{issue.student_department || 'N/A'}</td>
                        <td>
                          <span className={`status-badge ${issue.status}`}>
                            {issue.status}
                          </span>
                        </td>
                        <td>{formatDate(issue.created_at)}</td>
                        <td>
                          <button 
                            className="view-button"
                            onClick={() => handleViewIssue(issue)}
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default RegistrarIssues;