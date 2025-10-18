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
    console.log('Login attempt started with:', { username, password })

    try {
      // Use URLSearchParams for form data as required by FastAPI OAuth2
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)
      formData.append('grant_type', 'password')

      console.log('Sending authentication request to:', `${apiConfig.ENDPOINTS.AUTH}/token`)
      
      const response = await axios.post(`${apiConfig.ENDPOINTS.AUTH}/token`, 
        formData.toString(),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )

      console.log('Authentication response received:', response.data)
      const token = response.data.access_token
      
      // Create user data from token and username (since /users/me endpoint doesn't work)
      const userData = {
        id: 1, // Default ID since we don't have user info
        username: username,
        email: `${username}@example.com`, // Default email
        role: 'Inspector', // Default role
        permissions: ['read', 'write'], // Default permissions
        token: token
      }
      
      console.log('Created user data:', userData)
      
      // Store user in AuthContext
      console.log('Calling login function from AuthContext...')
      login(userData)
      console.log('Login function completed, user stored in context')
      
      // Redirect to project selection instead of dashboard
      console.log('Navigating to /project-select...')
      navigate('/project-select')
      console.log('Navigation completed')
      
    } catch (err) {
      console.error('Login error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        statusText: err.response?.statusText
      })
      setError('Invalid username or password')
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

      <div className="contact-info">
        <p>Please contact 65-83782324 if you cannot login</p>
      </div>
    </div>
  )
}

export default Login
