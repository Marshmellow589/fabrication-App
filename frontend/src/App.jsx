import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './components/auth/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Projects from './pages/Projects.jsx'
import Material from './pages/Material.jsx'
import Fitup from './pages/Fitup.jsx'
import FinalInspection from './pages/FinalInspection.jsx'
import NDTRequest from './pages/NDTRequest.jsx'
import Users from './pages/Users.jsx'
import ProjectSelector from './components/project/ProjectSelector'

// Protected Route component that requires authentication
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? children : <Navigate to="/" replace />
}

// Project Route component that requires project selection
const ProjectRoute = ({ children }) => {
  const { isAuthenticated, selectedProject } = useAuth()
  
  if (!isAuthenticated) {
    return <Navigate to="/" replace />
  }
  
  if (!selectedProject) {
    return <Navigate to="/project-select" replace />
  }
  
  return children
}

// Main App Content
const AppContent = () => {
  const { isAuthenticated, selectedProject, selectProject } = useAuth()

  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Login />} />
        
        {/* Project selection route */}
        <Route 
          path="/project-select" 
          element={
            <ProtectedRoute>
              <ProjectSelector onProjectSelect={selectProject} />
            </ProtectedRoute>
          } 
        />
        
        {/* Routes that require project selection */}
        <Route 
          path="/dashboard" 
          element={
            <ProjectRoute>
              <Dashboard />
            </ProjectRoute>
          } 
        />
        <Route 
          path="/materials" 
          element={
            <ProjectRoute>
              <Material />
            </ProjectRoute>
          } 
        />
        <Route 
          path="/fitup" 
          element={
            <ProjectRoute>
              <Fitup />
            </ProjectRoute>
          } 
        />
        <Route 
          path="/final" 
          element={
            <ProjectRoute>
              <FinalInspection />
            </ProjectRoute>
          } 
        />
        <Route 
          path="/ndt" 
          element={
            <ProjectRoute>
              <NDTRequest />
            </ProjectRoute>
          } 
        />
        
        {/* Routes that don't require project selection */}
        <Route 
          path="/projects" 
          element={
            <ProtectedRoute>
              <Projects />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/users" 
          element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          } 
        />
        
        {/* Redirect authenticated users to project selection if no project selected */}
        <Route 
          path="*" 
          element={
            isAuthenticated ? (
              selectedProject ? <Navigate to="/dashboard" replace /> : <Navigate to="/project-select" replace />
            ) : (
              <Navigate to="/" replace />
            )
          } 
        />
      </Routes>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
