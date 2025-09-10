import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const Material = () => {
  const [materials, setMaterials] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingMaterial, setEditingMaterial] = useState(null)
  const navigate = useNavigate()

  // Form state
  const [formData, setFormData] = useState({
    project_id: 1,
    material_type: '',
    material_grade: '',
    thickness: '',
    size: '',
    heat_no: '',
    material_inspection_date: '',
    material_inspection_result: '',
    material_report_no: '',
    status: 'pending'
  })

  useEffect(() => {
    fetchMaterials()
  }, [])

  const fetchMaterials = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiConfig.ENDPOINTS.MATERIAL}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setMaterials(response.data)
    } catch (err) {
      setError('Failed to fetch materials')
      console.error('Error fetching materials:', err)
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
      
      if (editingMaterial) {
        // Update existing material
        await axios.put(`${apiConfig.ENDPOINTS.MATERIAL}/${editingMaterial.id}`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else {
        // Create new material
        await axios.post(`${apiConfig.ENDPOINTS.MATERIAL}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }
      
      setShowAddForm(false)
      setEditingMaterial(null)
      setFormData({
        project_id: 1,
        material_type: '',
        material_grade: '',
        thickness: '',
        size: '',
        heat_no: '',
        material_inspection_date: '',
        material_inspection_result: '',
        material_report_no: '',
        status: 'pending'
      })
      fetchMaterials() // Refresh the list
    } catch (err) {
      setError('Failed to save material')
      console.error('Error saving material:', err)
    }
  }

  const handleEdit = (material) => {
    setEditingMaterial(material)
    setFormData({
      project_id: material.project_id,
      material_type: material.material_type,
      material_grade: material.material_grade || '',
      thickness: material.thickness || '',
      size: material.size || '',
      heat_no: material.heat_no || '',
      material_inspection_date: material.material_inspection_date || '',
      material_inspection_result: material.material_inspection_result || '',
      material_report_no: material.material_report_no || '',
      status: material.status
    })
    setShowAddForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this material record?')) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${apiConfig.ENDPOINTS.MATERIAL}/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchMaterials() // Refresh the list
      } catch (err) {
        setError('Failed to delete material')
        console.error('Error deleting material:', err)
      }
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingMaterial(null)
    setFormData({
      project_id: 1,
      material_type: '',
      material_grade: '',
      thickness: '',
      size: '',
      heat_no: '',
      material_inspection_date: '',
      material_inspection_result: '',
      material_report_no: '',
      status: 'pending'
    })
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  if (loading) return <div className="loading">Loading materials...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={handleBack} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>Material Inspections</h1>
      </div>

      <div className="module-content">
        <div className="module-actions">
          <button 
            className="add-button" 
            onClick={() => setShowAddForm(true)}
          >
            + Add New Material
          </button>
        </div>

        {showAddForm && (
          <div className="form-overlay">
            <div className="form-container">
              <h2>{editingMaterial ? 'Edit Material' : 'Add New Material'}</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Material Type *</label>
                    <input
                      type="text"
                      name="material_type"
                      value={formData.material_type}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Material Grade</label>
                    <input
                      type="text"
                      name="material_grade"
                      value={formData.material_grade}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Thickness (mm)</label>
                    <input
                      type="number"
                      step="0.1"
                      name="thickness"
                      value={formData.thickness}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Size</label>
                    <input
                      type="text"
                      name="size"
                      value={formData.size}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Heat No</label>
                    <input
                      type="text"
                      name="heat_no"
                      value={formData.heat_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Inspection Date</label>
                    <input
                      type="date"
                      name="material_inspection_date"
                      value={formData.material_inspection_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Inspection Result</label>
                    <select
                      name="material_inspection_result"
                      value={formData.material_inspection_result}
                      onChange={handleInputChange}
                    >
                      <option value="">Select Result</option>
                      <option value="passed">Passed</option>
                      <option value="failed">Failed</option>
                      <option value="pending">Pending</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Report No</label>
                    <input
                      type="text"
                      name="material_report_no"
                      value={formData.material_report_no}
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
                      <option value="pending">Pending</option>
                      <option value="approved">Approved</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </div>
                </div>
                <div className="form-buttons">
                  <button type="submit" className="save-btn">
                    {editingMaterial ? 'Update' : 'Save'}
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
                <th>Material Type</th>
                <th>Grade</th>
                <th>Thickness</th>
                <th>Size</th>
                <th>Heat No</th>
                <th>Inspection Date</th>
                <th>Result</th>
                <th>Report No</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {materials.map((material) => (
                <tr key={material.id}>
                  <td>{material.id}</td>
                  <td>{material.material_type}</td>
                  <td>{material.material_grade || 'N/A'}</td>
                  <td>{material.thickness || 'N/A'}</td>
                  <td>{material.size || 'N/A'}</td>
                  <td>{material.heat_no || 'N/A'}</td>
                  <td>{material.material_inspection_date || 'N/A'}</td>
                  <td>
                    <span className={`result ${material.material_inspection_result?.toLowerCase()}`}>
                      {material.material_inspection_result || 'N/A'}
                    </span>
                  </td>
                  <td>{material.material_report_no || 'N/A'}</td>
                  <td>
                    <span className={`status ${material.status?.toLowerCase()}`}>
                      {material.status}
                    </span>
                  </td>
                  <td>
                    <button className="action-btn edit" onClick={() => handleEdit(material)}>
                      Edit
                    </button>
                    <button className="action-btn delete" onClick={() => handleDelete(material.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {materials.length === 0 && !showAddForm && (
          <div className="no-data">
            <p>No material inspections found.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Material
