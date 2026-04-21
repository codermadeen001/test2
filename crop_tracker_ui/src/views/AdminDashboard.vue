<template>
  <div>
    <NavBar />
    
    <div class="container">
      <!-- Header -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem">
        <h1 style="color: var(--crop-green)">Admin Dashboard</h1>
        <div style="display: flex; gap: 1rem">
          <button @click="openAddAgentModal" class="btn btn-primary">
            + Add New Agent
          </button>
          <button @click="openCreateFieldModal" class="btn btn-secondary">
            + Create New Field
          </button>
        </div>
      </div>
      
      <!-- Statistics Cards -->
      <div class="grid" style="margin-bottom: 2rem">
        <div class="card" style="text-align: center">
          <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Total Fields</h3>
          <p style="font-size: 2rem; font-weight: bold">{{ stats.total_fields || 0 }}</p>
        </div>
        
        <div class="card" style="text-align: center">
          <h3 style="color: var(--crop-green); margin-bottom: 0.5rem">Active Fields</h3>
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
      

<div style="margin-bottom: 2rem">
  <div style="width: 100%;">
    <input 
      type="text" 
      v-model="searchQuery" 
      placeholder="🔍 Search fields by name..." 
      style="width: 100%; padding: 0.75rem 1rem; border: 2px solid var(--gray-border); border-radius: 8px; font-size: 1rem;"
    />
    <div v-if="searchQuery" style="margin-top: 0.5rem; font-size: 0.875rem; color: #666;">
      Showing {{ filteredFields.length }} of {{ fields.length }} fields
      <button @click="clearSearch" style="margin-left: 0.5rem; background: none; border: none; color: var(--crop-green); cursor: pointer;">
        Clear search
      </button>
    </div>
  </div>
</div>
      
      <!-- Fields List -->
      <h2 style="color: var(--crop-green); margin-bottom: 1rem">
        All Fields 
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
          :can-update="false"
          :show-actions="true"
          @view-updates="viewUpdates"
          @edit-field="openEditFieldModal"
          @delete-field="confirmDeleteField"
        />
      </div>
      
      <div v-if="!loading && filteredFields.length === 0 && fields.length > 0" style="text-align: center; padding: 3rem">
        <p>No fields match "{{ searchQuery }}". Try a different search term.</p>
      </div>
      
      <div v-if="!loading && fields.length === 0" style="text-align: center; padding: 3rem">
        <p>No fields created yet. Click "Create New Field" to get started.</p>
      </div>
    </div>
    
    <!-- Add Agent Modal -->
    <div v-if="showAddAgent" class="modal-overlay" @click.self="closeAgentModal">
      <div class="modal-content">
        <div style="padding: 2rem">
          <h2 style="color: var(--crop-green); margin-bottom: 1.5rem">Add New Field Agent</h2>
          
          <div v-if="agentError" class="alert alert-error">{{ agentError }}</div>
          <div v-if="agentSuccess" class="alert alert-success">{{ agentSuccess }}</div>
          
          <form @submit.prevent="handleAddAgent">
            <div style="margin-bottom: 1rem">
              <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Full Name</label>
              <input 
                type="text" 
                v-model="newAgent.name" 
                required 
                placeholder="Enter agent's full name"
                style="width: 100%"
                :disabled="agentLoading"
              />
            </div>
            
            <div style="margin-bottom: 1rem">
              <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Email Address</label>
              <input 
                type="email" 
                v-model="newAgent.email" 
                required 
                placeholder="agent@example.com"
                style="width: 100%"
                :disabled="agentLoading"
              />
            </div>
            
            <div style="margin-bottom: 1.5rem">
              <label style="display: block; margin-bottom: 0.5rem; font-weight: 500">Password</label>
              <input 
                type="password" 
                v-model="newAgent.password" 
                required 
                placeholder="Enter password"
                style="width: 100%"
                :disabled="agentLoading"
              />
            </div>
            
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem">
              <button type="submit" class="btn btn-primary" style="flex: 1" :disabled="agentLoading">
                {{ agentLoading ? 'Creating Agent...' : 'Create Agent' }}
              </button>
              <button type="button" @click="closeAgentModal" class="btn btn-secondary" style="flex: 1" :disabled="agentLoading">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Create Field Modal -->
    <FieldForm 
      v-if="showCreateField"
      :editing="false"
      @close="closeCreateFieldModal"
      @submit="createField"
    />
    
    <!-- Edit Field Modal -->
    <FieldForm 
      v-if="showEditField"
      :editing="true"
      :field-data="editingField"
      @close="closeEditFieldModal"
      @submit="updateField"
    />
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal-content">
        <div style="padding: 2rem">
          <h2 style="color: var(--danger-red); margin-bottom: 1rem">Confirm Delete</h2>
          <p style="margin-bottom: 1.5rem">
            Are you sure you want to delete field <strong>{{ fieldToDelete?.name }}</strong>?
            This action cannot be undone.
          </p>
          
          <div style="display: flex; gap: 1rem">
            <button @click="deleteField" class="btn btn-danger" style="flex: 1" :disabled="isDeleting">
              {{ isDeleting ? 'Deleting...' : 'Yes, Delete' }}
            </button>
            <button @click="closeDeleteModal" class="btn btn-secondary" style="flex: 1">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Updates History Modal -->
    <div v-if="showUpdates" class="modal-overlay" @click.self="closeUpdatesModal">
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
          
          <button @click="closeUpdatesModal" class="btn btn-secondary" style="margin-top: 1rem; width: 100%">
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
import FieldForm from '../components/FieldForm.vue'
import { fieldsAPI, updatesAPI, authAPI } from '../services/api'

