<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  offices: {
    type: Array,
    default: () => []
  }
})

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])

// Fix Leaflet's default icon path issue
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
})

const initializeMap = () => {
  if (!mapContainer.value) return

  // Initialize the map
  map.value = L.map(mapContainer.value).setView([20, 0], 2)

  // Add dark theme tile layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    maxZoom: 19
  }).addTo(map.value)

  // Add initial markers
  updateMarkers()
}

const updateMarkers = () => {
  if (!map.value) return

  // Clear existing markers
  markers.value.forEach(marker => marker.remove())
  markers.value = []

  // Add new markers
  props.offices.forEach(office => {
    const marker = L.marker([office.lat, office.lon])
      .addTo(map.value)
      .bindPopup(`
        <div style="min-width: 200px;">
          <h3 style="margin: 0 0 8px 0;">${office.name}</h3>
          <p style="margin: 4px 0;"><strong>Status:</strong> <span style="color: ${office.status === 'active' ? '#22c55e' : '#ef4444'};">${office.status}</span></p>
          <p style="margin: 4px 0;"><strong>Employees:</strong> ${office.employee_count}</p>
          <p style="margin: 4px 0;"><strong>Incidents:</strong> ${office.active_incidents}</p>
          <p style="margin: 4px 0;"><strong>Time Zone:</strong> ${office.timezone}</p>
        </div>
      `)
    
    // Color code markers based on status
    const icon = L.divIcon({
      className: 'custom-marker',
      html: `<div class="marker-pin ${office.status}" data-incidents="${office.active_incidents}">
        <span class="marker-number">${office.employee_count}</span>
      </div>`,
      iconSize: [40, 40],
      iconAnchor: [20, 40]
    })
    
    marker.setIcon(icon)
    markers.value.push(marker)
  })

  // Fit map to show all markers if we have offices
  if (props.offices.length > 0) {
    const group = L.featureGroup(markers.value)
    map.value.fitBounds(group.getBounds().pad(0.1))
  }
}

// Watch for changes in offices data
watch(() => props.offices, () => {
  updateMarkers()
}, { deep: true })

onMounted(() => {
  initializeMap()
})
</script>

<template>
  <div class="office-map-widget">
    <h3>Global Office Locations</h3>
    <div ref="mapContainer" class="map-container"></div>
    <div class="map-legend">
      <div class="legend-item">
        <span class="legend-color active"></span>
        <span>Active</span>
      </div>
      <div class="legend-item">
        <span class="legend-color inactive"></span>
        <span>Inactive</span>
      </div>
      <div class="legend-item">
        <span class="legend-icon">📍</span>
        <span>Has Incidents</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.office-map-widget {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.office-map-widget h3 {
  margin: 0 0 1rem 0;
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
}

.map-container {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
  min-height: 400px;
}

.map-legend {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  font-size: 0.875rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-color.active {
  background: #22c55e;
}

.legend-color.inactive {
  background: #ef4444;
}

.legend-icon {
  font-size: 1rem;
}
</style>

<style>
/* Global styles for custom markers */
.custom-marker {
  background: transparent;
  border: 0;
}

.marker-pin {
  width: 40px;
  height: 40px;
  border-radius: 50% 50% 50% 0;
  position: relative;
  transform: rotate(-45deg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.marker-pin.active {
  background: #22c55e;
  border: 2px solid #16a34a;
}

.marker-pin.inactive {
  background: #ef4444;
  border: 2px solid #dc2626;
}

.marker-pin[data-incidents]:not([data-incidents="0"])::after {
  content: "⚠";
  position: absolute;
  top: -8px;
  right: -8px;
  background: #f59e0b;
  color: #000;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transform: rotate(45deg);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.marker-number {
  transform: rotate(45deg);
  font-weight: bold;
  color: white;
  font-size: 14px;
}

/* Leaflet popup styling for dark theme */
.leaflet-popup-content-wrapper {
  background: rgba(30, 30, 30, 0.95);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.leaflet-popup-tip {
  background: rgba(30, 30, 30, 0.95);
}

.leaflet-popup-content {
  margin: 12px;
}

.leaflet-popup-content h3 {
  color: #00a8ff;
}
</style>