<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div style="padding: 2rem">
        <h2 style="color: var(--crop-green); margin-bottom: 1.5rem">Login to CropTrack</h2>
        
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        
        <form @submit.prevent="handleLogin">
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Email</label>
            <input 
              type="email" 
              v-model="email" 
              required 
              placeholder="Enter your email"
              style="width: 100%"
            />
          </div>
          
          <div style="margin-bottom: 1.5rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Password</label>
            <input 
              type="password" 
              v-model="password" 
              required 
              placeholder="Enter your password"
              style="width: 100%"
            />
          </div>
          
          <button type="submit" class="btn btn-primary" style="width: 100%" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        
        <div style="margin-top: 1rem; text-align: center; font-size: 0.875rem; color: #666">
          <p>Demo Credentials:</p>
          <p>Admin: syeundainnocent@gmail.com / demo123_Admin</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../services/api'

export default {
  name: 'LoginModal',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await authAPI.login(this.email, this.password)
        
        // Check if login was successful
        if (response.data.success) {
          // Store the token
          if (response.data.token) {
            localStorage.setItem('token', response.data.token)
          }
          
          // Store user role
          if (response.data.role) {
            localStorage.setItem('user_role', response.data.role)
          }
          
          // Store user data (already an object, no need to stringify twice)
          if (response.data.user) {
            // Make sure user has a name, if null provide a default
            const userData = {
              ...response.data.user,
              name: response.data.user.name || response.data.user.email.split('@')[0] || 'User'
            }
            localStorage.setItem('user', JSON.stringify(userData))
          }
          
          console.log('Login successful, user stored:', localStorage.getItem('user'))
          
          // Redirect based on role
          if (response.data.role === 'admin') {
            await this.$router.push('/admin')
          } else {
            await this.$router.push('/agent')
          }
          
          this.$emit('close')
        } else {
          this.error = response.data.message || 'Login failed. Please try again.'
        }
      } catch (error) {
        console.error('Login error:', error)
        if (error.response?.data) {
          this.error = error.response.data.message || 'Login failed. Please try again.'
        } else if (error.message === 'Network Error') {
          this.error = 'Cannot connect to server. Please check if backend is running.'
        } else {
          this.error = 'Login failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>