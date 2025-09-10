import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const NDTRequest = () => {
  const [ndtRequests, setNdtRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingRequest, setEditingRequest] = useState(null)
  const navigate = useNavigate()

  // Form state
  const [formData, setFormData] = useState({
    project_id: 1,
    line_no: '',
    spool_no: '',
    joint_no: '',
    weld_process: '',
    welder_no: '',
    weld_length: '',
    ndt_request_date: '',
    ndt_method: '',
    ndt_result: '',
    status: 'pending'
  })

  useEffect(() => {
    fetchNdtRequests()
  }, [])

  const fetchNdtRequests = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiConfig.ENDPOINTS.NDT}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setNdtRequests(response.data)
    } catch (err) {
      setError('Failed to fetch NDT requests')
      console.error('Error fetching NDT requests:', err)
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
      
      if (editingRequest) {
        // Update existing NDT request
        await axios.put(`${apiConfig.ENDPOINTS.NDT}/${editingRequest.id}`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else {
        // Create new NDT request
        await axios.post(`${apiConfig.ENDPOINTS.NDT}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }
      
      setShowAddForm(false)
      setEditingRequest(null)
      setFormData({
        project_id: 1,
        line_no: '',
        spool_no: '',
        joint_no: '',
        weld_process: '',
        welder_no: '',
        weld_length: '',
        ndt_request_date: '',
        ndt_method: '',
        ndt_result: '',
        status: 'pending'
      })
      fetchNdtRequests() // Refresh the list
    } catch (err) {
      setError('Failed to save NDT request')
      console.error('Error saving NDT request:', err)
    }
  }

  const handleEdit = (request) => {
    setEditingRequest(request)
    setFormData({
      project_id: request.project_id,
      line_no: request.line_no || '',
      spool_no: request.spool_no || '',
      joint_no: request.joint_no || '',
      weld_process: request.weld_process || '',
      welder_no: request.welder_no || '',
      weld_length: request.weld_length || '',
      ndt_request_date: request.ndt_request_date || '',
      ndt_method: request.ndt_method || '',
      ndt_result: request.ndt_result || '',
      status: request.status
    })
    setShowAddForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this NDT request?')) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${apiConfig.ENDPOINTS.NDT}/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchNdtRequests() // Refresh the list
      } catch (err) {
        setError('Failed to delete NDT request')
        console.error('Error deleting NDT request:', err)
      }
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingRequest(null)
    setFormData({
      project_id: 1,
      line_no: '',
      spool_no: '',
      joint_no: '',
      weld_process: '',
      welder_no: '',
      weld_length: '',
      ndt_request_date: '',
      ndt_method: '',
      ndt_result: '',
      status: 'pending'
    })
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  if (loading) return <div className="loading">Loading NDT requests...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={handleBack} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>NDT Requests</h1>
      </div>

      <div className="module-content">
        <div className="module-actions">
          <button 
            className="add-button" 
            onClick={() => setShowAddForm(true)}
          >
            + Add New NDT Request
          </button>
        </div>

        {showAddForm && (
          <div className="form-overlay">
            <div className="form-container">
              <h2>{editingRequest ? 'Edit NDT Request' : 'Add New NDT Request'}</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Line No</label>
                    <input
                      type="text"
                      name="line_no"
                      value={formData.line_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Spool No</label>
                    <input
                      type="text"
                      name="spool_no"
                      value={formData.spool_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Joint No</label>
                    <input
                      type="text"
                      name="joint_no"
                      value={formData.joint_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Weld Process</label>
                    <input
                      type="text"
                      name="weld_process"
                      value={formData.weld_process}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Welder No</label>
                    <input
                      type="text"
                      name="welder_no"
                      value={formData.welder_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Weld Length (mm)</label>
                    <input
                      type="number"
                      step="0.1"
                      name="weld_length"
                      value={formData.weld_length}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>NDT Request Date</label>
                    <input
                      type="date"
                      name="ndt_request_date"
                      value={formData.ndt_request_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>NDT Method</label>
                    <select
                      name="ndt_method"
                      value={formData.ndt_method}
                      onChange={handleInputChange}
                    >
                      <option value="">Select Method</option>
                      <option value="UT">Ultrasonic Testing (UT)</option>
                      <option value="RT">Radiographic Testing (RT)</option>
                      <option value="PT">Penetrant Testing (PT)</option>
                      <option value="MT">Magnetic Testing (MT)</option>
                      <option value="VT">Visual Testing (VT)</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>NDT Result</label>
                    <select
                      name="ndt_result"
                      value={formData.ndt_result}
                      onChange={handleInputChange}
                    >
                      <option value="">Select Result</option>
                      <option value="passed">Passed</option>
                      <option value="failed">Failed</option>
                      <option value="pending">Pending</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Status</label>
                    <select
                      name="status"
                      value={formData.status}
                      onChange={handleInputChange}
                    >
                      <option value="pending">Pending</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </div>
                </div>
                <div className="form-buttons">
                  <button type="submit" className="save-btn">
                    {editingRequest ? 'Update' : 'Save'}
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
                <th>Line No</th>
                <th>Spool No</th>
                <th>Joint No</th>
                <th>Welder No</th>
                <th>Weld Process</th>
                <th>Weld Length</th>
                <th>Request Date</th>
                <th>NDT Method</th>
                <th>Result</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {ndtRequests.map((request) => (
                <tr key={request.id}>
                  <td>{request.id}</td>
                  <td>{request.line_no || 'N/A'}</td>
                  <td>{request.spool_no || 'N/A'}</td>
                  <td>{request.joint_no || 'N/A'}</td>
                  <td>{request.welder_no || 'N/A'}</td>
                  <td>{request.weld_process || 'N/A'}</td>
                  <td>{request.weld_length || 'N/A'}</td>
                  <td>{request.ndt_request_date || 'N/A'}</td>
                  <td>{request.ndt_method || 'N/A'}</td>
                  <td>
                    <span className={`result ${request.ndt_result?.toLowerCase()}`}>
                      {request.ndt_result || 'N/A'}
                    </span>
                  </td>
                  <td>
                    <span className={`status ${request.status?.toLowerCase()}`}>
                      {request.status}
                    </span>
                  </td>
                  <td>
                    <button className="action-btn edit" onClick={() => handleEdit(request)}>
                      Edit
                    </button>
                    <button className="action-btn delete" onClick={() => handleDelete(request.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {ndtRequests.length === 0 && !showAddForm && (
          <div className="no-data">
            <p>No NDT requests found.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default NDTRequest
