import { getActivePinia } from 'pinia';
import axios from 'axios';

const api = axios.create({
    // baseURL: import.meta.env.VITE_API_BASE_URL_PROD,
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000,
});

const token = localStorage.getItem('access_token');
if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const pinia = getActivePinia();
            const { useAuthStore } = await import('@/stores/auth');
            const auth = useAuthStore(pinia);

            await auth.refreshAccessToken();
            if (auth.isAuthenticated) {
                originalRequest.headers['Authorization'] = `Bearer ${auth.accessToken}`;
                return api(originalRequest);
            }
        }
        return Promise.reject(error);
    }
);

export default api;