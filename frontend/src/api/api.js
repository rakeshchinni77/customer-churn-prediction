import axios from 'axios';
import { API_BASE_URL } from '../constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Unable to connect to FastAPI backend server.');
  }
};

export const modelInfo = async () => {
  try {
    const response = await api.get('/model-info');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch model metadata.');
  }
};

export const predictCustomer = async (customerData) => {
  try {
    const response = await api.post('/predict', customerData);
    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.error ||
      error.response?.data?.detail ||
      'Prediction service encountered an error.';
    throw new Error(message);
  }
};

export default api;
