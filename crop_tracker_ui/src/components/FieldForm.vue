<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div style="padding: 2rem">
        <h2 style="color: var(--crop-green); margin-bottom: 1.5rem">
          {{ editing ? 'Edit Field' : 'Create New Field' }}
        </h2>
        
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        
        <form @submit.prevent="handleSubmit">
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Field Name</label>
            <input 
              v-model="form.name" 
              required 
              placeholder="e.g., North Field 40 acres"
              :disabled="isSubmitting"
            />
          </div>
          
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Crop Type</label>
            <select v-model="form.crop_type" required :disabled="isSubmitting">
              <option value="">Select crop</option>
              <option value="Corn">Corn</option>
              <option value="Wheat">Wheat</option>
              <option value="Soybeans">Soybeans</option>
              <option value="Rice">Rice</option>
              <option value="Barley">Barley</option>
            </select>
          </div>
          
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Planting Date</label>
            <input 
              type="date" 
              v-model="form.planting_date" 
              required 
              :disabled="isSubmitting"
            />
          </div>
          
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Assign to Agent</label>
            <select v-model="form.assigned_agent_id" :disabled="isSubmitting">
              <option :value="null">Unassigned</option>
              <option v-for="agent in agents" :key="agent.id" :value="agent.id">
                {{ agent.name }} 
              </option>
            </select>
          </div>
          
          <div style="display: flex; gap: 1rem; margin-top: 1.5rem">
            <button type="submit" class="btn btn-primary" style="flex: 1" :disabled="isSubmitting">
              {{ isSubmitting ? 'Creating...' : (editing ? 'Update' : 'Create') }}
            </button>
            <button type="button" @click="$emit('close')" class="btn btn-secondary" style="flex: 1" :disabled="isSubmitting">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../services/api'

export default {
  name: 'FieldForm',
  props: {
    editing: Boolean,
    fieldData: Object
  },
  data() {
    return {
      form: {
        name: '',
        crop_type: '',
        planting_date: '',
        assigned_agent_id: null
      },
      agents: [],
      error: '',
      isSubmitting: false
    }
  },
  mounted() {
    this.loadAgents()
    if (this.editing && this.fieldData) {
      this.form = { ...this.fieldData }
      this.form.planting_date = this.fieldData.planting_date?.split('T')[0] || ''
    }
  },
  methods: {
    async loadAgents() {
      try {
        const response = await authAPI.getAllUsers()
        this.agents = response.data.users.filter(u => u.role === 'agent')
      } catch (error) {
        console.error('Failed to load agents:', error)
      }
    },
    handleSubmit() {
      // Prevent double submission
      if (this.isSubmitting) {
        console.log('Already submitting, ignoring...')
        return
      }
      
      // Validate form
      if (!this.form.name || !this.form.crop_type || !this.form.planting_date) {
        this.error = 'Please fill all required fields'
        return
      }
      
      // Clear previous error
      this.error = ''
      
      // Set submitting flag
      this.isSubmitting = true
      
      // Create a clean copy of the data
      const submitData = {
        name: this.form.name,
        crop_type: this.form.crop_type,
        planting_date: this.form.planting_date,
        assigned_agent_id: this.form.assigned_agent_id
      }
      
      console.log('Emitting submit with data:', submitData)
      
      // Emit the submit event
      this.$emit('submit', submitData)
      
      // Reset submitting flag after a delay
      setTimeout(() => {
        this.isSubmitting = false
      }, 2000)
    }
  }
}
</script>