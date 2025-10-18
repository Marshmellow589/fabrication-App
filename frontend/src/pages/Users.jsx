import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiConfig from '../config/api'

const Users = () => {
  const [users, setUsers] = useState([])
  const [projects, setProjects] = useState([])
  const [assignments, setAssignments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingUser, setEditingUser] = useState(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [showAssignmentForm, setShowAssignmentForm] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [currentUser, setCurrentUser] = useState(null)
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    role: 'visitor',
    is_active: true
  })
  const [newAssignment, setNewAssignment] = useState({
    user_id: '',
    project_id: '',
    project_role: 'viewer',
    assigned_by: ''
  })
  const [editingAssignment, setEditingAssignment] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchUsers()
    fetchProjects()
    fetchAssignments()
    fetchCurrentUser()
  }, [])

  const fetchCurrentUser = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const userData = await response.json()
        setCurrentUser(userData)
      }
    } catch (err) {
      console.error('Error fetching current user:', err)
    }
  }

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch users')
      }

      const data = await response.json()
      setUsers(data)
      setLoading(false)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const fetchProjects = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/projects/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch projects')
      }

      const data = await response.json()
      setProjects(data)
    } catch (err) {
      console.error('Error fetching projects:', err)
    }
  }

  const fetchAssignments = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/assignments/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch assignments')
      }

      const data = await response.json()
      setAssignments(data)
    } catch (err) {
      console.error('Error fetching assignments:', err)
    }
  }

  const handleEdit = (user) => {
    setEditingUser(user)
  }

  const handleUpdate = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/${editingUser.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editingUser)
      })

      if (!response.ok) {
        throw new Error('Failed to update user')
      }

      const updatedUser = await response.json()
      setUsers(users.map(user => user.id === updatedUser.id ? updatedUser : user))
      setEditingUser(null)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to delete user')
      }

      setUsers(users.filter(user => user.id !== userId))
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleChangePassword = (user) => {
    const newPassword = prompt(`Enter new password for ${user.username}:`)
    if (newPassword && newPassword.trim() !== '') {
      updateUserPassword(user.id, newPassword.trim())
    }
  }

  const updateUserPassword = async (userId, newPassword) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/${userId}/password`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: newPassword })
      })

      if (!response.ok) {
        throw new Error('Failed to update password')
      }

      alert('Password updated successfully!')
      setError('')
    } catch (err) {
      setError(err.message)
      alert('Failed to update password: ' + err.message)
    }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/users/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newUser)
      })

      if (!response.ok) {
        throw new Error('Failed to create user')
      }

      const createdUser = await response.json()
      setUsers([...users, createdUser])
      setNewUser({
        username: '',
        email: '',
        full_name: '',
        password: '',
        role: 'visitor',
        is_active: true
      })
      setShowCreateForm(false)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleAssignProject = (user) => {
    setSelectedUser(user)
    setNewAssignment({
      user_id: user.id,
      project_id: '',
      project_role: 'viewer',
      assigned_by: currentUser ? currentUser.id : 1 // Default to admin ID if current user not available
    })
    setShowAssignmentForm(true)
  }

  const handleCreateAssignment = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const assignmentData = {
        ...newAssignment,
        assigned_by: currentUser ? currentUser.id : 1 // Ensure assigned_by is included
      }
      
      const response = await fetch(`${apiConfig.BASE_URL}/assignments/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(assignmentData)
      })

      if (!response.ok) {
        throw new Error('Failed to assign project')
      }

      const createdAssignment = await response.json()
      setAssignments([...assignments, createdAssignment])
      setNewAssignment({
        user_id: '',
        project_id: '',
        project_role: 'viewer',
        assigned_by: ''
      })
      setShowAssignmentForm(false)
      setSelectedUser(null)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleEditAssignment = (assignment) => {
    setEditingAssignment(assignment)
  }

  const handleUpdateAssignment = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/assignments/${editingAssignment.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          project_role: editingAssignment.project_role
        })
      })

      if (!response.ok) {
        throw new Error('Failed to update assignment')
      }

      const updatedAssignment = await response.json()
      setAssignments(assignments.map(assignment => 
        assignment.id === updatedAssignment.id ? updatedAssignment : assignment
      ))
      setEditingAssignment(null)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDeleteAssignment = async (assignmentId) => {
    if (!window.confirm('Are you sure you want to remove this project assignment?')) {
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`${apiConfig.BASE_URL}/assignments/${assignmentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to delete assignment')
      }

      setAssignments(assignments.filter(assignment => assignment.id !== assignmentId))
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const getUserAssignments = (userId) => {
    return assignments.filter(assignment => assignment.user_id === userId)
  }

  if (loading) return <div className="loading">Loading users...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="module-container">
      <div className="module-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>
        <h1>User Management</h1>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="module-actions">
        <button 
          onClick={() => setShowCreateForm(!showCreateForm)} 
          className="add-button"
        >
          {showCreateForm ? 'Cancel' : 'Add New User'}
        </button>
      </div>

      {showCreateForm && (
        <div className="form-container">
          <h3>Create New User</h3>
          <form onSubmit={handleCreate} className="login-form">
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={newUser.username}
                onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Full Name:</label>
              <input
                type="text"
                value={newUser.full_name}
                onChange={(e) => setNewUser({...newUser, full_name: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Role:</label>
              <select
                value={newUser.role}
                onChange={(e) => setNewUser({...newUser, role: e.target.value})}
              >
                <option value="visitor">Visitor</option>
                <option value="member">Member</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={newUser.is_active}
                  onChange={(e) => setNewUser({...newUser, is_active: e.target.checked})}
                />
                Active
              </label>
            </div>
            <button type="submit" className="login-button">Create User</button>
          </form>
        </div>
      )}

      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Full Name</th>
              <th>Role</th>
              <th>Status</th>
              <th>Assigned Projects</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => {
              const userAssignments = getUserAssignments(user.id)
              return (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{user.full_name || '-'}</td>
                  <td>
                    <span className={`status ${user.role}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>
                    <span className={`status ${user.is_active ? 'active' : 'inactive'}`}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    {userAssignments.length > 0 ? (
                      <div className="project-assignments">
                        {userAssignments.map(assignment => (
                          <div key={assignment.id} className="assignment-item">
                            <span className="project-name">{assignment.project_name}</span>
                            <span className={`role ${assignment.project_role}`}>
                              ({assignment.project_role})
                            </span>
                            <button
                              onClick={() => handleEditAssignment(assignment)}
                              className="edit-btn"
                              title="Edit assignment"
                            >
                              ✏️
                            </button>
                            <button
                              onClick={() => handleDeleteAssignment(assignment.id)}
                              className="remove-btn"
                              title="Remove assignment"
                            >
                              ×
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <span className="no-assignments">No projects assigned</span>
                    )}
                  </td>
                  <td style={{whiteSpace: 'nowrap'}}>
                    <button
                      onClick={() => handleEdit(user)}
                      className="action-btn edit"
                      style={{margin: '2px'}}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleChangePassword(user)}
                      className="action-btn password"
                      style={{
                        backgroundColor: '#f39c12', 
                        color: 'white',
                        margin: '2px',
                        padding: '5px 10px',
                        border: 'none',
                        borderRadius: '3px',
                        cursor: 'pointer'
                      }}
                      title="Change Password"
                    >
                      Change Password
                    </button>
                    <button
                      onClick={() => handleAssignProject(user)}
                      className="action-btn assign"
                      style={{
                        backgroundColor: '#3498db',
                        margin: '2px'
                      }}
                    >
                      Assign Project
                    </button>
                    <button
                      onClick={() => handleDelete(user.id)}
                      className="action-btn delete"
                      style={{
                        backgroundColor: '#e74c3c',
                        margin: '2px'
                      }}
                      title="Delete user"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {editingUser && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Edit User</h3>
            <form onSubmit={handleUpdate} className="login-form">
              <div className="form-group">
                <label>Username:</label>
                <input
                  type="text"
                  value={editingUser.username}
                  onChange={(e) => setEditingUser({...editingUser, username: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email:</label>
                <input
                  type="email"
                  value={editingUser.email}
                  onChange={(e) => setEditingUser({...editingUser, email: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Full Name:</label>
                <input
                  type="text"
                  value={editingUser.full_name || ''}
                  onChange={(e) => setEditingUser({...editingUser, full_name: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Role:</label>
                <select
                  value={editingUser.role}
                  onChange={(e) => setEditingUser({...editingUser, role: e.target.value})}
                >
                  <option value="visitor">Visitor</option>
                  <option value="member">Member</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={editingUser.is_active}
                    onChange={(e) => setEditingUser({...editingUser, is_active: e.target.checked})}
                  />
                  Active
                </label>
              </div>
              <div className="modal-actions">
                <button type="submit" className="login-button">Update</button>
                <button
                  type="button"
                  onClick={() => setEditingUser(null)}
                  className="back-button"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showAssignmentForm && selectedUser && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Assign Project to {selectedUser.username}</h3>
            <form onSubmit={handleCreateAssignment} className="login-form">
              <div className="form-group">
                <label>Project:</label>
                <select
                  value={newAssignment.project_id}
                  onChange={(e) => setNewAssignment({...newAssignment, project_id: parseInt(e.target.value)})}
                  required
                >
                  <option value="">Select a project</option>
                  {projects.map(project => (
                    <option key={project.id} value={project.id}>
                      {project.project_number} - {project.project_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Project Role:</label>
                <select
                  value={newAssignment.project_role}
                  onChange={(e) => setNewAssignment({...newAssignment, project_role: e.target.value})}
                >
                  <option value="viewer">Viewer (Read Only)</option>
                  <option value="editor">Editor (Read & Write)</option>
                  <option value="manager">Manager (Full Access)</option>
                </select>
              </div>
              <div className="modal-actions">
                <button type="submit" className="login-button">Assign Project</button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAssignmentForm(false)
                    setSelectedUser(null)
                  }}
                  className="back-button"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {editingAssignment && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Edit Project Assignment</h3>
            <form onSubmit={handleUpdateAssignment} className="login-form">
              <div className="form-group">
                <label>Project:</label>
                <input
                  type="text"
                  value={editingAssignment.project_name}
                  disabled
                  className="disabled-input"
                />
              </div>
              <div className="form-group">
                <label>User:</label>
                <input
                  type="text"
                  value={editingAssignment.username}
                  disabled
                  className="disabled-input"
                />
              </div>
              <div className="form-group">
                <label>Project Role:</label>
                <select
                  value={editingAssignment.project_role}
                  onChange={(e) => setEditingAssignment({...editingAssignment, project_role: e.target.value})}
                >
                  <option value="viewer">Viewer (Read Only)</option>
                  <option value="editor">Editor (Read & Write)</option>
                  <option value="manager">Manager (Full Access)</option>
                </select>
              </div>
              <div className="modal-actions">
                <button type="submit" className="login-button">Update Assignment</button>
                <button
                  type="button"
                  onClick={() => setEditingAssignment(null)}
                  className="back-button"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Users
