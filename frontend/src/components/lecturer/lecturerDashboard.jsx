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
  
  return (
    <div>lecturerDashboard</div>
  )
}

export default lecturerDashboard