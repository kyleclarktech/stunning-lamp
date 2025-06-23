<template>
  <div class="graph-explorer">
    <div class="graph-controls">
      <button @click="resetView" class="control-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
          <path d="M3 3v5h5"/>
        </svg>
        Reset View
      </button>
      <button @click="togglePhysics" class="control-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="3"/>
          <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
        </svg>
        {{ physicsEnabled ? 'Disable' : 'Enable' }} Physics
      </button>
      <button @click="fitToScreen" class="control-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
        </svg>
        Fit to Screen
      </button>
      <div class="node-count">
        Nodes: {{ nodeCount }} | Edges: {{ edgeCount }}
      </div>
    </div>
    
    <div ref="networkContainer" class="network-container"></div>
    
    <div v-if="selectedNode" class="node-details">
      <h3>{{ getNodeTitle(selectedNode) }}</h3>
      <div class="details-content">
        <div v-for="(value, key) in getNodeDetails(selectedNode)" :key="key" class="detail-row">
          <span class="detail-key">{{ formatKey(key) }}:</span>
          <span class="detail-value">{{ value }}</span>
        </div>
      </div>
      <button @click="selectedNode = null" class="close-btn">×</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { Network } from 'vis-network'

const props = defineProps({
  queryResults: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['nodeClick', 'edgeClick'])

const networkContainer = ref(null)
const network = ref(null)
const selectedNode = ref(null)
const physicsEnabled = ref(true)
const nodeCount = ref(0)
const edgeCount = ref(0)

// Node type configurations
const nodeStyles = {
  Person: {
    shape: 'dot',
    color: '#4ade80',
    size: 20,
    font: { color: '#fff' }
  },
  Team: {
    shape: 'square',
    color: '#60a5fa',
    size: 25,
    font: { color: '#fff' }
  },
  Policy: {
    shape: 'triangle',
    color: '#f59e0b',
    size: 22,
    font: { color: '#fff' }
  },
  Project: {
    shape: 'diamond',
    color: '#a78bfa',
    size: 24,
    font: { color: '#fff' }
  },
  Group: {
    shape: 'star',
    color: '#ec4899',
    size: 26,
    font: { color: '#fff' }
  },
  Skill: {
    shape: 'hexagon',
    color: '#10b981',
    size: 18,
    font: { color: '#fff' }
  },
  Client: {
    shape: 'ellipse',
    color: '#f97316',
    size: 28,
    font: { color: '#fff' }
  }
}

// Parse query results into nodes and edges
const parseGraphData = (results) => {
  const nodes = new Map()
  const edges = []
  const processedEdges = new Set()

  results.forEach(row => {
    // Extract nodes
    Object.entries(row).forEach(([key, value]) => {
      if (value && typeof value === 'object' && value.labels) {
        const nodeType = value.labels[0]
        const nodeId = value.id || value.name
        
        if (!nodes.has(nodeId)) {
          nodes.set(nodeId, {
            id: nodeId,
            label: value.name || nodeId,
            title: `${nodeType}: ${value.name || nodeId}`,
            ...nodeStyles[nodeType],
            data: value
          })
        }
      }
    })

    // Extract relationships (if query returns them)
    if (row._relationship) {
      const rel = row._relationship
      const edgeId = `${rel.from}-${rel.type}-${rel.to}`
      
      if (!processedEdges.has(edgeId)) {
        edges.push({
          id: edgeId,
          from: rel.from,
          to: rel.to,
          label: rel.type,
          arrows: 'to',
          color: { color: '#6b7280', hover: '#9ca3af' },
          font: { color: '#9ca3af', size: 12 }
        })
        processedEdges.add(edgeId)
      }
    }
  })

  // Infer relationships from data patterns
  results.forEach(row => {
    const rowNodes = Object.values(row).filter(v => v && v.labels)
    
    if (rowNodes.length >= 2) {
      for (let i = 0; i < rowNodes.length - 1; i++) {
        for (let j = i + 1; j < rowNodes.length; j++) {
          const fromId = rowNodes[i].id || rowNodes[i].name
          const toId = rowNodes[j].id || rowNodes[j].name
          const edgeId = `${fromId}-RELATED_TO-${toId}`
          
          if (!processedEdges.has(edgeId) && fromId !== toId) {
            edges.push({
              id: edgeId,
              from: fromId,
              to: toId,
              label: 'RELATED',
              arrows: 'to',
              color: { color: '#374151', hover: '#6b7280' },
              font: { color: '#6b7280', size: 10 },
              dashes: true
            })
            processedEdges.add(edgeId)
          }
        }
      }
    }
  })

  nodeCount.value = nodes.size
  edgeCount.value = edges.length

  return {
    nodes: Array.from(nodes.values()),
    edges: edges
  }
}

// Initialize network
const initNetwork = () => {
  if (!networkContainer.value) return

  const { nodes, edges } = parseGraphData(props.queryResults)

  const data = { nodes, edges }

  const options = {
    physics: {
      enabled: physicsEnabled.value,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -50,
        centralGravity: 0.01,
        springLength: 100,
        springConstant: 0.08
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 200,
      zoomView: true,
      dragView: true
    },
    layout: {
      improvedLayout: true,
      randomSeed: 42
    },
    edges: {
      smooth: {
        type: 'continuous',
        roundness: 0.5
      },
      width: 2,
      hoverWidth: 3
    }
  }

  network.value = new Network(networkContainer.value, data, options)

  // Event handlers
  network.value.on('click', (params) => {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0]
      const nodeData = nodes.find(n => n.id === nodeId)
      selectedNode.value = nodeData?.data
      emit('nodeClick', nodeData)
    } else if (params.edges.length > 0) {
      emit('edgeClick', params.edges[0])
    }
  })

  network.value.on('stabilizationIterationsDone', () => {
    network.value.setOptions({ physics: false })
  })
}

