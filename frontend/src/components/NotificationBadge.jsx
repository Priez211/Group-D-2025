import React, { useState, useEffect } from 'react';
import '../styles/NotificationBadge.css';

const NotificationBadge = () => {
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const fetchUnreadCount = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/notifications/unread-count/', {
          credentials: 'exclude'
        });
        if (response.ok) {
          const data = await response.json();
          setUnreadCount(data.count);
        }
      } catch (error) {
        console.error('Error fetching unread notifications:', error);
      }
    };

    fetchUnreadCount();
    const interval = setInterval(fetchUnreadCount, 60000); // Poll every minute

    return () => clearInterval(interval);
  }, []);

  if (unreadCount === 0) return null;

  return (
    <div className="notification-badge">
      {unreadCount}
    </div>
  );
};

export default NotificationBadge; 