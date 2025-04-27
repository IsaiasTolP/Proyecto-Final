// src/stores/auth.ts
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'));
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'));
  const user = ref<any>(null);

  const isAuthenticated = computed(() => !!accessToken.value);

  async function login(username: string, password: string) {
    const response = await api.post('/users/login/', { username, password });
    accessToken.value = response.data.access;
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
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  }

  function logout() {
    accessToken.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
  }

  async function refreshAccessToken() {
    try {
      const { data } = await api.post('/users/token/refresh/', {
        refresh: refreshToken.value,
      });
      accessToken.value = data.access;
      refreshToken.value = data.refresh ?? refreshToken.value;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh ?? refreshToken.value);
    } catch {
      logout();
    }
  }

  return { accessToken, user, isAuthenticated, login, register, fetchUser, logout, refreshAccessToken };
});
