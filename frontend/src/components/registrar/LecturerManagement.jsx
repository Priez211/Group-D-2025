import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import { getLecturers } from '../../services/api';
import '../../styles/Dashboard.css';
import '../../styles/ManagementPage.css';

// Map departments to their colleges for filtering
const DEPARTMENT_FACULTY_MAP = {
  'Department of Computer Science': 'College of Computing',
  'Department Of Software Engineering': 'College of Computing',
  'Department of Library And Information System': 'College Of Humanity And Social Sciences',
  'Department Of Information Technology': 'College of Computing'
};

const LecturerManagement = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [lecturers, setLecturers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('All Departments');

  const departmentOptions = [
    'All Departments',
    'Department of Computer Science',
    'Department Of Software Engineering',
    'Department of Library And Information System',
    'Department Of Information Technology'
  ];

  const fetchLecturers = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      
      if (selectedDepartment && selectedDepartment !== 'All Departments') {
        params.department = selectedDepartment;
      }

      const data = await getLecturers(params);
      setLecturers(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching lecturers:', error);
      if (error.message === 'Authentication required. Please log in again.') {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  }, [selectedDepartment, navigate]);

  useEffect(() => {
    // Check authentication and get user data
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'registrar') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  useEffect(() => {
    fetchLecturers();
  }, [fetchLecturers]);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const filteredLecturers = lecturers.filter(lecturer => {
    const fullName = `${lecturer.fullName}`;
    const matchesSearch = 
      fullName.toLowerCase().includes(filter.toLowerCase()) ||
      lecturer.email.toLowerCase().includes(filter.toLowerCase()) ||
      lecturer.lecturerId.toLowerCase().includes(filter.toLowerCase());
    
    const matchesDepartment = selectedDepartment === 'All Departments' || 
      lecturer.department?.name === selectedDepartment;
    
    return matchesSearch && matchesDepartment;
  });

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
        {/* Sidebar Navigation */}
        <nav className="dashboard-nav">
          <ul>
            <li onClick={() => navigate('/registrar')}>
              <span>🏠</span>
              Home
            </li>
            <li onClick={() => navigate('/registrar/issues')}>
              <span>📝</span>
              Issues
            </li>
            <li onClick={() => navigate('/registrar/students')}>
              <span>👨‍🎓</span>
              Students
            </li>
            <li className="active">
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
            <li>
              <span>⚙️</span>
              Settings
            </li>
          </ul>
        </nav>

        {/* Main Content */}
        <main className="dashboard-main">
          <div className="page-header">
            <h1>Lecturer Management</h1>
            <button className="primary-button">
              Add New Lecturer
            </button>
          </div>
          
          <div className="filter-bar">
            <div className="search-bar">
              <input
                type="text"
                placeholder="Search by name, ID or email..."
                value={filter}
                onChange={handleFilterChange}
              />
            </div>
            
            <div className="filter-dropdowns">
              <select 
                value={selectedDepartment} 
                onChange={(e) => setSelectedDepartment(e.target.value)}
                className="filter-select"
              >
                {departmentOptions.map((option, index) => (
                  <option key={index} value={option}>{option}</option>
                ))}
              </select>
            </div>
          </div>
          
          {loading ? (
            <div className="loading-spinner">Loading lecturer data...</div>
          ) : (
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Lecturer ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredLecturers.length === 0 ? (
                    <tr>
                      <td colSpan="5" className="no-data">No lecturers match your filters</td>
                    </tr>
                  ) : (
                    filteredLecturers.map(lecturer => (
                      <tr key={lecturer.id}>
                        <td>{lecturer.lecturerId}</td>
                        <td>{lecturer.fullName}</td>
                        <td>{lecturer.email}</td>
                        <td>{lecturer.department?.name}</td>
                        <td className="actions-cell">
                          <button className="icon-button view-button" title="View Details">👁️</button>
                          <button className="icon-button edit-button" title="Edit">✏️</button>
                          <button className="icon-button delete-button" title="Delete">🗑️</button>
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

export default LecturerManagement;