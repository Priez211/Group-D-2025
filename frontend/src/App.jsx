import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/login';
import SignupPage from './components/signup';
import StudentDashboard from './components/studentDashboard';
import AddNewIssue from './components/CreateIssue';
import MyIssues from './components/MyIssues';
import IssueDetail from './components/IssueDetails';
import Notifications from './components/notifications';
// Import registrar components
import RegistrarDashboard from './components/RegistrarDashboard';
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
         {/* <Route
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
          */}
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );

  
}

export default App;
