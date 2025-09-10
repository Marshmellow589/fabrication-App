import React from 'react'
import { useNavigate } from 'react-router-dom'

const Dashboard = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  const navigateToModule = (module) => {
    navigate(`/${module.toLowerCase()}`)
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button onClick={handleLogout} className="logout-button-top-right">
          Logout
        </button>
      </div>
      <div className="dashboard-content">
        <h2>Welcome to Fabrication Management System</h2>
        <p>You have successfully logged in!</p>
        
        <div className="dashboard-sections">
          <div className="dashboard-card" onClick={() => navigateToModule('projects')}>
            <h3>Projects</h3>
            <p>Manage fabrication projects</p>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateToModule('materials')}>
            <h3>Materials</h3>
            <p>Track material inspections</p>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateToModule('fitup')}>
            <h3>Fit-up</h3>
            <p>Manage fit-up inspections</p>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateToModule('final')}>
            <h3>Final Inspection</h3>
            <p>Final quality checks</p>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateToModule('ndt')}>
            <h3>NDT Requests</h3>
            <p>Non-destructive testing requests</p>
          </div>
          
          <div className="dashboard-card" onClick={() => navigateToModule('users')}>
            <h3>User Management</h3>
            <p>Manage system users and permissions</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
