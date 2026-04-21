<template>
  <div class="card">
    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem">
      <h3 style="color: var(--crop-green); font-size: 1.25rem">{{ field.name }}</h3>
      <div style="display: flex; gap: 0.5rem; align-items: center">
        <span :class="['status-badge', statusClass]">{{ statusText }}</span>
        <!-- Edit and Delete Icons - Only show for admin -->
        <button 
          v-if="showActions" 
          @click="$emit('edit-field', field)" 
          class="icon-btn icon-edit"
          title="Edit Field"
        >
          ✏️
        </button>
        <button 
          v-if="showActions" 
          @click="$emit('delete-field', field)" 
          class="icon-btn icon-delete"
          title="Delete Field"
        >
          🗑️
        </button>
      </div>
    </div>
    
    <div style="margin-bottom: 1rem">
      <p><strong>Crop:</strong> {{ field.crop_type }}</p>
      <p><strong>Planted:</strong> {{ formatDate(field.planting_date) }}</p>
      <p><strong>Stage:</strong> {{ field.current_stage }}</p>
      <p v-if="field.assigned_agent_name"><strong>Agent:</strong> {{ field.assigned_agent_name }}</p>
    </div>
    
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
      <button 
        v-if="canUpdate" 
        @click="$emit('update-stage', field)" 
        class="btn btn-primary" 
        style="flex: 1; padding: 0.5rem"
      >
        Update Stage
      </button>
      <button 
        @click="$emit('view-updates', field)" 
        class="btn btn-secondary" 
        style="flex: 1; padding: 0.5rem"
      >
        View History
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FieldCard',
  props: {
    field: Object,
    canUpdate: Boolean,
    showActions: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    statusText() {
      return this.field.status || 'Active'
    },
    statusClass() {
      const status = this.field.status || 'Active'
      if (status === 'Active') return 'status-active'
      if (status === 'At Risk') return 'status-at-risk'
      return 'status-completed'
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.icon-edit:hover {
  background-color: #e8f5e9;
  transform: scale(1.1);
}

.icon-delete:hover {
  background-color: #ffebee;
  transform: scale(1.1);
}
</style>