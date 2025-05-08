// this is the page for designing a lecture user interface
import React from 'react'
import { useNavigate } from 'react-router-dom';
import { getLecturerIssues } from '../../services/api';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';


const API_URL = 'http://localhost:8000';

const lecturerDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || userData.role !== 'lecturer') {
      navigate('/login');
      return;
    }
    setUser(userData);
  }, [navigate]);
  useEffect(() => {
    fetchIssues();
  }, []);
// this is for handling the fetching of issues and errors assoiated with that
  const fetchIssues = async () => {
    setLoading(true);
    try {
      const data = await getLecturerIssues();
      setIssues(Array.isArray(data) ? data : data.issues || []);
      setError('');
    } catch (err) {
      console.error('Error fetching issues:', err);
      setError('Failed to fetch issues. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusClass = (status) => {
    if (!status) return 'unknown';
    return status.toLowerCase().replace(/\s+/g, '_');
  };

  const filteredIssues = issues.filter(issue => {
    if (filter === 'all') return true;
    return issue.status?.toLowerCase() === filter;
  }).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));


  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="logo">
          <span className="graduation-icon">👨‍🏫</span>
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
            <li className="active">
              <span>🏠</span>
              Home
            </li>
            <li onClick={() => navigate('/lecturer/issues')}>
              <span>📝</span>
              Assigned Issues
            </li>
            <li onClick={() => navigate('/lecturer/notifications')} className="notification-item">
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
          <h1 className="welcome-message">Welcome back, {user?.first_name || 'Lecturer'}!</h1>
          
          <section className="issues-section">
            <div className="section-header">
              <h2>Assigned Issues</h2>
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
 
    <div>lecturerDashboard</div>
  )
}

export default lecturerDashboard
