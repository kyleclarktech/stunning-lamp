<script setup>
import { computed } from 'vue'

const props = defineProps({
  incidents: {
    type: Array,
    default: () => []
  }
})

const severityColors = {
  critical: '#dc2626',
  high: '#f59e0b',
  medium: '#3b82f6',
  low: '#22c55e'
}

const severityIcons = {
  critical: '🚨',
  high: '⚠️',
  medium: 'ℹ️',
  low: '✓'
}

const groupedIncidents = computed(() => {
  const groups = {
    critical: [],
    high: [],
    medium: [],
    low: []
  }
  
  props.incidents.forEach(incident => {
    if (groups[incident.severity]) {
      groups[incident.severity].push(incident)
    }
  })
  
  return groups
})

const totalIncidents = computed(() => props.incidents.length)

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // Less than 1 minute
    return 'Just now'
  } else if (diff < 3600000) { // Less than 1 hour
    const minutes = Math.floor(diff / 60000)
    return `${minutes}m ago`
  } else if (diff < 86400000) { // Less than 1 day
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  } else {
    const days = Math.floor(diff / 86400000)
    return `${days}d ago`
  }
}
</script>

<template>
  <div class="incident-board-widget">
    <div class="widget-header">
      <h3>Active Incidents</h3>
      <span class="incident-count">{{ totalIncidents }}</span>
    </div>
    
    <div class="incident-sections">
      <div v-for="(severity, index) in ['critical', 'high', 'medium', 'low']" 
           :key="severity"
           class="severity-section">
        <div class="severity-header" :style="{ borderColor: severityColors[severity] }">
          <span class="severity-icon">{{ severityIcons[severity] }}</span>
          <span class="severity-label">{{ severity.toUpperCase() }}</span>
          <span class="severity-count">{{ groupedIncidents[severity].length }}</span>
        </div>
        
        <div class="incidents-list">
          <div v-if="groupedIncidents[severity].length === 0" class="no-incidents">
            No {{ severity }} incidents
          </div>
          <div v-else
               v-for="incident in groupedIncidents[severity].slice(0, 3)" 
               :key="incident.id"
               class="incident-item">
            <div class="incident-title">{{ incident.title }}</div>
            <div class="incident-meta">
              <span class="incident-location">{{ incident.location }}</span>
              <span class="incident-time">{{ formatTime(incident.created_at) }}</span>
            </div>
          </div>
          <div v-if="groupedIncidents[severity].length > 3" class="more-incidents">
            +{{ groupedIncidents[severity].length - 3 }} more
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.incident-board-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.widget-header h3 {
  margin: 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.incident-count {
  background: rgba(255, 255, 255, 0.1);
  color: #00a8ff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
}

.incident-sections {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
}

.severity-section {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.severity-header {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-left: 4px solid;
  gap: 0.5rem;
}

.severity-icon {
  font-size: 1rem;
}

.severity-label {
  flex: 1;
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.9);
}

.severity-count {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
}

.incidents-list {
  padding: 0.5rem;
}

.no-incidents {
  text-align: center;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.875rem;
  padding: 0.5rem;
  font-style: italic;
}

.incident-item {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
  margin-bottom: 0.25rem;
  transition: background 0.2s ease;
}

.incident-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.incident-title {
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.incident-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.incident-location {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 0.5rem;
}

.incident-time {
  white-space: nowrap;
}

.more-incidents {
  text-align: center;
  color: #00a8ff;
  font-size: 0.75rem;
  padding: 0.25rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.more-incidents:hover {
  color: #3b9fff;
}
</style>