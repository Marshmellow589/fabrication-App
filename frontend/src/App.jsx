import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/auth/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Projects from './pages/Projects.jsx'
import Material from './pages/Material.jsx'
import Fitup from './pages/Fitup.jsx'
import FinalInspection from './pages/FinalInspection.jsx'
import NDTRequest from './pages/NDTRequest.jsx'
import Users from './pages/Users.jsx'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/materials" element={<Material />} />
          <Route path="/fitup" element={<Fitup />} />
          <Route path="/final" element={<FinalInspection />} />
          <Route path="/ndt" element={<NDTRequest />} />
          <Route path="/users" element={<Users />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
