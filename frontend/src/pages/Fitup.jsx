import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import apiConfig from '../config/api'

const Fitup = () => {
  const [fitups, setFitups] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingFitup, setEditingFitup] = useState(null)
  const [selectedRecords, setSelectedRecords] = useState(new Set())
  const [showExportModal, setShowExportModal] = useState(false)
  const [exportForm, setExportForm] = useState({
    project: '',
    location: '',
    report_no: '',
    drawing_no: '',
    inspector: '',
    date: new Date().toISOString().split('T')[0]
  })
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
    fitup_inspection_date: '',
    fitup_report_no: '',
    fitup_result: '',
    status: 'pending'
  })

  useEffect(() => {
    fetchFitups()
  }, [])

  const fetchFitups = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${apiConfig.ENDPOINTS.FITUP}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setFitups(response.data)
    } catch (err) {
      setError('Failed to fetch fitup records')
      console.error('Error fetching fitup records:', err)
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
      
      if (editingFitup) {
        // Update existing fitup
        await axios.put(`${apiConfig.ENDPOINTS.FITUP}/${editingFitup.id}`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      } else {
        // Create new fitup
        await axios.post(`${apiConfig.ENDPOINTS.FITUP}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }
      
      setShowAddForm(false)
      setEditingFitup(null)
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
        fitup_inspection_date: '',
        fitup_report_no: '',
        fitup_result: '',
        status: 'pending'
      })
      fetchFitups() // Refresh the list
    } catch (err) {
      setError('Failed to save fitup record')
      console.error('Error saving fitup record:', err)
    }
  }

  const handleEdit = (fitup) => {
    setEditingFitup(fitup)
    setFormData({
      project_id: fitup.project_id,
      drawing_no: fitup.drawing_no || '',
      line_no: fitup.line_no || '',
      spool_no: fitup.spool_no || '',
      joint_no: fitup.joint_no || '',
      weld_type: fitup.weld_type || '',
      part1_thickness: fitup.part1_thickness || '',
      part1_grade: fitup.part1_grade || '',
      part1_size: fitup.part1_size || '',
      part2_thickness: fitup.part2_thickness || '',
      part2_grade: fitup.part2_grade || '',
      part2_size: fitup.part2_size || '',
      joint_type: fitup.joint_type || '',
      work_site: fitup.work_site || 'shop',
      fitup_inspection_date: fitup.fitup_inspection_date || '',
      fitup_report_no: fitup.fitup_report_no || '',
      fitup_result: fitup.fitup_result || '',
      status: fitup.status
    })
    setShowAddForm(true)
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this fitup record?')) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${apiConfig.ENDPOINTS.FITUP}/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        fetchFitups() // Refresh the list
      } catch (err) {
        setError('Failed to delete fitup record')
        console.error('Error deleting fitup record:', err)
      }
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingFitup(null)
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
      fitup_inspection_date: '',
      fitup_report_no: '',
      fitup_result: '',
      status: 'pending'
    })
  }

  const handleBack = () => {
    navigate('/dashboard')
  }

  const handleRecordSelect = (id) => {
    const newSelected = new Set(selectedRecords)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedRecords(newSelected)
  }

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedRecords(new Set(fitups.map(fitup => fitup.id)))
    } else {
      setSelectedRecords(new Set())
    }
  }

  const handleExportInputChange = (e) => {
    const { name, value } = e.target
    setExportForm(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleExportPDF = async () => {
    if (selectedRecords.size === 0) {
      alert('Please select at least one record to export')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const exportData = {
        record_ids: Array.from(selectedRecords),
        project: exportForm.project,
        location: exportForm.location,
        report_no: exportForm.report_no,
        drawing_no: exportForm.drawing_no,
        inspector: exportForm.inspector,
        date: exportForm.date
      }

      const response = await axios.post(
        `${apiConfig.ENDPOINTS.EXPORT}/pdf/fitups`,
        exportData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          responseType: 'blob'
        }
      )

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `fitup_report_${exportForm.report_no}_${new Date().toISOString().slice(0, 10)}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()

      // Close modal and reset
      setShowExportModal(false)
      setExportForm({
        project: '',
        location: '',
        report_no: '',
        drawing_no: '',
        inspector: '',
        date: new Date().toISOString().split('T')[0]
      })

    } catch (err) {
      console.error('Error exporting PDF:', err)
      alert('Failed to export PDF. Please try again.')
    }
  }

  const handleCancelExport = () => {
    setShowExportModal(false)
    setExportForm({
      project: '',
      location: '',
      report_no: '',
      drawing_no: '',
      inspector: '',
      date: new Date().toISOString().split('T')[0]
    })
  }

  if (loading) return <div className="loading">Loading fitup records...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={handleBack} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>Fitup Inspections</h1>
      </div>

      <div className="module-content">
        <div className="module-actions">
          <button 
            className="add-button" 
            onClick={() => setShowAddForm(true)}
          >
            + Add New Fitup
          </button>
          
          {selectedRecords.size > 0 && (
            <button 
              className="export-button" 
              onClick={() => setShowExportModal(true)}
            >
              📄 Export Selected ({selectedRecords.size})
            </button>
          )}
        </div>

        {showAddForm && (
          <div className="form-overlay">
            <div className="form-container">
              <h2>{editingFitup ? 'Edit Fitup' : 'Add New Fitup'}</h2>
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
                    <label>Inspection Date</label>
                    <input
                      type="date"
                      name="fitup_inspection_date"
                      value={formData.fitup_inspection_date}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Report No</label>
                    <input
                      type="text"
                      name="fitup_report_no"
                      value={formData.fitup_report_no}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="form-group">
                    <label>Fitup Result</label>
                    <select
                      name="fitup_result"
                      value={formData.fitup_result}
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
                    {editingFitup ? 'Update' : 'Save'}
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
                <th>
                  <input
                    type="checkbox"
                    onChange={handleSelectAll}
                    checked={selectedRecords.size === fitups.length && fitups.length > 0}
                  />
                </th>
                <th>ID</th>
                <th>Drawing No</th>
                <th>Line No</th>
                <th>Spool No</th>
                <th>Joint No</th>
                <th>Weld Type</th>
                <th>Part 1 Grade</th>
                <th>Part 2 Grade</th>
                <th>Joint Type</th>
                <th>Work Site</th>
                <th>Inspection Date</th>
                <th>Result</th>
                <th>Report No</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {fitups.map((fitup) => (
                <tr key={fitup.id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedRecords.has(fitup.id)}
                      onChange={() => handleRecordSelect(fitup.id)}
                    />
                  </td>
                  <td>{fitup.id}</td>
                  <td>{fitup.drawing_no || 'N/A'}</td>
                  <td>{fitup.line_no || 'N/A'}</td>
                  <td>{fitup.spool_no || 'N/A'}</td>
                  <td>{fitup.joint_no || 'N/A'}</td>
                  <td>{fitup.weld_type || 'N/A'}</td>
                  <td>{fitup.part1_grade || 'N/A'}</td>
                  <td>{fitup.part2_grade || 'N/A'}</td>
                  <td>{fitup.joint_type || 'N/A'}</td>
                  <td>{fitup.work_site || 'N/A'}</td>
                  <td>{fitup.fitup_inspection_date || 'N/A'}</td>
                  <td>
                    <span className={`result ${fitup.fitup_result?.toLowerCase()}`}>
                      {fitup.fitup_result || 'N/A'}
                    </span>
                  </td>
                  <td>{fitup.fitup_report_no || 'N/A'}</td>
                  <td>
                    <span className={`status ${fitup.status?.toLowerCase()}`}>
                      {fitup.status}
                    </span>
                  </td>
                  <td>
                    <button className="action-btn edit" onClick={() => handleEdit(fitup)}>
                      Edit
                    </button>
                    <button className="action-btn delete" onClick={() => handleDelete(fitup.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {fitups.length === 0 && !showAddForm && (
          <div className="no-data">
            <p>No fitup inspections found.</p>
          </div>
        )}

        {showExportModal && (
          <div className="modal-overlay">
            <div className="modal-container">
              <h2>Export Fit-Up Report to PDF</h2>
              <div className="modal-form">
                <div className="form-group">
                  <label>Project Name *</label>
                  <input
                    type="text"
                    name="project"
                    value={exportForm.project}
                    onChange={handleExportInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Location *</label>
                  <input
                    type="text"
                    name="location"
                    value={exportForm.location}
                    onChange={handleExportInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Report Number *</label>
                  <input
                    type="text"
                    name="report_no"
                    value={exportForm.report_no}
                    onChange={handleExportInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Drawing Number</label>
                  <input
                    type="text"
                    name="drawing_no"
                    value={exportForm.drawing_no}
                    onChange={handleExportInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Inspector Name</label>
                  <input
                    type="text"
                    name="inspector"
                    value={exportForm.inspector}
                    onChange={handleExportInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Date</label>
                  <input
                    type="date"
                    name="date"
                    value={exportForm.date}
                    onChange={handleExportInputChange}
                  />
                </div>
              </div>
              <div className="modal-buttons">
                <button onClick={handleExportPDF} className="export-btn">
                  Export PDF
                </button>
                <button onClick={handleCancelExport} className="cancel-btn">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Fitup
