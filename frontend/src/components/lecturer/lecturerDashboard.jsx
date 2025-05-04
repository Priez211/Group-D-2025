import React from 'react'
import { useNavigate } from 'react-router-dom';
import { getLecturerIssues } from '../../services/api';
import UserProfile from '../UserProfile';
import NotificationBadge from '../NotificationBadge';
import '../../styles/Dashboard.css';


const API_URL = 'http://localhost:8000';

const lecturerDashboard = () => {
  return (
    <div>lecturerDashboard</div>
  )
}

export default lecturerDashboard