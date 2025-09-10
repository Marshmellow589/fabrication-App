import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const FinalInspection = () => {
  const [inspections, setInspections] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingInspection, setEditingInspection] = useState(null)
  const navigate = useNavigate()

  // Form state
  const [formData, setFormData] = useState({
    project_id: 1,
    drawing_no: '',
    line_no: '',
    spool_no: '',
    joint_no: '',
    weld_type: '',
    part1_thickness: '',
    part1_grade: '',
    part1_size: '',
    part2_thickness: '',
    part2_grade: '',
    part2_size: '',
    joint_type: '',
    work_site: 'shop',
    wps_no: '',
    welder_no: '',
    weld_process: '',
    welding_completion_date: '',
    weld_length: '',
    final_inspection_date: '',
    final_report_no: '',
    final_result: '',
    status: 'pending'
  })

  useEffect(() => {
    fetchInspections()
  }, [])

  const fetchInspections = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiConfig.ENDPOINTS.FINAL}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setInspections(response.data)
    } catch (err) {
      setError('Failed to fetch final inspections')
      console.error('Error fetching final inspections:', err)
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
      
      if (editingInspection) {
        // Update existing inspection
        await axios.put(`${apiConfig.ENDPOINTS.FINAL}/${editingInspection.id}`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else {
        // Create new inspection
        await axios.post(`${apiConfig.ENDPOINTS.FINAL}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }
      
      setShowAddForm(false)
      setEditingInspection(null)
      setFormData({
        project_id: 1,
        drawing_no: '',
        line_no: '',
        spool_no: '',
        joint_no: '',
        weld_type: '',
        part1_thickness: '',
        part1_grade: '',
        part1_size: '',
        part2_thickness: '',
        part2_grade: '',
        part2_size: '',
        joint_type: '',
        work_site: 'shop',
        wps_no: '',
        welder_no: '',
        weld_process: '',
        welding_completion_date: '',
        weld_length: '',
        final_inspection_date: '',
        final_report_no: '',
        final_result: '',
        status: 'pending'
      })
      fetchInspections() // Refresh the list
    } catch (err) {
      setError('Failed to save final inspection')
      console.error('Error saving final inspection:', err)
    }
  }

  const handleEdit = (inspection) => {
    setEditingInspection(inspection)
    setFormData({
      project_id: inspection.project_id,
      drawing_no: inspection.drawing_no || '',
      line_no: inspection.line_no || '',
      spool_no: inspection.spool_no || '',
      joint_no: inspection.joint_no || '',
      weld_type: inspection.weld_type || '',
      part1_thickness: inspection.part1_thickness || '',
      part1_grade: inspection.part1_grade || '',
      part1_size: inspection.part1_size || '',
      part2_thickness: inspection.part2_thickness || '',
      part2_grade: inspection.part2_grade || '',
      part2_size: inspection.part2_size || '',
      joint_type: inspection.joint_type || '',
      work_site: inspection.work_site || 'shop',
      wps_no: inspection.wps_no || '',
      welder_no: inspection.welder_no || '',
      weld_process: inspection.weld_process || '',
      welding_completion_date: inspection.welding_completion_date || '',
      weld_length: inspection.weld_length || '',
      final_inspection_date: inspection.final_inspection_date || '',
      final_report_no: inspection.final_report_no || '',
      final_result: inspection.final_result || '',
      status: inspection.status
    })
    setShowAddForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this final inspection record?')) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${apiConfig.ENDPOINTS.FINAL}/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchInspections() // Refresh the list
      } catch (err) {
        setError('Failed to delete final inspection')
        console.error('Error deleting final inspection:', err)
      }
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingInspection(null)
    setFormData({
      project_id: 1,
      drawing_no: '',
      line_no: '',
      spool_no: '',
      joint_no: '',
      weld_type: '',
      part1_thickness: '',
      part1_grade: '',
      part1_size: '',
      part2_thickness: '',
      part2_grade: '',
      part2_size: '',
      joint_type: '',
      work_site: 'shop',
      wps_no: '',
      welder_no: '',
      weld_process: '',
      welding_completion_date: '',
      weld_length: '',
      final_inspection_date: '',
      final_report_no: '',
      final_result: '',
      status: 'pending'
    })
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  if (loading) return <div className="loading">Loading final inspections...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={handleBack} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>Final Inspections</h1>
      </div>

      <div className="module-content">
        <div className="module-actions">
          <button 
            className="add-button" 
            onClick={() => setShowAddForm(true)}
          >
            + Add New Final Inspection
          </button>
        </div>

        {showAddForm && (
          <div className="form-overlay">
            <div className="form-container">
              <h2>{editingInspection ? 'Edit Final Inspection' : 'Add New Final Inspection'}</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label>Drawing No</label>
                    <input
                      type="text"
                      name="drawing_no"
                      value={formData.drawing_no}
                      onChange={handleInputChange}
                    />
                  </div>
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
                    <label>Weld Type</label>
                    <input
                      type="text"
                      name="weld_type"
                      value={formData.weld_type}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 1 Thickness (mm)</label>
                    <input
                      type="number"
                      step="0.1"
                      name="part1_thickness"
                      value={formData.part1_thickness}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 1 Grade</label>
                    <input
                      type="text"
                      name="part1_grade"
                      value={formData.part1_grade}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 1 Size</label>
                    <input
                      type="text"
                      name="part1_size"
                      value={formData.part1_size}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 2 Thickness (mm)</label>
                    <input
                      type="number"
                      step="0.1"
                      name="part2_thickness"
                      value={formData.part2_thickness}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 2 Grade</label>
                    <input
                      type="text"
                      name="part2_grade"
                      value={formData.part2_grade}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Part 2 Size</label>
                    <input
                      type="text"
                      name="part2_size"
                      value={formData.part2_size}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Joint Type</label>
                    <input
                      type="text"
                      name="joint_type"
                      value={formData.joint_type}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Work Site</label>
                    <select
                      name="work_site"
                      value={formData.work_site}
                      onChange={handleInputChange}
                    >
                      <option value="shop">Shop</option>
                      <option value="field">Field</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>WPS No</label>
                    <input
                      type="text"
                      name="wps_no"
                      value={formData.wps_no}
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
                    <label>Weld Process</label>
                    <input
                      type="text"
                      name="weld_process"
                      value={formData.weld_process}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Welding Completion Date</label>
                    <input
                      type="date"
                      name="welding_completion_date"
                      value={formData.welding_completion_date}
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
                    <label>Final Inspection Date</label>
                    <input
                      type="date"
                      name="final_inspection_date"
                      value={formData.final_inspection_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Final Report No</label>
                    <input
                      type="text"
                      name="final_report_no"
                      value={formData.final_report_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Final Result</label>
                    <select
                      name="final_result"
                      value={formData.final_result}
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
                      <option value="approved">Approved</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </div>
                </div>
                <div className="form-buttons">
                  <button type="submit" className="save-btn">
                    {editingInspection ? 'Update' : 'Save'}
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
                <th>Drawing No</th>
                <th>Line No</th>
                <th>Spool No</th>
                <th>Joint No</th>
                <th>WPS No</th>
                <th>Welder No</th>
                <th>Weld Process</th>
                <th>Weld Length</th>
                <th>Completion Date</th>
                <th>Inspection Date</th>
                <th>Result</th>
                <th>Report No</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {inspections.map((inspection) => (
                <tr key={inspection.id}>
                  <td>{inspection.id}</td>
                  <td>{inspection.drawing_no || 'N/A'}</td>
                  <td>{inspection.line_no || 'N/A'}</td>
                  <td>{inspection.spool_no || 'N/A'}</td>
                  <td>{inspection.joint_no || 'N/A'}</td>
                  <td>{inspection.wps_no || 'N/A'}</td>
                  <td>{inspection.welder_no || 'N/A'}</td>
                  <td>{inspection.weld_process || 'N/A'}</td>
                  <td>{inspection.weld_length || 'N/A'}</td>
                  <td>{inspection.welding_completion_date || 'N/A'}</td>
                  <td>{inspection.final_inspection_date || 'N/A'}</td>
                  <td>
                    <span className={`result ${inspection.final_result?.toLowerCase()}`}>
                      {inspection.final_result || 'N/A'}
                    </span>
                  </td>
                  <td>{inspection.final_report_no || 'N/A'}</td>
                  <td>
                    <span className={`status ${inspection.status?.toLowerCase()}`}>
                      {inspection.status}
                    </span>
                  </td>
                  <td>
                    <button className="action-btn edit" onClick={() => handleEdit(inspection)}>
                      Edit
                    </button>
                    <button className="action-btn delete" onClick={() => handleDelete(inspection.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {inspections.length === 0 && !showAddForm && (
          <div className="no-data">
            <p>No final inspections found.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default FinalInspection
