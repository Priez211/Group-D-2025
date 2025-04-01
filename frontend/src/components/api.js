import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
});

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
    
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config,
    });
    return Promise.reject(error);
  }
);

// Helper function for HTTP requests
const fetchWithAuth = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include'
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      message: 'Something went wrong'
    }));
    throw new Error(errorData.message || `Error: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
};

// User authentication
export const loginUser = async (credentials) => {
  return fetchWithAuth(`${API_URL}/login/`, {
    method: 'POST',
    body: JSON.stringify(credentials)
  });
};

export const registerUser = async (userData) => {
  console.log('Registering user with data:', JSON.stringify(userData, null, 2));
  
  try {
    const response = await fetch(`${API_URL}/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    console.log('Registration response status:', response.status);
    
    const responseData = await response.json();
    console.log('Registration response data:', responseData);
    
    if (!response.ok) {
      console.error('Registration error response:', responseData);
      
      // Handle different types of error responses
      if (responseData.errors) {
        // Handle field-specific errors
        const errorMessages = Object.entries(responseData.errors)
          .map(([field, messages]) => {
            if (Array.isArray(messages)) {
              return `${field}: ${messages.join(', ')}`;
            }
            return `${field}: ${messages}`;
          })
          .join('\n');
        throw new Error(errorMessages);
      } else if (responseData.message) {
        // Handle general error message
        throw new Error(responseData.message);
      } else if (responseData.detail) {
        // Handle DRF detail error
        throw new Error(responseData.detail);
      } else {
        throw new Error('Registration failed. Please check your input and try again.');
      }
    }

    return responseData;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

export const getStudentIssues = async () => {
  try {
    console.log('Fetching all student issues');
    const response = await api.get('/student/issues', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.data) {
      throw new Error('No data received from server');
    }
    
    console.log('Received issues:', response.data);
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Server responded with error:', error.response.data);
      throw error.response.data;
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
      throw new Error('No response from server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error setting up request:', error.message);
      throw error;
    }
  }
};

export const getIssueById = async (issueId) => {
  try {
    console.log('Making request to fetch issue:', issueId);
    const response = await api.get(`/student/issues/${issueId}`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.data) {
      console.error('No data received for issue:', issueId);
      throw new Error('No data received from server');
    }
    
    console.log('Successfully fetched issue data:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching issue:', {
      issueId,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    
    if (error.response?.status === 404) {
      throw new Error('Issue not found');
    }
    
    throw error.response?.data || error.message;
  }
};

export const createIssue = async (issueData) => {
  try {
    console.log('Creating issue with data:', issueData);
    
    // Create FormData if there's an attachment
    let data = issueData;
    if (issueData.attachment) {
      const formData = new FormData();
      Object.keys(issueData).forEach(key => {
        if (key === 'attachment') {
          formData.append('attachment', issueData.attachment);
        } else {
          formData.append(key, issueData[key]);
        }
      });
      data = formData;
    }

    const response = await api.post('/student/issues', data, {
      headers: {
        ...(issueData.attachment ? {
          'Content-Type': 'multipart/form-data'
        } : {
          'Content-Type': 'application/json'
        })
      }
    });
    
    console.log('Issue created successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error creating issue:', error.response?.data || error.message);
    throw error.response?.data || error.message;
  }
};

export const updateIssue = async (issueId, issueData) => {
  try {
    console.log('Updating issue:', issueId, 'with data:', issueData);
    
    // Create FormData if there's an attachment
    let data = issueData;
    if (issueData.attachment) {
      const formData = new FormData();
      Object.keys(issueData).forEach(key => {
        if (key === 'attachment') {
          formData.append('attachment', issueData.attachment);
        } else {
          formData.append(key, issueData[key]);
        }
      });
      data = formData;
    }

    const response = await api.patch(`/student/issues/${issueId}`, data, {
      headers: {
        ...(issueData.attachment ? {
          'Content-Type': 'multipart/form-data'
        } : {
          'Content-Type': 'application/json'
        })
      }
    });
    
    console.log('Issue updated successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error updating issue:', error.response?.data || error.message);
    throw error.response?.data || error.message;
  }
};

export const getNotifications = async () => {
  try {
    console.log('Fetching notifications');
    const response = await api.get('/notifications', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.data) {
      throw new Error('No data received from server');
    }
    
    console.log('Received notifications:', response.data);
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Server responded with error:', error.response.data);
      throw error.response.data;
    } else if (error.request) {
      console.error('No response received:', error.request);
      throw new Error('No response from server');
    } else {
      console.error('Error setting up request:', error.message);
      throw error;
    }
  }
};

export const markNotificationRead = async (notificationId) => {
  try {
    console.log('Marking notification as read:', notificationId);
    const response = await api.post(`/notifications/${notificationId}/mark-read`, {}, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.data) {
      throw new Error('No data received from server');
    }
    
    console.log('Notification marked as read:', response.data);
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Server responded with error:', error.response.data);
      throw error.response.data;
    } else if (error.request) {
      console.error('No response received:', error.request);
      throw new Error('No response from server');
    } else {
      console.error('Error setting up request:', error.message);
      throw error;
    }
  }
};

export default api;