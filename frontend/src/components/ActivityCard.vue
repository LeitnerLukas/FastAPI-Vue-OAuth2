<template>
  <div class="card mb-4 shadow-sm">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <div>
          <h5 class="card-title">
            {{ entity.activity_id }} - {{ entity.curriculum_reference }}
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">
            State: {{ entity.state }}
          </h6>
        </div>
        <span
          :class="[
            'badge',
            entity.sga_approved
              ? 'bg-success text-white'
              : 'bg-danger text-white',
          ]"
        >
          {{ entity.sga_approved ? 'SGA Approved' : 'Not SGA Approved' }}
        </span>
      </div>

      <div class="row mb-3">
        <div class="col-md-6">
          <p class="mb-1"><strong>Location:</strong> {{ entity.location }}</p>
          <p class="mb-1">
            <strong>Cost:</strong> ${{ entity.cost.toFixed(2) }}
          </p>
          <p class="mb-1">
            <strong>Transfer Cost:</strong> ${{
              entity.transfer_cost.toFixed(2)
            }}
          </p>
        </div>
        <div class="col-md-6">
          <p class="mb-1">
            <strong>Start Date:</strong> {{ formatDate(entity.starting_date) }}
          </p>
          <p class="mb-1">
            <strong>End Date:</strong> {{ formatDate(entity.ending_date) }}
          </p>
        </div>
      </div>

      <p class="card-text mb-3">
        <strong>Description:</strong> {{ entity.description }}
      </p>

      <router-link
        :to="'/activity/' + entity.activity_id"
        class="btn btn-primary"
      >
        View Details
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  entity: {
    type: Object,
    required: true,
  },
});

const formatDate = (date) => {
  const d = new Date(date);
  return d.toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};
</script>

<style scoped>
.card {
  transition: box-shadow 0.3s ease-in-out;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
