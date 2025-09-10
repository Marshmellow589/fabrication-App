import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import apiConfig from '../../config/api'

const Login = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${apiConfig.ENDPOINTS.AUTH}/token`, {
        username,
        password
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      const token = response.data.access_token
      localStorage.setItem('token', token)
      console.log('Login successful, token:', token)
      // Redirect to dashboard
      navigate('/dashboard')
      
    } catch (err) {
      setError('Invalid username or password')
      console.error('Login error:', err)
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
