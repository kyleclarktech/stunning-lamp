<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import OfficeMap from '../components/dashboard/OfficeMap.vue'
import MetricsChart from '../components/dashboard/MetricsChart.vue'
import IncidentBoard from '../components/dashboard/IncidentBoard.vue'
import TeamDistribution from '../components/dashboard/TeamDistribution.vue'
import VisaTimeline from '../components/dashboard/VisaTimeline.vue'
import DashboardOverview from '../components/dashboard/DashboardOverview.vue'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

// Data refs
const overviewData = ref(null)
const officesData = ref([])
const incidentsData = ref([])
const metricsData = ref({})
const teamsData = ref([])
const visasData = ref([])
const isLoading = ref(true)
const lastUpdated = ref(new Date())

// WebSocket connection
const socket = ref(null)

// Fetch all dashboard data
const fetchDashboardData = async () => {
  try {
    const [overview, offices, incidents, metrics, teams, visas] = await Promise.all([
      axios.get(`${API_BASE_URL}/api/dashboard/overview`),
      axios.get(`${API_BASE_URL}/api/dashboard/offices`),
      axios.get(`${API_BASE_URL}/api/dashboard/incidents`),
      axios.get(`${API_BASE_URL}/api/dashboard/metrics`),
      axios.get(`${API_BASE_URL}/api/dashboard/teams`),
      axios.get(`${API_BASE_URL}/api/dashboard/visas`)
    ])

    overviewData.value = overview.data
    officesData.value = offices.data
    incidentsData.value = incidents.data
    metricsData.value = metrics.data
    teamsData.value = teams.data
    visasData.value = visas.data
    lastUpdated.value = new Date()
    isLoading.value = false
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    isLoading.value = false
  }
}

// Setup WebSocket connection for real-time updates
const setupWebSocket = () => {
  try {
    socket.value = new WebSocket(WS_URL)
    
    socket.value.onopen = () => {
      console.log('Dashboard WebSocket connected')
    }
    
    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'dashboard_update') {
          // Handle specific dashboard updates
          const update = data.update
          if (update.type === 'overview') {
            overviewData.value = update.data
          } else if (update.type === 'offices') {
            officesData.value = update.data
          } else if (update.type === 'incidents') {
            incidentsData.value = update.data
          } else if (update.type === 'metrics') {
            metricsData.value = update.data
          } else if (update.type === 'teams') {
            teamsData.value = update.data
          } else if (update.type === 'visas') {
            visasData.value = update.data
          }
          lastUpdated.value = new Date()
        }
      } catch (e) {
        console.error('Error parsing WebSocket message:', e)
      }
    }
    
    socket.value.onclose = () => {
      console.log('Dashboard WebSocket disconnected')
      // Attempt to reconnect after 5 seconds
      setTimeout(setupWebSocket, 5000)
    }
    
    socket.value.onerror = (error) => {
      console.error('Dashboard WebSocket error:', error)
    }
  } catch (error) {
    console.error('Failed to setup WebSocket:', error)
  }
}

// Auto-refresh every 60 seconds
const refreshInterval = ref(null)

onMounted(() => {
  fetchDashboardData()
  setupWebSocket()
  
  // Setup auto-refresh
  refreshInterval.value = setInterval(fetchDashboardData, 60000)
})

onUnmounted(() => {
  if (socket.value) {
    socket.value.close()
  }
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h2>Real-Time Dashboard</h2>
      <div class="dashboard-info">
        <span class="last-updated">Last Updated: {{ lastUpdated.toLocaleTimeString() }}</span>
        <button @click="fetchDashboardData" class="refresh-btn" :disabled="isLoading">
          <span :class="['refresh-icon', { 'rotating': isLoading }]">↻</span>
          Refresh
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <div v-else class="dashboard-grid">
      <!-- Overview Widget (Spans 2 columns) -->
      <div class="widget widget-overview">
        <DashboardOverview :data="overviewData" />
      </div>

      <!-- Office Map Widget (Spans 2 columns, 2 rows) -->
      <div class="widget widget-map">
        <OfficeMap :offices="officesData" />
      </div>

      <!-- Metrics Chart Widget -->
      <div class="widget widget-metrics">
        <MetricsChart :metrics="metricsData" />
      </div>

      <!-- Incident Board Widget -->
      <div class="widget widget-incidents">
        <IncidentBoard :incidents="incidentsData" />
      </div>

      <!-- Team Distribution Widget -->
      <div class="widget widget-teams">
        <TeamDistribution :teams="teamsData" />
      </div>

      <!-- Visa Timeline Widget -->
      <div class="widget widget-visas">
        <VisaTimeline :visas="visasData" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #ffffff;
}

.dashboard-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.last-updated {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 123, 255, 0.2);
  color: #00a8ff;
  border: 1px solid rgba(0, 123, 255, 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(0, 123, 255, 0.3);
  border-color: rgba(0, 123, 255, 0.5);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-icon {
  font-size: 1.2rem;
  display: inline-block;
}

.refresh-icon.rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: rgba(255, 255, 255, 0.7);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #00a8ff;
  border-radius: 50%;
  animation: rotate 1s linear infinite;
  margin-bottom: 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto;
  gap: 1.5rem;
  grid-auto-rows: minmax(300px, auto);
}

.widget {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.widget:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Widget-specific grid placement */
.widget-overview {
  grid-column: span 2;
}

.widget-map {
  grid-column: span 2;
  grid-row: span 2;
}

.widget-metrics {
  grid-column: span 2;
}

.widget-incidents {
  grid-column: span 1;
}

.widget-teams {
  grid-column: span 1;
}

.widget-visas {
  grid-column: span 2;
}

/* Responsive design */
@media (max-width: 1400px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .widget-map {
    grid-column: span 3;
  }
  
  .widget-overview {
    grid-column: span 3;
  }
  
  .widget-metrics {
    grid-column: span 3;
  }
  
  .widget-incidents,
  .widget-teams {
    grid-column: span 1;
  }
  
  .widget-visas {
    grid-column: span 3;
  }
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .widget {
    grid-column: span 2 !important;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .widget {
    grid-column: span 1 !important;
    grid-row: span 1 !important;
  }
}</style>