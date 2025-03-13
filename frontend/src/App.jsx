import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home';
import StudentDashboard from './components/StudentDashboard';
import LecturerDashboard from './components/LecturerDashboard';
import RegistrarDashboard from './components/RegistrarDashboard';
import IssueDetails from './components/IssueDetails';
import AddIssue from './components/AddIssue';
import Login from './components/Login';
import SignUp from './components/SignUp';
import NotificationsDashboard from './components/NotificationsDashboard';

import './App.css';

const App = () => {
  // This would normally come from your authentication system
  const isAuthenticated = false; // Set to true to test authenticated routes
  const userRole = 'registrar'; // This would come from your auth system

  // Protected Route wrapper
  const ProtectedRoute = ({ children, allowedRoles = [] }) => {
    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }
    if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
      return <Navigate to="/dashboard" />;
    }
    return children;
  };

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />

        {/* Student Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/add-issue"
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <AddIssue />
            </ProtectedRoute>
          }
        />
        <Route
          path="/issue/:issueId"
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <IssueDetails userRole="student" />
            </ProtectedRoute>
          }
        />

        {/* Lecturer Routes */}
        <Route
          path="/lecturer-dashboard"
          element={
            <ProtectedRoute allowedRoles={['lecturer']}>
              <LecturerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lecturer-issues"
          element={
            <ProtectedRoute allowedRoles={['lecturer']}>
              <LecturerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lecturer-students"
          element={
            <ProtectedRoute allowedRoles={['lecturer']}>
              <LecturerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lecturer/issue/:issueId"
          element={
            <ProtectedRoute allowedRoles={['lecturer']}>
              <IssueDetails userRole="lecturer" />
            </ProtectedRoute>
          }
        />

        {/* Registrar Routes */}
        <Route
          path="/registrar-dashboard"
          element={
            <ProtectedRoute allowedRoles={['registrar']}>
              <RegistrarDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/registrar-issues"
          element={
            <ProtectedRoute allowedRoles={['registrar']}>
              <RegistrarDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/registrar-students"
          element={
            <ProtectedRoute allowedRoles={['registrar']}>
              <RegistrarDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/registrar/issue/:issueId"
          element={
            <ProtectedRoute allowedRoles={['registrar']}>
              <IssueDetails userRole="registrar" />
            </ProtectedRoute>
          }
        />

        {/* Common Protected Routes */}
        <Route
          path="/notifications"
          element={
            <ProtectedRoute>
              <NotificationsDashboard />
            </ProtectedRoute>
          }
        />

        {/* Fallback route for unmatched paths */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;


