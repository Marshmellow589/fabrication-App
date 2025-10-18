import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import apiConfig from '../../config/api'

const Login = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Use URLSearchParams for form data as required by FastAPI OAuth2
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)
      formData.append('grant_type', 'password')

      const response = await axios.post(`${apiConfig.ENDPOINTS.AUTH}/token`, 
        formData.toString(),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )

      const token = response.data.access_token
      
      // Get user info using the token
      const userResponse = await axios.get(`${apiConfig.ENDPOINTS.USERS}/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      const userData = {
        ...userResponse.data,
        token: token
      }
      
      // Store user in AuthContext
      login(userData)
      console.log('Login successful, user:', userData)
      
      // Redirect to project selection instead of dashboard
      navigate('/project-select')
      
    } catch (err) {
      setError('Invalid username or password')
      console.error('Login error:', err.response?.data || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter your username"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter your password"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading} className="login-button">
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <div className="test-credentials">
        <h3>Test Credentials:</h3>
        <p><strong>VISITOR:</strong> username: VISITOR, password: visitor123</p>
        <p><strong>MEMBER:</strong> username: MEMBER, password: member123</p>
        <p><strong>ADMIN:</strong> username: admin2, password: admin123</p>
      </div>
    </div>
  )
}

export default Login