// Control functions
const resetView = () => {
  network.value?.fit()
}

const togglePhysics = () => {
  physicsEnabled.value = !physicsEnabled.value
  network.value?.setOptions({ physics: { enabled: physicsEnabled.value } })
}

const fitToScreen = () => {
  network.value?.fit({ animation: true })
}

// Helper functions
const getNodeTitle = (node) => {
  return node?.name || node?.id || 'Unknown'
}

const getNodeDetails = (node) => {
  const details = {}
  const exclude = ['labels', 'id', 'name']
  
  Object.entries(node || {}).forEach(([key, value]) => {
    if (!exclude.includes(key) && value !== null && value !== undefined) {
      details[key] = value
    }
  })
  
  return details
}

const formatKey = (key) => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Lifecycle
onMounted(() => {
  if (props.queryResults.length > 0) {
    initNetwork()
  }
})

watch(() => props.queryResults, (newResults) => {
  if (newResults.length > 0) {
    network.value?.destroy()
    initNetwork()
  }
}, { deep: true })

onUnmounted(() => {
  network.value?.destroy()
})
</script>

<style scoped>
.graph-explorer {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  overflow: hidden;
}

.graph-controls {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: rgba(31, 41, 55, 0.5);
  border-bottom: 1px solid rgba(75, 85, 99, 0.3);
  align-items: center;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(55, 65, 81, 0.5);
  border: 1px solid rgba(75, 85, 99, 0.3);
  border-radius: 8px;
  color: #e5e7eb;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:hover {
  background: rgba(75, 85, 99, 0.5);
  border-color: rgba(156, 163, 175, 0.3);
}

.control-btn svg {
  stroke-width: 2;
}

.node-count {
  margin-left: auto;
  color: #9ca3af;
  font-size: 14px;
}

.network-container {
  flex: 1;
  width: 100%;
  background: rgba(17, 24, 39, 0.3);
}

.node-details {
  position: absolute;
  top: 80px;
  right: 16px;
  width: 320px;
  max-height: 60%;
  background: rgba(31, 41, 55, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(75, 85, 99, 0.3);
  border-radius: 12px;
  padding: 20px;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.node-details h3 {
  margin: 0 0 16px 0;
  color: #f3f4f6;
  font-size: 18px;
  font-weight: 600;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(55, 65, 81, 0.5);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-key {
  color: #9ca3af;
  font-size: 14px;
  font-weight: 500;
}

.detail-value {
  color: #e5e7eb;
  font-size: 14px;
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  border-color: rgba(239, 68, 68, 0.5);
}

/* Dark theme scrollbar */
.node-details::-webkit-scrollbar {
  width: 8px;
}

.node-details::-webkit-scrollbar-track {
  background: rgba(31, 41, 55, 0.5);
  border-radius: 4px;
}

.node-details::-webkit-scrollbar-thumb {
  background: rgba(75, 85, 99, 0.5);
  border-radius: 4px;
}

.node-details::-webkit-scrollbar-thumb:hover {
  background: rgba(107, 114, 128, 0.5);
}
</style>