import { getActivePinia } from 'pinia';
import { useMessageStore } from '@/stores/message';
import axios from 'axios';



const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL_PROD,
  timeout: 10000,
});

const token = localStorage.getItem('access_token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token!);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Si la 401 viene de intentar refrescar el token, deslogueamos inmediatamente
    if (
      error.response?.status === 401 &&
      originalRequest.url?.includes('/users/token/refresh/')
    ) {
      const pinia = getActivePinia();
			const messageStore = useMessageStore();
      const { useAuthStore } = await import('@/stores/auth');
      const auth = useAuthStore(pinia);
      auth.logout();
			messageStore.setMessage('Su sesión ha caducado, vuelva a iniciar sesión', 'error');
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const pinia = getActivePinia();
      const { useAuthStore } = await import('@/stores/auth');
      const auth = useAuthStore(pinia);

      // Si no hay refresh token, logout directo
      if (!auth.refreshToken) {
        auth.logout();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // Si ya estamos refrescando, encolamos la petición
        return new Promise<string>((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((newToken) => {
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
            return api(originalRequest);
          })
          .catch(err => Promise.reject(err));
      }

      isRefreshing = true;

      // Intentamos refrescar
      return new Promise(async (resolve, reject) => {
        try {
          await auth.refreshAccessToken();  // si falla, lanza
          const newToken = auth.accessToken!;
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
          processQueue(null, newToken);
          resolve(api(originalRequest));
        } catch (err) {
          processQueue(err, null);
          reject(err);
        } finally {
          isRefreshing = false;
        }
      });
    }

    return Promise.reject(error);
  }
);

export default api;