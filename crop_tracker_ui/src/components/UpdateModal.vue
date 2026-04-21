<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div style="padding: 2rem">
        <h2 style="color: var(--crop-green); margin-bottom: 1rem">Update Field Stage</h2>
        <p style="margin-bottom: 1.5rem"><strong>{{ field.name }}</strong> - Current: {{ field.current_stage }}</p>
        
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        
        <form @submit.prevent="handleUpdate">
          <div style="margin-bottom: 1rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">New Stage</label>
            <select v-model="newStage" required>
              <option value="">Select new stage</option>
              <option v-for="stage in availableStages" :key="stage" :value="stage">
                {{ stage }}
              </option>
            </select>
          </div>
          
          <div style="margin-bottom: 1.5rem">
            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Notes</label>
            <textarea 
              v-model="notes" 
              rows="3" 
              placeholder="Add observations or notes about the field..."
            ></textarea>
          </div>
          
          <div style="display: flex; gap: 1rem">
            <button type="submit" class="btn btn-primary" style="flex: 1" :disabled="loading">
              {{ loading ? 'Updating...' : 'Update Field' }}
            </button>
            <button type="button" @click="$emit('close')" class="btn btn-secondary" style="flex: 1">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { updatesAPI } from '../services/api'

export default {
  name: 'UpdateModal',
  props: {
    field: Object
  },
  data() {
    return {
      newStage: '',
      notes: '',
      loading: false,
      error: ''
    }
  },
  computed: {
    availableStages() {
      const transitions = {
        'Planted': ['Growing'],
        'Growing': ['Ready'],
        'Ready': ['Harvested'],
        'Harvested': []
      }
      return transitions[this.field.current_stage] || []
    }
  },
  methods: {
    async handleUpdate() {
      if (!this.newStage) {
        this.error = 'Please select a new stage'
        return
      }
      
      this.loading = true
      this.error = ''
      
      try {
        await updatesAPI.create({
          field_id: this.field.id,
          new_stage: this.newStage,
          notes: this.notes
        })
        this.$emit('updated')
        this.$emit('close')
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update field'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>