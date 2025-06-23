<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">
    <div class="w-full max-w-md p-8 space-y-8 bg-gray-800 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-white">LegisLink AI</h1>
        <p class="mt-2 text-gray-400">Inicia sesión para continuar</p>
      </div>
      <form class="space-y-6" @submit.prevent="handleLogin">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300">Correo Electrónico</label>
          <div class="mt-1">
            <input id="email" name="email" type="email" autocomplete="email" required v-model="email"
                   class="w-full px-3 py-2 text-white bg-gray-700 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-300">Contraseña</label>
          <div class="mt-1">
            <input id="password" name="password" type="password" autocomplete="current-password" required v-model="password"
                   class="w-full px-3 py-2 text-white bg-gray-700 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
                   class="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500">
            <label for="remember-me" class="ml-2 block text-sm text-gray-300">Recuérdame</label>
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-blue-400 hover:text-blue-300">¿Olvidaste tu contraseña?</a>
          </div>
        </div>

        <div>
          <button type="submit"
                  class="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Iniciar Sesión
          </button>
        </div>
      </form>
       <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../store/auth';

export default {
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      email: '',
      password: '',
      error: ''
    };
  },
  methods: {
    handleLogin() {
      // Lógica de autenticación simulada
      if (this.email === 'admin@legislink.com' && this.password === 'password') {
        this.error = '';
        this.authStore.login();
        this.$router.push('/');
      } else {
        this.error = 'Credenciales inválidas. Inténtalo de nuevo.';
      }
    }
  }
};
</script> 