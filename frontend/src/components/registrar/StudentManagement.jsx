import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';
import '../../styles/ManagementPage.css';

const StudentManagement = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [selectedCollege, setSelectedCollege] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [selectedYear, setSelectedYear] = useState('');

  const collegeOptions = [
    'All Colleges',
    'College of Computing',
    'College Of Humanity And Social Sciences',
    'College Of Engineering',
    'College Of Education'
  ];

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

  useEffect(() => {
    // Check authentication
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'registrar') {
      navigate('/login');
      return;
    }
    setUser(userData);
    
    // Fetch student data
    fetchStudents();
  }, [navigate]);

  const fetchStudents = async () => {
    
    setLoading(true);
    try {
      // Simulated data - replace with actual API call
      const mockStudents = [
        {
          id: 1,
          name: 'John Doe',
          studentNumber: '2400721001',
          email: 'john.doe@student.example.com',
          college: 'College of Computing',
          department: 'Department of Computer Science',
          yearOfStudy: 'Second Year',
          course: 'Computer Science'
        },
        {
          id: 2,
          name: 'Jane Smith',
          studentNumber: '2400721002',
          email: 'jane.smith@student.example.com',
          college: 'College of Computing',
          department: 'Department Of Software Engineering',
          yearOfStudy: 'First Year',
          course: 'Software Engineering'
        },
        {
          id: 3,
          name: 'Michael Johnson',
          studentNumber: '2400721003',
          email: 'michael.j@student.example.com',
          college: 'College of Computing',
          department: 'Department Of Information Technology',
          yearOfStudy: 'Third Year',
          course: 'Information Technology'
        },
        {
          id: 4,
          name: 'Anna Delvey',
          studentNumber: '2400721004',
          email: 'anna.delvey@student.example.com',
          college: 'College of Computing',
          department: 'Department Of Information Technology',
          yearOfStudy: 'Second Year',
          course: 'Computer Science'
        }
      ];
      
      setTimeout(() => {
        setStudents(mockStudents);
        setLoading(false);
      }, 800); // Simulate network delay
    } catch (error) {
      console.error('Error fetching students:', error);
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = 
      student.name.toLowerCase().includes(filter.toLowerCase()) ||
      student.studentNumber.toLowerCase().includes(filter.toLowerCase()) ||
      student.email.toLowerCase().includes(filter.toLowerCase());
    
    const matchesCollege = selectedCollege === '' || selectedCollege === 'All Colleges' || 
      student.college === selectedCollege;
    
    const matchesDepartment = selectedDepartment === '' || selectedDepartment === 'All Departments' || 
      student.department === selectedDepartment;
    
    const matchesYear = selectedYear === '' || selectedYear === 'All Years' || 
      student.yearOfStudy === selectedYear;
    
    return matchesSearch && matchesCollege && matchesDepartment && matchesYear;
  });

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="logo">
          <span className="graduation-icon">👨‍💼</span>
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
            <li onClick={() => navigate('/registrar/issues')}>
              <span>📝</span>
              Issues
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
          <div className="page-header">
            <h1>Student Management</h1>
            <button className="primary-button" onClick={() => navigate('/add-student')}>
              Add New Student
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
                value={selectedCollege} 
                onChange={(e) => setSelectedCollege(e.target.value)}
                className="filter-select"
              >
                {collegeOptions.map((option, index) => (
                  <option key={index} value={option}>{option}</option>
                ))}
              </select>
              
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
            <>
              <div className="data-table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Student Number</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>College</th>
                      <th>Department</th>
                      <th>Year</th>
                      <th>Course</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStudents.length === 0 ? (
                      <tr>
                        <td colSpan="8" className="no-data">No students match your filters</td>
                      </tr>
                    ) : (
                      filteredStudents.map(student => (
                        <tr key={student.id}>
                          <td>{student.studentNumber}</td>
                          <td>{student.name}</td>
                          <td>{student.email}</td>
                          <td>{student.college}</td>
                          <td>{student.department}</td>
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
              
              <div className="pagination-controls">
                <button className="pagination-button" disabled>&lt; Previous</button>
                <span className="page-indicator">Page 1 of 1</span>
                <button className="pagination-button" disabled>Next &gt;</button>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default StudentManagement; 