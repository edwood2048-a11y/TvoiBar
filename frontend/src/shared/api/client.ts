import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8001/api/v1', // или ваш backend URL
});

// apiClient.defaults.withCredentials = true;

export default apiClient;