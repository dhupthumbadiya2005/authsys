import axios from 'axios';

// Dynamically detect hostname and use same for API
const API_BASE_URL = `http://${window.location.hostname}:8000`;

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Simple API without authentication headers

export const authAPI = {
  // Registration endpoints
  registerBegin: (username) => 
    api.post('/api/auth/register/begin', { username }),
  
  registerComplete: (username, credential) => 
    api.post('/api/auth/register/complete', { username, credential }),
  
  // Login endpoints
  loginBegin: (username) => 
    api.post('/api/auth/login/begin', { username }),
  
  loginComplete: (username, credential) => 
    api.post('/api/auth/login/complete', { username, credential }),
};

// No user API needed - WebAuthn handles authentication directly

export default api;
