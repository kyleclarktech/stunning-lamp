<script setup>
import { computed } from 'vue'

const props = defineProps({
  visas: {
    type: Array,
    default: () => []
  }
})

const sortedVisas = computed(() => {
  return [...props.visas].sort((a, b) => new Date(a.expiry_date) - new Date(b.expiry_date))
})

const groupedVisas = computed(() => {
  const groups = {
    critical: [], // < 30 days
    warning: [],  // 30-60 days
    normal: []    // > 60 days
  }
  
  const now = new Date()
  
  sortedVisas.value.forEach(visa => {
    const expiryDate = new Date(visa.expiry_date)
    const daysUntilExpiry = Math.floor((expiryDate - now) / (1000 * 60 * 60 * 24))
    
    if (daysUntilExpiry < 30) {
      groups.critical.push({ ...visa, daysUntilExpiry })
    } else if (daysUntilExpiry <= 60) {
      groups.warning.push({ ...visa, daysUntilExpiry })
    } else {
      groups.normal.push({ ...visa, daysUntilExpiry })
    }
  })
  
  return groups
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusColor = (daysUntilExpiry) => {
  if (daysUntilExpiry < 30) return '#dc2626'
  if (daysUntilExpiry <= 60) return '#f59e0b'
  return '#22c55e'
}

const getStatusText = (daysUntilExpiry) => {
  if (daysUntilExpiry < 0) return 'Expired'
  if (daysUntilExpiry === 0) return 'Expires today'
  if (daysUntilExpiry === 1) return '1 day'
  return `${daysUntilExpiry} days`
}
</script>

<template>
  <div class="visa-timeline-widget">
    <h3>Visa Expiry Timeline</h3>
    
    <div class="visa-stats">
      <div class="stat-card critical">
        <span class="stat-number">{{ groupedVisas.critical.length }}</span>
        <span class="stat-label">Critical (&lt; 30 days)</span>
      </div>
      <div class="stat-card warning">
        <span class="stat-number">{{ groupedVisas.warning.length }}</span>
        <span class="stat-label">Warning (30-60 days)</span>
      </div>
      <div class="stat-card normal">
        <span class="stat-number">{{ groupedVisas.normal.length }}</span>
        <span class="stat-label">Normal (&gt; 60 days)</span>
      </div>
    </div>
    
    <div class="visa-list">
      <div class="visa-group" v-if="groupedVisas.critical.length > 0">
        <h4 class="group-header critical">Critical - Action Required</h4>
        <div v-for="visa in groupedVisas.critical" :key="visa.id" class="visa-item">
          <div class="visa-info">
            <div class="employee-info">
              <span class="employee-name">{{ visa.employee_name }}</span>
              <span class="visa-type">{{ visa.visa_type }}</span>
            </div>
            <div class="expiry-info">
              <span class="expiry-date">{{ formatDate(visa.expiry_date) }}</span>
              <span class="days-remaining" :style="{ color: getStatusColor(visa.daysUntilExpiry) }">
                {{ getStatusText(visa.daysUntilExpiry) }}
              </span>
            </div>
          </div>
          <div class="visa-progress">
            <div class="progress-bar" :style="{ 
              width: `${Math.max(0, Math.min(100, (30 - visa.daysUntilExpiry) / 30 * 100))}%`,
              backgroundColor: getStatusColor(visa.daysUntilExpiry)
            }"></div>
          </div>
        </div>
      </div>
      
      <div class="visa-group" v-if="groupedVisas.warning.length > 0">
        <h4 class="group-header warning">Warning - Monitor Closely</h4>
        <div v-for="visa in groupedVisas.warning.slice(0, 5)" :key="visa.id" class="visa-item">
          <div class="visa-info">
            <div class="employee-info">
              <span class="employee-name">{{ visa.employee_name }}</span>
              <span class="visa-type">{{ visa.visa_type }}</span>
            </div>
            <div class="expiry-info">
              <span class="expiry-date">{{ formatDate(visa.expiry_date) }}</span>
              <span class="days-remaining" :style="{ color: getStatusColor(visa.daysUntilExpiry) }">
                {{ getStatusText(visa.daysUntilExpiry) }}
              </span>
            </div>
          </div>
        </div>
        <div v-if="groupedVisas.warning.length > 5" class="more-items">
          +{{ groupedVisas.warning.length - 5 }} more
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.visa-timeline-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.visa-timeline-widget h3 {
  margin: 0 0 1rem 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.visa-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-card.critical {
  border-color: rgba(220, 38, 38, 0.3);
  background: rgba(220, 38, 38, 0.1);
}

.stat-card.warning {
  border-color: rgba(245, 158, 11, 0.3);
  background: rgba(245, 158, 11, 0.1);
}

.stat-card.normal {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.1);
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-card.critical .stat-number {
  color: #dc2626;
}

.stat-card.warning .stat-number {
  color: #f59e0b;
}

.stat-card.normal .stat-number {
  color: #22c55e;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
}

.visa-list {
  flex: 1;
  overflow-y: auto;
}

.visa-group {
  margin-bottom: 1.5rem;
}

.group-header {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.group-header.critical {
  color: #dc2626;
}

.group-header.warning {
  color: #f59e0b;
}

.visa-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  transition: all 0.2s ease;
}

.visa-item:hover {
  background: rgba(0, 0, 0, 0.3);
}

.visa-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.employee-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.employee-name {
  font-weight: 500;
  color: #ffffff;
}

.visa-type {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.expiry-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.125rem;
}

.expiry-date {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
}

.days-remaining {
  font-size: 0.75rem;
  font-weight: 600;
}

.visa-progress {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition: width 0.5s ease;
}

.more-items {
  text-align: center;
  color: #00a8ff;
  font-size: 0.875rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.more-items:hover {
  color: #3b9fff;
}
</style>