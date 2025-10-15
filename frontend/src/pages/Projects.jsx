import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const Projects = () => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingProject, setEditingProject] = useState(null)
  const [userRole, setUserRole] = useState('')
  const navigate = useNavigate()

  // Form state
  const [formData, setFormData] = useState({
    project_number: '',
    project_name: '',
    client: '',
    start_date: '',
    end_date: '',
    status: 'active',
    project_manager: '',
    description: '',
    budget: ''
  })

  useEffect(() => {
    fetchProjects()
    // Get user role from localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      setUserRole(user.role)
    }
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

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      
      if (editingProject) {
        // Update existing project
        await axios.put(`${apiConfig.ENDPOINTS.PROJECTS}/${editingProject.id}`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else {
        // Create new project
        await axios.post(`${apiConfig.ENDPOINTS.PROJECTS}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }
      
      setShowAddForm(false)
      setEditingProject(null)
      setFormData({
        project_number: '',
        project_name: '',
        client: '',
        start_date: '',
        end_date: '',
        status: 'active',
        project_manager: '',
        description: '',
        budget: ''
      })
      fetchProjects() // Refresh the list
    } catch (err) {
      if (err.response?.status === 403) {
        setError('Only admin users can create projects')
      } else if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Failed to save project')
      } else {
        setError('Failed to save project')
      }
      console.error('Error saving project:', err)
    }
  }

  const handleEdit = (project) => {
    setEditingProject(project)
    setFormData({
      project_number: project.project_number,
      project_name: project.project_name,
      client: project.client,
      start_date: project.start_date,
      end_date: project.end_date || '',
      status: project.status,
      project_manager: project.project_manager,
      description: project.description || '',
      budget: project.budget || ''
    })
    setShowAddForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${apiConfig.ENDPOINTS.PROJECTS}/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchProjects() // Refresh the list
      } catch (err) {
        setError('Failed to delete project')
        console.error('Error deleting project:', err)
      }
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingProject(null)
    setFormData({
      project_number: '',
      project_name: '',
      client: '',
      start_date: '',
      end_date: '',
      status: 'active',
      project_manager: '',
      description: '',
      budget: ''
    })
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  const isAdmin = userRole === 'admin'

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
          {isAdmin && (
            <button 
              className="add-button" 
              onClick={() => setShowAddForm(true)}
            >
              + Add New Project
            </button>
          )}
        </div>

        {showAddForm && (
          <div className="form-overlay">
            <div className="form-container">
              <h2>{editingProject ? 'Edit Project' : 'Add New Project'}</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Project Number *</label>
                    <input
                      type="text"
                      name="project_number"
                      value={formData.project_number}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Project Name *</label>
                    <input
                      type="text"
                      name="project_name"
                      value={formData.project_name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Client *</label>
                    <input
                      type="text"
                      name="client"
                      value={formData.client}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Start Date *</label>
                    <input
                      type="date"
                      name="start_date"
                      value={formData.start_date}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>End Date</label>
                    <input
                      type="date"
                      name="end_date"
                      value={formData.end_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Status</label>
                    <select
                      name="status"
                      value={formData.status}
                      onChange={handleInputChange}
                    >
                      <option value="active">Active</option>
                      <option value="completed">Completed</option>
                      <option value="on-hold">On Hold</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Project Manager *</label>
                    <input
                      type="text"
                      name="project_manager"
                      value={formData.project_manager}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Budget</label>
                    <input
                      type="number"
                      step="0.01"
                      name="budget"
                      value={formData.budget}
                      onChange={handleInputChange}
                      placeholder="0.00"
                    />
                  </div>
                  <div className="form-group full-width">
                    <label>Description</label>
                    <textarea
                      name="description"
                      value={formData.description}
                      onChange={handleInputChange}
                      rows="3"
                      placeholder="Project description..."
                    />
                  </div>
                </div>
                <div className="form-buttons">
                  <button type="submit" className="save-btn">
                    {editingProject ? 'Update' : 'Save'}
                  </button>
                  <button type="button" onClick={handleCancel} className="cancel-btn">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

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
                  <td>{project.end_date || 'N/A'}</td>
                  <td>
                    <span className={`status ${project.status?.toLowerCase()}`}>
                      {project.status}
                    </span>
                  </td>
                  <td>{project.project_manager}</td>
                  <td>
                    <button className="action-btn view" onClick={() => alert('View details')}>View</button>
                    {isAdmin && (
                      <>
                        <button className="action-btn edit" onClick={() => handleEdit(project)}>
                          Edit
                        </button>
                        <button className="action-btn delete" onClick={() => handleDelete(project.id)}>
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {projects.length === 0 && !showAddForm && (
          <div className="no-data">
            <p>No projects found.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Projects
