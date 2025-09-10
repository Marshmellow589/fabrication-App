import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const Projects = () => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiConfig.ENDPOINTS.PROJECTS}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setProjects(response.data)
    } catch (err) {
      setError('Failed to fetch projects')
      console.error('Error fetching projects:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  if (loading) return <div className="loading">Loading projects...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={handleBack} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>Projects</h1>
      </div>

      <div className="module-content">
        <div className="module-actions">
          <button className="add-button" onClick={() => alert('Add project functionality will be implemented')}>
            + Add New Project
          </button>
        </div>

        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Project Number</th>
                <th>Project Name</th>
                <th>Client</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Status</th>
                <th>Project Manager</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td>{project.id}</td>
                  <td>{project.project_number}</td>
                  <td>{project.project_name}</td>
                  <td>{project.client}</td>
                  <td>{project.start_date}</td>
                  <td>{project.end_date}</td>
                  <td>
                    <span className={`status ${project.status?.toLowerCase()}`}>
                      {project.status}
                    </span>
                  </td>
                  <td>{project.project_manager}</td>
                  <td>
                    <button className="action-btn view" onClick={() => alert('View details')}>View</button>
                    <button className="action-btn edit" onClick={() => alert('Edit project')}>Edit</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {projects.length === 0 && (
          <div className="no-data">
            <p>No projects found.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Projects
