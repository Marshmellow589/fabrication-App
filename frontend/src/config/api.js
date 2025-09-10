// API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default {
  BASE_URL: API_BASE_URL,
  ENDPOINTS: {
    AUTH: `${API_BASE_URL}/auth`,
    USERS: `${API_BASE_URL}/users`,
    PROJECTS: `${API_BASE_URL}/projects`,
    MATERIAL: `${API_BASE_URL}/material`,
    FITUP: `${API_BASE_URL}/fitup`,
    FINAL: `${API_BASE_URL}/final`,
    NDT: `${API_BASE_URL}/ndt`,
    EXPORT: `${API_BASE_URL}/export`,
    DASHBOARD: `${API_BASE_URL}/dashboard`
  }
};
