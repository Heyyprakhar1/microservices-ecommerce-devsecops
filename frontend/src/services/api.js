import axios from 'axios';

export const authAPI = axios.create({
  baseURL: '/api/auth',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const orderAPI = axios.create({
  baseURL: '/api/orders',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const productAPI = axios.create({
  baseURL: '/api/products',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add JWT token to requests
authAPI.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

orderAPI.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

productAPI.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

