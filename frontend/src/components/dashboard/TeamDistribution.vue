<script setup>
import { computed } from 'vue'

const props = defineProps({
  teams: {
    type: Array,
    default: () => []
  }
})

const totalMembers = computed(() => {
  return props.teams.reduce((sum, team) => sum + team.member_count, 0)
})

const sortedTeams = computed(() => {
  return [...props.teams].sort((a, b) => b.member_count - a.member_count)
})

const getTeamIcon = (teamName) => {
  const icons = {
    'Engineering': '⚙️',
    'Sales': '💼',
    'Marketing': '📢',
    'HR': '👥',
    'Finance': '💰',
    'Operations': '📊',
    'Support': '🎧',
    'Legal': '⚖️'
  }
  return icons[teamName] || '👥'
}

const getBarWidth = (memberCount) => {
  const maxCount = Math.max(...props.teams.map(t => t.member_count), 1)
  return `${(memberCount / maxCount) * 100}%`
}
</script>

<template>
  <div class="team-distribution-widget">
    <div class="widget-header">
      <h3>Team Distribution</h3>
      <span class="total-members">{{ totalMembers }} total</span>
    </div>
    
    <div class="teams-list">
      <div v-for="team in sortedTeams" :key="team.name" class="team-item">
        <div class="team-info">
          <span class="team-icon">{{ getTeamIcon(team.name) }}</span>
          <span class="team-name">{{ team.name }}</span>
          <span class="team-count">{{ team.member_count }}</span>
        </div>
        <div class="team-bar-container">
          <div class="team-bar" :style="{ width: getBarWidth(team.member_count) }"></div>
        </div>
        <div class="team-details">
          <span class="team-location">{{ team.primary_location }}</span>
          <span class="team-lead" v-if="team.lead">Lead: {{ team.lead }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.team-distribution-widget {
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

.total-members {
  background: rgba(255, 255, 255, 0.1);
  color: #00a8ff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
}

.teams-list {
  flex: 1;
  overflow-y: auto;
}

.team-item {
  margin-bottom: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.team-item:hover {
  background: rgba(0, 0, 0, 0.3);
  transform: translateX(4px);
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.team-icon {
  font-size: 1.25rem;
}

.team-name {
  flex: 1;
  font-weight: 500;
  color: #ffffff;
}

.team-count {
  font-weight: 600;
  color: #00a8ff;
  font-size: 1.125rem;
}

.team-bar-container {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.team-bar {
  height: 100%;
  background: linear-gradient(90deg, #00a8ff, #0056b3);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.team-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.team-location {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.team-lead {
  font-style: italic;
}
</style>