export default {
  name: 'AdminDashboard',
  components: {
    NavBar,
    FieldCard,
    FieldForm
  },
  data() {
    return {
      fields: [],
      stats: {},
      loading: true,
      showCreateField: false,
      showUpdates: false,
      selectedField: null,
      updates: [],
      updatesLoading: false,
      showAddAgent: false,
      newAgent: {
        name: '',
        email: '',
        password: ''
      },
      agentLoading: false,
      agentError: '',
      agentSuccess: '',
      isCreatingField: false,
      searchQuery: '',
      showEditField: false,
      editingField: null,
      isUpdatingField: false,
      // Delete Field properties
      showDeleteConfirm: false,
      fieldToDelete: null,
      isDeleting: false
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
    
    clearSearch() {
      this.searchQuery = ''
    },
    
    openAddAgentModal() {
      this.showAddAgent = true
      this.newAgent = {
        name: '',
        email: '',
        password: ''
      }
      this.agentError = ''
      this.agentSuccess = ''
    },
    
    closeAgentModal() {
      this.showAddAgent = false
      this.agentError = ''
      this.agentSuccess = ''
      this.newAgent = {
        name: '',
        email: '',
        password: ''
      }
    },
    
    openCreateFieldModal() {
      this.showCreateField = true
    },
    
    closeCreateFieldModal() {
      this.showCreateField = false
    },
    
    openEditFieldModal(field) {
      this.editingField = { ...field }
      this.showEditField = true
    },
    
    closeEditFieldModal() {
      this.showEditField = false
      this.editingField = null
    },
    
    closeUpdatesModal() {
      this.showUpdates = false
      this.selectedField = null
      this.updates = []
    },
    
    async createField(formData) {
      if (this.isCreatingField) {
        console.log('Already creating field, ignoring duplicate request...')
        return
      }
      
      this.isCreatingField = true
      
      try {
        console.log('Creating field with data:', formData)
        const response = await fieldsAPI.create(formData)
        
        if (response.data.success) {
          console.log('Field created successfully')
          this.closeCreateFieldModal()
          await this.loadData()
        } else {
          alert(response.data.error || 'Failed to create field')
        }
      } catch (error) {
        console.error('Error creating field:', error)
        alert(error.response?.data?.error || 'Failed to create field')
      } finally {
        setTimeout(() => {
          this.isCreatingField = false
        }, 1000)
      }
    },
    
    async updateField(formData) {
      if (this.isUpdatingField) return
      
      this.isUpdatingField = true
      
      try {
        console.log('Updating field with data:', formData)
        const response = await fieldsAPI.update(this.editingField.id, formData)
        
        if (response.data && !response.data.error) {
          console.log('Field updated successfully')
          this.closeEditFieldModal()
          await this.loadData()
          console.log('Field updated successfully!')
        } else if (response.data.message) {
          console.log('Field updated successfully')
          this.closeEditFieldModal()
          await this.loadData()
          alert(response.data.message)
        } else {
          alert(response.data.error || 'Failed to update field')
        }
      } catch (error) {
        console.error('Error updating field:', error)
        if (error.response?.data?.message) {
          alert(error.response.data.message)
          await this.loadData()
          this.closeEditFieldModal()
        } else {
          alert(error.response?.data?.error || 'Failed to update field')
        }
      } finally {
        this.isUpdatingField = false
      }
    },
    

    confirmDeleteField(field) {
      console.log('Delete clicked for field:', field)
      this.fieldToDelete = field
      this.showDeleteConfirm = true
    },
    
    closeDeleteModal() {
      this.showDeleteConfirm = false
      this.fieldToDelete = null
      this.isDeleting = false
    },
    
    async deleteField() {
      if (this.isDeleting) return
      
      this.isDeleting = true
      
      try {
        console.log('Deleting field:', this.fieldToDelete.id)
        const response = await fieldsAPI.delete(this.fieldToDelete.id)
        
        if (response.data.success || response.data.message) {
          console.log('Field deleted successfully')
          this.closeDeleteModal()
          await this.loadData()
          console.log('Field deleted successfully!')
        } else {
          alert(response.data.error || 'Failed to delete field')
        }
      } catch (error) {
        console.error('Error deleting field:', error)
        alert(error.response?.data?.error || 'Failed to delete field')
      } finally {
        this.isDeleting = false
      }
    },
    
    async handleAddAgent() {
      if (this.agentLoading) return
      
      this.agentLoading = true
      this.agentError = ''
      this.agentSuccess = ''
      
      try {
        const agentData = {
          name: this.newAgent.name,
          email: this.newAgent.email,
          password: this.newAgent.password,
          role: 'agent'
        }
        
        const response = await authAPI.register(agentData)
        
        if (response.data.message || response.data.success) {
          this.agentSuccess = `Agent ${this.newAgent.name} created successfully!`
          
          this.newAgent = {
            name: '',
            email: '',
            password: ''
          }
          
          setTimeout(() => {
            this.closeAgentModal()
          }, 2000)
        } else {
          this.agentError = response.data.error || 'Failed to create agent'
        }
      } catch (error) {
        console.error('Error creating agent:', error)
        this.agentError = error.response?.data?.error || 
                         error.response?.data?.message || 
                         'Failed to create agent. Please try again.'
      } finally {
        this.agentLoading = false
      }
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