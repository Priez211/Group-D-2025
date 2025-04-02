import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import SignupPage from './components/SignupPage';
import StudentDashboard from './components/StudentDashboard';
import AddNewIssue from './components/AddNewIssue';
import MyIssues from './components/MyIssues';
import IssueDetail from './components/IssueDetail';
import Notifications from './components/Notifications';
// Import registrar components
import RegistrarDashboard from './components/registrar/RegistrarDashboard';
import StudentManagement from './components/registrar/StudentManagement';
import DepartmentManagement from './components/registrar/DepartmentManagement';
import './App.css';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('token');
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Redirect root to login */}
          <Route path="/" element={<Navigate to="/login" />} />
          
          {/* Auth routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          
          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <StudentDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/add-issue"
            element={
              <PrivateRoute>
                <AddNewIssue />
              </PrivateRoute>
            }
          />
          <Route
            path="/my-issues"
            element={
              <PrivateRoute>
                <MyIssues />
              </PrivateRoute>
            }
          />
          <Route
            path="/issue/:issueId"
            element={
              <PrivateRoute>
                <IssueDetail />
              </PrivateRoute>
            }
          />
          <Route
            path="/add-issue/:issueId"
            element={
              <PrivateRoute>
                <AddNewIssue />
              </PrivateRoute>
            }
          />
          <Route
            path="/notifications"
            element={
              <PrivateRoute>
                <Notifications />
              </PrivateRoute>
            }
          />
          
          {/* Registrar routes */}
          <Route
            path="/registrar"
            element={
              <PrivateRoute>
                <RegistrarDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/registrar/students"
            element={
              <PrivateRoute>
                <StudentManagement />
              </PrivateRoute>
            }
          />
          <Route
            path="/registrar/departments"
            element={
              <PrivateRoute>
                <DepartmentManagement />
              </PrivateRoute>
            }
          />
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
