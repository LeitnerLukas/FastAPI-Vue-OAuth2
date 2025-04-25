<!-- src/views/DashboardView.vue -->
<template>
  <div class="container">
    <div class="dashboard">
      <div class="header d-flex justify-content-between align-items-center">
        <h3>Dashboard</h3>
        <router-link :to="'/activity/new'" class="btn btn-primary">
          New Activity
        </router-link>
      </div>
      <div class="entity-list mt-3">
        <EntityDisplay
          v-for="(entity, index) in entities"
          :key="index"
          :entity="entity"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EntityDisplay from '../components/ActivityCard.vue';
import { apiGetActivities } from '../api/activities.js';
import { useAuthStore } from '../store/auth';


export default {
  components: {
    EntityDisplay,
  },
  data() {
    return {
      entities: [], // Initially empty, will be populated dynamically
    };
  },
  mounted() {
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      try {
        const auth = useAuthStore();
        const response = await apiGetActivities(auth.access_token);
        this.entities = response.data; // Assuming the API returns an array of activities
      } catch (error) {
        console.error('Error fetching activities:', error);
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  margin-top: 20px;
}

.entity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
</style>
