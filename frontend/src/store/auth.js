import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true'
  }),
  actions: {
    login() {
      this.isAuthenticated = true;
      localStorage.setItem('isAuthenticated', 'true');
    },
    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem('isAuthenticated');
    }
  }
}); 