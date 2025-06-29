import axios from 'axios';
import { authStore } from '../stores/AuthStore';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// Публичные GET-эндпоинты (без токена)
const publicGetEndpoints = [
  '/login',
  '/register',
  '/pet-reports/', // GET списка
  /^\/pet-reports\/\d+\/$/, // GET деталей
  '/reviews/',
  '/blogs/',
  '/token/refresh'
];

api.interceptors.request.use(config => {
  const path = config.url!.replace(config.baseURL!, '');
  const isPublicGet = config.method === 'get' && 
    publicGetEndpoints.some(pattern => 
      typeof pattern === 'string' ? path === pattern : pattern.test(path)
    );

  if (!isPublicGet && authStore.tokens?.access) {
    config.headers.Authorization = `Bearer ${authStore.tokens.access}`;
  }
  
  // Для FormData автоматически устанавливаем правильный Content-Type
  if (config.data instanceof FormData) {
    config.headers['Content-Type'] = 'multipart/form-data';
  }
  
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const { config, response } = error;
    
    if (response?.status === 401 && !config._retry) {
      config._retry = true;
      if (await authStore.refreshToken()) {
        return api(config);
      }
      authStore.logout();
    }
    
    return Promise.reject(error);
  }
);

export default api;