import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/api/client";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("access_token") || null);
  const refreshToken = ref(localStorage.getItem("refresh_token") || null);
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);

  async function login(email, password) {
    const { data } = await api.post("/auth/token/", { email, password });
    token.value = data.access;
    refreshToken.value = data.refresh;
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    await fetchMe();
  }

  async function fetchMe() {
    const { data } = await api.get("/accounts/me/");
    user.value = data;
  }

  function logout() {
    token.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  return { token, user, isAuthenticated, login, logout, fetchMe };
});
