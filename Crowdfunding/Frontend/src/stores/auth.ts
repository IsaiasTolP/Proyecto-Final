import { defineStore } from "pinia";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: !!localStorage.getItem("access_token"),
  }),
  actions: {
    login(accessToken: string, refreshToken: string) {
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);
      api.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
      this.isAuthenticated = true;
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      delete api.defaults.headers.common["Authorization"];
      this.isAuthenticated = false;
    },
	},
});