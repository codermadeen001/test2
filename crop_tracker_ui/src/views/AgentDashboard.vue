<template>
  <div>
    <NavBar />
    
    <div class="container">
      <!-- Header -->
      <div style="margin-bottom: 2rem">
        <h1 style="color: var(--crop-green)">My Assigned Fields</h1>
        <p style="color: #666">Welcome back, {{ user?.name }}! Here are your fields to manage.</p>
      </div>
      
      <!-- Statistics Cards -->
      <div class="grid" style="margin-bottom: 2rem">
        <div class="card" style="text-align: center">
          <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">My Fields</h3>
          <p style="font-size: 2rem; font-weight: bold">{{ stats.total_fields || 0 }}</p>
        </div>
        
        <div class="card" style="text-align: center">
          <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Active</h3>
          <p style="font-size: 2rem; font-weight: bold; color: var(--crop-green)">
            {{ stats.status_breakdown?.Active || 0 }}
          </p>
        </div>
        
        <div class="card" style="text-align: center">
          <h3 style="color: var(--danger-red); margin-bottom: 0.5rem">At Risk</h3>
          <p style="font-size: 2rem; font-weight: bold; color: var(--danger-red)">
            {{ stats.status_breakdown?.['At Risk'] || 0 }}
          </p>
        </div>
        
        <div class="card" style="text-align: center">
          <h3 style="color: #666; margin-bottom: 0.5rem">Completed</h3>
          <p style="font-size: 2rem; font-weight: bold">
            {{ stats.status_breakdown?.Completed || 0 }}
          </p>
        </div>
      </div>
      
      <!-- Search Bar - 80% width -->
      <div style="margin-bottom: 2rem; display: flex; justify-content: center;">
        <div style="width: 80%;">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="🔍 Search your fields by name..." 
            style="width: 100%; padding: 0.75rem 1rem; border: 2px solid var(--gray-border); border-radius: 8px; font-size: 1rem;"
          />
          <div v-if="searchQuery" style="margin-top: 0.5rem; font-size: 0.875rem; color: #666; text-align: center;">
            Showing {{ filteredFields.length }} of {{ fields.length }} fields
            <button @click="clearSearch" style="margin-left: 0.5rem; background: none; border: none; color: var(--crop-green); cursor: pointer;">
              Clear search
            </button>
          </div>
        </div>
      </div>
      
      <!-- Fields List -->
      <h2 style="color: var(--crop-green); margin-bottom: 1rem">
        My Fields
        <span v-if="searchQuery" style="font-size: 0.9rem; color: #666;">
          (Showing {{ filteredFields.length }} of {{ fields.length }} fields)
        </span>
      </h2>
      
      <div v-if="loading" class="spinner"></div>
      
      <div v-else class="grid">
        <FieldCard 
          v-for="field in filteredFields" 
          :key="field.id"
          :field="field"
          :can-update="field.current_stage !== 'Harvested'"
          @update-stage="showUpdateModal = true; selectedField = field"
          @view-updates="viewUpdates"
        />
      </div>
      
      <div v-if="!loading && filteredFields.length === 0 && fields.length > 0" style="text-align: center; padding: 3rem">
        <p>No fields match "{{ searchQuery }}". Try a different search term.</p>
      </div>
      
      <div v-if="!loading && fields.length === 0" style="text-align: center; padding: 3rem">
        <p>No fields assigned to you yet. Contact your admin for assignments.</p>
      </div>
    </div>
    
    <!-- Update Modal -->
    <UpdateModal 
      v-if="showUpdateModal"
      :field="selectedField"
      @close="showUpdateModal = false"
      @updated="handleUpdateComplete"
    />
    
    <!-- Updates History Modal -->
    <div v-if="showUpdates" class="modal-overlay" @click.self="showUpdates = false">
      <div class="modal-content">
        <div style="padding: 2rem">
          <h2 style="color: var(--crop-green); margin-bottom: 1rem">Field Update History</h2>
          <h3 style="margin-bottom: 1rem">{{ selectedField?.name }}</h3>
          
          <div v-if="updatesLoading" class="spinner"></div>
          
          <div v-else>
            <div v-if="updates.length === 0" style="text-align: center; padding: 2rem">
              <p>No updates yet for this field.</p>
            </div>
            
            <div v-for="update in updates" :key="update.id" class="card" style="margin-bottom: 1rem; padding: 1rem">
              <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem">
                <strong>{{ update.agent_name }}</strong>
                <small>{{ formatDate(update.created_at) }}</small>
              </div>
              <p>Stage: {{ update.old_stage }} → {{ update.new_stage }}</p>
              <p v-if="update.notes" style="margin-top: 0.5rem; color: #666">{{ update.notes }}</p>
            </div>
          </div>
          
          <button @click="showUpdates = false" class="btn btn-secondary" style="margin-top: 1rem; width: 100%">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import FieldCard from '../components/FieldCard.vue'
import UpdateModal from '../components/UpdateModal.vue'
import { fieldsAPI, updatesAPI } from '../services/api'

export default {
  name: 'AgentDashboard',
  components: {
    NavBar,
    FieldCard,
    UpdateModal
  },
  data() {
    return {
      fields: [],
      stats: {},
      loading: true,
      showUpdateModal: false,
      selectedField: null,
      showUpdates: false,
      updates: [],
      updatesLoading: false,
      user: null,
      searchQuery: '' 
    }
  },
  computed: {
    
    filteredFields() {
      if (!this.searchQuery) {
        return this.fields
      }
      const query = this.searchQuery.toLowerCase()
      return this.fields.filter(field => 
        field.name.toLowerCase().includes(query)
      )
    }
  },
  mounted() {
    this.loadData()
    const userStr = localStorage.getItem('user')
    this.user = userStr ? JSON.parse(userStr) : null
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [fieldsRes, statsRes] = await Promise.all([
          fieldsAPI.getAll(),
          fieldsAPI.getDashboardStats()
        ])
        this.fields = fieldsRes.data.fields || []
        this.stats = statsRes.data
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        this.loading = false
      }
    },
    
    // Add clear search method
    clearSearch() {
      this.searchQuery = ''
    },
    
    handleUpdateComplete() {
      this.showUpdateModal = false
      this.loadData()
    },
    
    async viewUpdates(field) {
      this.selectedField = field
      this.showUpdates = true
      this.updatesLoading = true
      
      try {
        const response = await updatesAPI.getByField(field.id)
        this.updates = response.data.updates || []
      } catch (error) {
        console.error('Failed to load updates:', error)
      } finally {
        this.updatesLoading = false
      }
    },
    
    formatDate(date) {
      return new Date(date).toLocaleString()
    }
  }
}
</script>