// API utility functions with automatic token handling
import apiConfig from '../config/api.js';

// Get token from localStorage
const getToken = () => {
  return localStorage.getItem('token');
};

// Create headers with authentication token
const getAuthHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Generic API request function
export const apiRequest = async (url, options = {}) => {
  const headers = {
    ...getAuthHeaders(),
    ...options.headers
  };

  const config = {
    ...options,
    headers
  };

  try {
    const response = await fetch(url, config);
    
    // Handle authentication errors
    if (response.status === 401) {
      // Clear authentication and redirect to login
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      window.location.href = '/login';
      throw new Error('Authentication failed');
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Specific API methods
export const apiGet = (endpoint) => apiRequest(endpoint);
export const apiPost = (endpoint, data) => apiRequest(endpoint, {
  method: 'POST',
  body: JSON.stringify(data)
});
export const apiPut = (endpoint, data) => apiRequest(endpoint, {
  method: 'PUT',
  body: JSON.stringify(data)
});
export const apiDelete = (endpoint) => apiRequest(endpoint, {
  method: 'DELETE'
});

// Authentication API calls
export const authAPI = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch(`${apiConfig.ENDPOINTS.AUTH}/token`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    return data;
  },
  
  getCurrentUser: async () => {
    return apiGet(`${apiConfig.ENDPOINTS.AUTH}/me`);
  }
};

// Final Inspection API calls
export const finalInspectionAPI = {
  getAll: () => apiGet(apiConfig.ENDPOINTS.FINAL),
  getById: (id) => apiGet(`${apiConfig.ENDPOINTS.FINAL}/${id}`),
  create: (data) => apiPost(apiConfig.ENDPOINTS.FINAL, data),
  update: (id, data) => apiPut(`${apiConfig.ENDPOINTS.FINAL}/${id}`, data),
  getFitupData: (fitupId) => apiGet(`${apiConfig.ENDPOINTS.FINAL}/fitup/${fitupId}`),
  requestNDT: (inspectionId, ndtMethod) => apiPost(`${apiConfig.ENDPOINTS.FINAL}/${inspectionId}/request-ndt`, { ndt_method: ndtMethod })
};

// NDT API calls
export const ndtAPI = {
  getAll: () => apiGet(apiConfig.ENDPOINTS.NDT),
  getById: (id) => apiGet(`${apiConfig.ENDPOINTS.NDT}/${id}`),
  create: (data) => apiPost(apiConfig.ENDPOINTS.NDT, data),
  update: (id, data) => apiPut(`${apiConfig.ENDPOINTS.NDT}/${id}`, data),
  createFromFinal: (finalInspectionId, ndtMethod) => apiPost(`${apiConfig.ENDPOINTS.NDT}/from-final/${finalInspectionId}`, { ndt_method: ndtMethod })
};

// Projects API calls
export const projectsAPI = {
  getAll: () => apiGet(apiConfig.ENDPOINTS.PROJECTS),
  getById: (id) => apiGet(`${apiConfig.ENDPOINTS.PROJECTS}/${id}`),
  create: (data) => apiPost(apiConfig.ENDPOINTS.PROJECTS, data),
  update: (id, data) => apiPut(`${apiConfig.ENDPOINTS.PROJECTS}/${id}`, data)
};

// Materials API calls
export const materialsAPI = {
  getAll: () => apiGet(apiConfig.ENDPOINTS.MATERIAL),
  getById: (id) => apiGet(`${apiConfig.ENDPOINTS.MATERIAL}/${id}`),
  create: (data) => apiPost(apiConfig.ENDPOINTS.MATERIAL, data),
  update: (id, data) => apiPut(`${apiConfig.ENDPOINTS.MATERIAL}/${id}`, data)
};

// Fitup API calls
export const fitupAPI = {
  getAll: () => apiGet(apiConfig.ENDPOINTS.FITUP),
  getById: (id) => apiGet(`${apiConfig.ENDPOINTS.FITUP}/${id}`),
  create: (data) => apiPost(apiConfig.ENDPOINTS.FITUP, data),
  update: (id, data) => apiPut(`${apiConfig.ENDPOINTS.FITUP}/${id}`, data)
};

// Dashboard API calls
export const dashboardAPI = {
  getStats: () => apiGet(apiConfig.ENDPOINTS.DASHBOARD)
};
