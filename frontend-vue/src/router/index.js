import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../lib/api'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../views/Landing.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/opportunities/:id',
    name: 'opportunity-detail',
    component: () => import('../views/OpportunityDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/applications',
    name: 'applications',
    component: () => import('../views/ApplicationsList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/applications/:id',
    name: 'application-detail',
    component: () => import('../views/ApplicationDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/Settings.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const isAuthed = !!getToken()

  if (to.meta.requiresAuth && !isAuthed) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.guestOnly && isAuthed) {
    return { name: 'dashboard' }
  }

  return true
})

export default router
