import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth';
import Dashboard from '../views/Dashboard.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  { 
    path: '/search', 
    name: 'LegalSearch', 
    component: () => import('../views/LegalSearch.vue') 
  },
  { 
    path: '/documents', 
    name: 'DocumentGeneration', 
    component: () => import('../views/DocumentGeneration.vue') 
  },
  { 
    path: '/clients', 
    name: 'ClientManagement', 
    component: () => import('../views/ClientManagement.vue') 
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false);

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/');
  }
  else {
    next();
  }
});

export default router; 