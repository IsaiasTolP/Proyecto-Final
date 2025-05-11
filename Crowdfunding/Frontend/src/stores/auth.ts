import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import api from '@/services/api';
import type { User } from '@/interfaces/Account';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'));
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'));
  const user = ref<User | null>(null);

  const isAuthenticated = computed(() => !!accessToken.value);

  async function login(username: string, password: string) {
    const response = await api.post('/users/login/', { username, password });
    accessToken.value = response.data.access;
    refreshToken.value = response.data.refresh;
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
    await fetchUser();
  }

  async function register(username: string, email: string, password: string, is_founder: boolean) {
    await api.post('/users/register/', { username, email, password, is_founder });
  }

  async function fetchUser() {
    try {
      const response = await api.get('/users/me/');
      user.value = response.data;
    } catch (error) { }
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];

    router.push('/auth');
  }

  async function refreshAccessToken() {
    try {
      const { data } = await api.post('/users/token/refresh/', {
        refresh: refreshToken.value,
      });
      accessToken.value = data.access;
      refreshToken.value = data.refresh ?? refreshToken.value;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh ?? refreshToken.value!);
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
    } catch (error) {
      // Si falla el refresh, limpieza y relanzar el error para que el interceptor capte el error
      logout();
      throw error;
    }
  }

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    fetchUser,
    logout,
    refreshAccessToken,
  };
});