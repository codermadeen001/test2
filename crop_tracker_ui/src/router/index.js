import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AgentDashboard from '../views/AgentDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/agent',
    name: 'Agent',
    component: AgentDashboard,
    meta: { requiresAuth: true, role: 'agent' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard with proper error handling
router.beforeEach(async (to, from, next) => {
  try {
    // Safely get and parse user from localStorage
    const userStr = localStorage.getItem('user')
    let user = null
    
    if (userStr && userStr !== 'undefined' && userStr !== 'null') {
      try {
        user = JSON.parse(userStr)
      } catch (parseError) {
        console.error('Error parsing user data:', parseError)
        // Clear invalid data
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        localStorage.removeItem('user_role')
        user = null
      }
    }
    
    // Check if route requires authentication
    if (to.meta.requiresAuth) {
      if (!user) {
        // Not logged in, redirect to home
        next('/')
      } else if (to.meta.role && user.role !== to.meta.role) {
        // Wrong role, redirect to appropriate dashboard
        next(user.role === 'admin' ? '/admin' : '/agent')
      } else {
        // Authorized, proceed
        next()
      }
    } else {
      // Public route, proceed
      next()
    }
  } catch (error) {
    console.error('Router guard error:', error)
    // Clear any corrupted data and redirect to home
    localStorage.clear()
    next('/')
  }
})

export default router