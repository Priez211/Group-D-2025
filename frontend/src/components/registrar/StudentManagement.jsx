import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import { getStudents } from '../../services/api';
import '../../styles/Dashboard.css';
import '../../styles/ManagementPage.css';

// Map departments to their colleges for filtering
const DEPARTMENT_FACULTY_MAP = {
  'Department of Computer Science': 'College of Computing',
  'Department Of Software Engineering': 'College of Computing',
  'Department of Library And Information System': 'College Of Humanity And Social Sciences',
  'Department Of Information Technology': 'College of Computing'
};

const StudentManagement = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('All Departments');
  const [selectedYear, setSelectedYear] = useState('All Years');

  const departmentOptions = [
    'All Departments',
    'Department of Computer Science',
    'Department Of Software Engineering',
    'Department of Library And Information System',
    'Department Of Information Technology'
  ];

  const yearOptions = [
    'All Years',
    'First Year',
    'Second Year',
    'Third Year'
  ];

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      
      if (selectedDepartment && selectedDepartment !== 'All Departments') {
        params.department = selectedDepartment;
      }
      if (selectedYear && selectedYear !== 'All Years') {
        params.year = selectedYear;
      }

      const data = await getStudents(params);
      setStudents(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching students:', error);
      if (error.message === 'Authentication required. Please log in again.') {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  }, [selectedDepartment, selectedYear, navigate]);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'registrar') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const filteredStudents = students.filter(student => {
    const fullName = `${student.fullName}`;
    const matchesSearch = 
      fullName.toLowerCase().includes(filter.toLowerCase()) ||
      student.email.toLowerCase().includes(filter.toLowerCase()) ||
      student.studentNumber.toLowerCase().includes(filter.toLowerCase());
    
    const matchesDepartment = selectedDepartment === 'All Departments' || 
      student.department?.name === selectedDepartment;
    
    const matchesYear = selectedYear === 'All Years' || 
      student.yearOfStudy === selectedYear;
    
    return matchesSearch && matchesDepartment && matchesYear;
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
            <li className="active">
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
            <li>
              <span>⚙️</span>
              Settings
            </li>
          </ul>
        </nav>

        <main className="dashboard-main">
          <div className="page-header">
            <h1>Student Management</h1>
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
              
              <select 
                value={selectedYear} 
                onChange={(e) => setSelectedYear(e.target.value)}
                className="filter-select"
              >
                {yearOptions.map((option, index) => (
                  <option key={index} value={option}>{option}</option>
                ))}
              </select>
            </div>
          </div>
          
          {loading ? (
            <div className="loading-spinner">Loading student data...</div>
          ) : (
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Student Number</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Year</th>
                    <th>Course</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredStudents.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="no-data">No students match your filters</td>
                    </tr>
                  ) : (
                    filteredStudents.map(student => (
                      <tr key={student.id}>
                        <td>{student.studentNumber}</td>
                        <td>{student.fullName}</td>
                        <td>{student.email}</td>
                        <td>{student.department?.name}</td>
                        <td>{student.yearOfStudy}</td>
                        <td>{student.course}</td>
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

export default StudentManagement;