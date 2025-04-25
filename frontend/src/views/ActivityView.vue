<template>
  <div class="container mt-4">
    <h1 class="mb-4">Activity Details</h1>
    <div v-if="activity" class="card shadow">
      <div class="card-body">
        <h5 class="card-title">{{ activity.curriculum_reference }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">
          Activity ID: {{ activity.activityId }}
        </h6>

        <div class="row mt-3">
          <div class="col-md-6">
            <p><strong>Location:</strong> {{ activity.location }}</p>
            <p><strong>Description:</strong> {{ activity.description }}</p>
            <p><strong>Cost:</strong> ${{ activity.cost.toFixed(2) }}</p>
            <p>
              <strong>Transfer Cost:</strong> ${{
                activity.transfer_cost.toFixed(2)
              }}
            </p>
          </div>
          <div class="col-md-6">
            <p>
              <strong>SGA Approved:</strong>
              <span
                :class="activity.sga_approved ? 'text-success' : 'text-danger'"
              >
                {{ activity.sga_approved ? 'Yes' : 'No' }}
              </span>
            </p>
            <p>
              <strong>Start Date:</strong>
              {{ formatDate(activity.starting_date) }}
            </p>
            <p>
              <strong>End Date:</strong> {{ formatDate(activity.ending_date) }}
            </p>
            <p>
              <strong>State:</strong>
              <span class="badge bg-primary text-white">{{
                activity.state
              }}</span>
            </p>
          </div>
        </div>

        <div class="mt-4">
          <label for="noteInput" class="form-label">Notes:</label>
          <textarea
            id="noteInput"
            v-model="note"
            :disabled="isTeacher"
            class="form-control"
            rows="3"
          ></textarea>
          <small v-if="isTeacher" class="form-text text-muted"
            >Teachers cannot edit notes.</small
          >
        </div>

        <div class="d-flex justify-content-between mt-3">
          <button
            v-if="activity"
            @click="saveNote"
            class="btn btn-primary"
            :disabled="isTeacher || !note.trim()"
          >
            Save Note
          </button>
          <button
            v-if="activity"
            @click="approve"
            class="btn btn-primary"
            :disabled="isTeacher || activity.approved"
          >
            Approve
          </button>
        </div>
      </div>
    </div>
    <div v-else class="alert alert-info" role="alert">
      Loading activity details...
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { apiGetActivities } from '../api/activities';

const route = useRoute();
const authStore = useAuthStore();

const activity = ref(null);
const note = ref('');

const isTeacher = computed(() => authStore.userRole === 'teacher');

const activityId = computed(() => route.params.id);

const formatDate = (date) => {
  const d = new Date(date);
  return d.toLocaleDateString('de-AT', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

const fetchActivity = async () => {
  try {
    const token = authStore.token; // Assuming the token is stored in the auth store
    const response = await apiGetActivity(activityId.value, token);
    activity.value = response.data;
  } catch (error) {
    console.error('Error fetching activity:', error);
  }
};

const saveNote = async () => {
  if (!note.value.trim()) {
    alert('Note cannot be empty.');
    return;
  }
  try {
    const token = authStore.token;
    console.log('Token:', token);
    const newActivity = {
      ...activity.value,
      note: note.value,
    };
    await createNote(newActivity, token);
    console.log('Activity created successfully');
  } catch (error) {
    console.error('Error adding activity:', error.response?.data || error);
  }
  console.log('Saving note:', note.value, activityId.value);
  // Add backend API call here
};

const approve = () => {
  console.log('Approving activity:', activityId.value);
  // Add backend API call here
};

onMounted(() => {
  fetchActivity();
});
</script>

<style scoped>
.card {
  transition: box-shadow 0.3s ease-in-out;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.badge {
  font-size: 0.9em;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
}
</style>
