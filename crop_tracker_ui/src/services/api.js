import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if it exists
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token && token !== 'undefined' && token !== 'null') {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Clear all auth data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('user_role')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (email, password) => api.post('/users/login/', { email, password }),
  logout: () => api.post('/users/logout/'),
  getCurrentUser: () => api.get('/users/me/'),
  register: (userData) => api.post('/users/register/', userData),
  getAllUsers: () => api.get('/users/all/')
}

export const fieldsAPI = {
  getAll: () => api.get('/fields/all/'),
  getById: (id) => api.get(`/fields/${id}/`),
  create: (data) => api.post('/fields/create/', data),
  update: (id, data) => api.put(`/fields/${id}/update/`, data),
  delete: (id) => api.delete(`/fields/${id}/delete/`),  // Add delete method
  getDashboardStats: () => api.get('/fields/dashboard/stats/')
}
/*
export const updatesAPI = {
  create: (data) => api.post('/updates/create/', data),
  getAll: () => api.get('/updates/all/'),
  getByField: (fieldId) => api.get(`/updates/field/${fieldId}/`)
}*/
export const updatesAPI = {
  create: (data) => api.post('/fields/create/updates/', data),
  getAll: () => api.get('/fields/updates/all/'),//
  getByField: (fieldId) => api.get(`fields/updates/${fieldId}/`)
}

export default api