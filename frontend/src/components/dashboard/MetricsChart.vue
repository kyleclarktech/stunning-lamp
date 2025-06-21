<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  metrics: {
    type: Object,
    default: () => ({})
  }
})

const chartCanvas = ref(null)
const chart = ref(null)
const selectedMetric = ref('user_activity')

const metricOptions = [
  { value: 'user_activity', label: 'User Activity' },
  { value: 'api_calls', label: 'API Calls' },
  { value: 'query_performance', label: 'Query Performance' },
  { value: 'error_rate', label: 'Error Rate' }
]

const currentMetricData = computed(() => {
  return props.metrics[selectedMetric.value] || []
})

const createChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  
  // Destroy existing chart if it exists
  if (chart.value) {
    chart.value.destroy()
  }

  const labels = currentMetricData.value.map(item => {
    const date = new Date(item.timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  })

  const data = currentMetricData.value.map(item => item.value)

  chart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: metricOptions.find(opt => opt.value === selectedMetric.value)?.label || 'Metric',
        data: data,
        borderColor: '#00a8ff',
        backgroundColor: 'rgba(0, 168, 255, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#00a8ff',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: function(context) {
              const label = context.dataset.label || ''
              const value = context.parsed.y
              return `${label}: ${value.toFixed(2)}`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: 'rgba(255, 255, 255, 0.7)',
            font: {
              size: 11
            },
            maxRotation: 45,
            minRotation: 45
          }
        },
        y: {
          grid: {
            color: 'rgba(255, 255, 255, 0.05)',
            drawBorder: false
          },
          ticks: {
            color: 'rgba(255, 255, 255, 0.7)',
            font: {
              size: 11
            }
          },
          beginAtZero: true
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  })
}

const updateChart = () => {
  if (!chart.value) {
    createChart()
    return
  }

  const labels = currentMetricData.value.map(item => {
    const date = new Date(item.timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  })

  const data = currentMetricData.value.map(item => item.value)

  chart.value.data.labels = labels
  chart.value.data.datasets[0].data = data
  chart.value.data.datasets[0].label = metricOptions.find(opt => opt.value === selectedMetric.value)?.label || 'Metric'
  chart.value.update('none')
}

// Watch for metric selection changes
watch(selectedMetric, () => {
  updateChart()
})

// Watch for data changes
watch(() => props.metrics, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  createChart()
})
</script>

<template>
  <div class="metrics-chart-widget">
    <div class="chart-header">
      <h3>Performance Metrics</h3>
      <select v-model="selectedMetric" class="metric-selector">
        <option v-for="option in metricOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="chart-stats">
      <div class="stat-item" v-if="currentMetricData.length > 0">
        <span class="stat-label">Current</span>
        <span class="stat-value">{{ currentMetricData[currentMetricData.length - 1]?.value.toFixed(2) || '0' }}</span>
      </div>
      <div class="stat-item" v-if="currentMetricData.length > 0">
        <span class="stat-label">Average</span>
        <span class="stat-value">{{ (currentMetricData.reduce((sum, item) => sum + item.value, 0) / currentMetricData.length).toFixed(2) }}</span>
      </div>
      <div class="stat-item" v-if="currentMetricData.length > 0">
        <span class="stat-label">Peak</span>
        <span class="stat-value">{{ Math.max(...currentMetricData.map(item => item.value)).toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.metrics-chart-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.metric-selector {
  padding: 0.25rem 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.875rem;
  cursor: pointer;
  outline: none;
  transition: all 0.3s ease;
}

.metric-selector:hover,
.metric-selector:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.metric-selector option {
  background: #1a1a1a;
  color: #ffffff;
}

.chart-container {
  flex: 1;
  position: relative;
  min-height: 200px;
}

.chart-stats {
  display: flex;
  justify-content: space-around;
  padding: 1rem 0 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #00a8ff;
}
</style>