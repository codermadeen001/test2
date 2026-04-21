<template>
  <nav style="background: var(--white); box-shadow: 0 2px 4px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 100">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center; padding: 1rem">
      <div style="display: flex; align-items: center; gap: 0.5rem">
        <div style="width: 32px; height: 32px; background: var(--crop-green); border-radius: 8px"></div>
        <h1 style="color: var(--crop-green); font-size: 1.25rem">CropTrack</h1>
      </div>
      
      <div v-if="user" style="display: flex; align-items: center; gap: 1rem">
        <span style="color: var(--crop-green)">
          👋 {{ getUserDisplayName() }} ({{ user.role === 'admin' ? 'Admin' : 'Agent' }})
        </span>
        <button @click="handleLogout" class="btn btn-secondary" style="padding: 0.5rem 1rem">
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      user: null
    }
  },
  mounted() {
    this.checkUser()
  },
  methods: {
    checkUser() {
      try {
        const userStr = localStorage.getItem('user')
        if (userStr && userStr !== 'undefined' && userStr !== 'null') {
          this.user = JSON.parse(userStr)
          console.log('NavBar user loaded:', this.user)
        } else {
          this.user = null
        }
      } catch (error) {
        console.error('Error parsing user data:', error)
        this.user = null
        localStorage.removeItem('user')
      }
    },
    getUserDisplayName() {
      if (!this.user) return 'User'
      if (this.user.name && this.user.name !== 'null') {
        return this.user.name
      }
      if (this.user.email) {
        return this.user.email.split('@')[0]
      }
      return 'User'
    },
    async handleLogout() {
      try {
        // Clear all localStorage items
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('user_role')
        
        this.user = null
        
        // Redirect to home
        await this.$router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
        // Force clear and redirect even if error
        localStorage.clear()
        window.location.href = '/'
      }
    }
  }
}
</script>