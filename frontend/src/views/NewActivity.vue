<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title mb-4">Add New Activity</h2>
            <form @submit.prevent="addActivity">
              <div class="mb-3">
                <label for="location" class="form-label">Location</label>
                <input
                  v-model="activity.location"
                  type="text"
                  class="form-control"
                  id="location"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="curriculum_reference" class="form-label"
                  >Curriculum Reference</label
                >
                <input
                  v-model="activity.curriculum_reference"
                  type="text"
                  class="form-control"
                  id="curriculum_reference"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea
                  v-model="activity.description"
                  class="form-control"
                  id="description"
                  required
                ></textarea>
              </div>

              <div class="mb-3">
                <label for="cost" class="form-label">Cost</label>
                <input
                  v-model.number="activity.cost"
                  type="number"
                  step="0.01"
                  class="form-control"
                  id="cost"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="transfer_cost" class="form-label"
                  >Transfer Cost</label
                >
                <input
                  v-model.number="activity.transfer_cost"
                  type="number"
                  step="0.01"
                  class="form-control"
                  id="transfer_cost"
                  required
                />
              </div>

              <div class="mb-3 form-check">
                <input
                  v-model="activity.sga_approved"
                  type="checkbox"
                  class="form-check-input"
                  id="sga_approved"
                />
                <label class="form-check-label" for="sga_approved"
                  >SGA Approved</label
                >
              </div>

              <div class="mb-3">
                <label for="starting_date" class="form-label"
                  >Starting Date</label
                >
                <input
                  v-model="activity.starting_date"
                  type="datetime-local"
                  class="form-control"
                  id="starting_date"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="ending_date" class="form-label">Ending Date</label>
                <input
                  v-model="activity.ending_date"
                  type="datetime-local"
                  class="form-control"
                  id="ending_date"
                  required
                />
              </div>

              <button type="submit" class="btn btn-primary">
                Add Activity
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createActivity } from "../api/activities";

const router = useRouter();

const activity = ref({
  location: "",
  description: "",
  curriculum_reference: "",
  cost: 0,
  transfer_cost: 0,
  sga_approved: false,
  starting_date: "",
  ending_date: "",
});

const addActivity = async () => {
  if (activity.value.starting_date >= activity.value.ending_date) {
    alert("Starting date must be before the ending date.");
    return;
  }

  console.log("Activity added:", activity.value);

  try {
    await createActivity({
      location: activity.value.location,
      description: activity.value.description,
      curriculum_reference: activity.value.curriculum_reference,
      cost: activity.value.cost,
      transfer_cost: activity.value.transfer_cost,
      sga_approved: activity.value.sga_approved,
      starting_date: activity.value.starting_date,
      ending_date: activity.value.ending_date,
    });
    // Reset the form
    const newActivity = {
      location: "",
      description: "",
      curriculum_reference: "",
      cost: 0,
      transfer_cost: 0,
      sga_approved: false,
      starting_date: "",
      ending_date: "",
    };
    Object.assign(activity.value, newActivity);
    router.push({ name: "Activities" });
  } catch (error) {
    console.error("Error adding activity:", error);
  }
};
</script>
