<!-- src/views/DashboardView.vue -->
<template>
  <div class="dashboard">
    <div class="header">
      <h1>Dashboard</h1>
      <router-link :to="'/apiactivity/new'" class="btn btn-primary">
        New Activity
      </router-link>
    </div>
    <div class="entity-list">
      <EntityDisplay
        v-for="(entity, index) in entities"
        :key="index"
        :entity="entity"
      />
    </div>
  </div>
</template>

<script>
import EntityDisplay from '../components/ActivityCard.vue';

export default {
  components: {
    EntityDisplay,
  },
  data() {
    return {
      // Example array of entities based on the provided structure
      entities: [
        {
          activityId: 1,
          location: 'New York',
          curriculum_reference: 'CURR001',
          description: 'Activity Description 1',
          cost: 100.0,
          transfer_cost: 20.5,
          sga_approved: true,
          starting_date: '2025-02-01T00:00:00Z',
          ending_date: '2025-02-10T00:00:00Z',
          state: 'Active',
        },
        {
          activityId: 2,
          location: 'Los Angeles',
          curriculum_reference: 'CURR002',
          description: 'Activity Description 2',
          cost: 150.0,
          transfer_cost: 30.0,
          sga_approved: false,
          starting_date: '2025-03-05T00:00:00Z',
          ending_date: '2025-03-15T00:00:00Z',
          state: 'Pending',
        },
        // Add more entities as needed
      ],
    };
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.entity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
</style>
