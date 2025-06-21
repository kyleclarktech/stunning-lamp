<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => null
  }
})

const stats = computed(() => {
  if (!props.data) {
    return [
      { label: 'Total Employees', value: 0, icon: '👥', color: '#00a8ff' },
      { label: 'Active Incidents', value: 0, icon: '🚨', color: '#dc2626' },
      { label: 'Queries Today', value: 0, icon: '🔍', color: '#22c55e' },
      { label: 'System Health', value: '0%', icon: '💚', color: '#22c55e' }
    ]
  }
  
  return [
    { label: 'Total Employees', value: props.data.total_employees || 0, icon: '👥', color: '#00a8ff' },
    { label: 'Active Incidents', value: props.data.active_incidents || 0, icon: '🚨', color: '#dc2626' },
    { label: 'Queries Today', value: props.data.queries_today || 0, icon: '🔍', color: '#3b82f6' },
    { label: 'System Health', value: `${props.data.system_health || 0}%`, icon: '💚', color: '#22c55e' }
  ]
})

const recentActivity = computed(() => {
  return props.data?.recent_activity || []
})

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="dashboard-overview-widget">
    <h3>Overview</h3>
    
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-box">
        <div class="stat-icon" :style="{ color: stat.color }">{{ stat.icon }}</div>
        <div class="stat-content">
          <div class="stat-value" :style="{ color: stat.color }">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>
    
    <div class="activity-section" v-if="recentActivity.length > 0">
      <h4>Recent Activity</h4>
      <div class="activity-list">
        <div v-for="(activity, index) in recentActivity.slice(0, 5)" :key="index" class="activity-item">
          <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
          <span class="activity-type">{{ activity.type }}</span>
          <span class="activity-description">{{ activity.description }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-overview-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.dashboard-overview-widget h3 {
  margin: 0 0 1rem 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-box {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-box:hover {
  background: rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  white-space: nowrap;
}

.activity-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-section h4 {
  margin: 0 0 0.75rem 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  font-weight: 600;
}

.activity-list {
  flex: 1;
  overflow-y: auto;
}

.activity-item {
  display: grid;
  grid-template-columns: auto auto 1fr;
  gap: 0.75rem;
  align-items: center;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  transition: background 0.2s ease;
}

.activity-item:hover {
  background: rgba(0, 0, 0, 0.2);
}

.activity-time {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.75rem;
  font-family: monospace;
}

.activity-type {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 3px;
  font-size: 0.75rem;
  color: #00a8ff;
  font-weight: 500;
  white-space: nowrap;
}

.activity-description {
  color: rgba(255, 255, 255, 0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }
  
  .activity-time,
  .activity-type {
    display: inline-block;
    margin-right: 0.5rem;
  }
}
</style>