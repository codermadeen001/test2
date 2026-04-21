<template>
  <div>
    <NavBar />
    
    <!-- Hero Section -->
    <div class="container" style="text-align: center; padding: 3rem 1rem">
      <div style="max-width: 800px; margin: 0 auto">
        <div style="width: 80px; height: 80px; background: var(--crop-green); border-radius: 20px; margin: 0 auto 2rem"></div>
        <h1 style="color: var(--crop-green); font-size: 2.5rem; margin-bottom: 1rem">
          Smart Crop Field Management
        </h1>
        <p style="font-size: 1.125rem; color: #666; margin-bottom: 2rem">
          Track your fields, monitor crop progress, and optimize your harvest with our intelligent field management system.
        </p>
        
        <button @click="showLoginModal = true" class="btn btn-primary" style="font-size: 1.125rem; padding: 1rem 2rem">
          Get Started → Login
        </button>
      </div>
    </div>
    
    <!-- Features Section -->
    <div style="background: var(--white); padding: 3rem 0">
      <div class="container">
        <div class="grid">
          <div class="card" style="text-align: center">
            <div style="font-size: 3rem; margin-bottom: 1rem">🌾</div>
            <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Field Management</h3>
            <p>Create and manage multiple fields with crop types, planting dates, and stage tracking.</p>
          </div>
          
          <div class="card" style="text-align: center">
            <div style="font-size: 3rem; margin-bottom: 1rem">📊</div>
            <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Real-time Updates</h3>
            <p>Field agents can update crop stages and add observations in real-time.</p>
          </div>
          
          <div class="card" style="text-align: center">
            <div style="font-size: 3rem; margin-bottom: 1rem">⚠️</div>
            <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Risk Monitoring</h3>
            <p>Automated status calculation to identify fields that need attention.</p>
          </div>
        </div>
      </div>
    </div>
    
    <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import LoginModal from '../components/LoginModal.vue'

export default {
  name: 'Home',
  components: {
    NavBar,
    LoginModal
  },
  data() {
    return {
      showLoginModal: false
    }
  }
}
</script>