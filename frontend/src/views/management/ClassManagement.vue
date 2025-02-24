<template>
  <div class="container mt-4">
    <router-link to="/user_manage">&lt; Back</router-link>
    <h5 class="mt-3">Create Class:</h5>
    <form @submit.prevent="submitClass(classData)">
      <div class="mb-3">
        <label for="classname" class="form-label">ID (Classname)</label>
        <input
          type="text"
          class="form-control"
          id="classname"
          v-model="classData.id"
          placeholder="e.g., 5ahit"
          required
        />
      </div>
      <div class="mb-3">
        <label for="girls" class="form-label">Number of Girls</label>
        <input
          type="number"
          class="form-control"
          id="girls"
          v-model.number="classData.girls"
          min="0"
          placeholder="Enter number of girls"
          required
        />
      </div>
      <div class="mb-3">
        <label for="boys" class="form-label">Number of Boys</label>
        <input
          type="number"
          class="form-control"
          id="boys"
          v-model.number="classData.boys"
          min="0"
          placeholder="Enter number of boys"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <h5 class="mt-5 mb-2">Classes:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">id</th>
            <th scope="col">Girls</th>
            <th scope="col">Boys</th>
            <th scope="col">Remove</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in classes" :key="idx">
            <th scope="row">{{ idx + 1 }}</th>
            <td>{{ item.class_id }}</td>
            <td>
              <input
                class="form-control"
                type="number"
                v-model="item.girl_count"
                @input="
                  updateClassData(
                    item.class_id,
                    item.girl_count,
                    item.boy_count
                  )
                "
              />
            </td>
            <td>
              <input
                class="form-control"
                type="number"
                v-model="item.boy_count"
                @input="
                  updateClassData(
                    item.class_id,
                    item.girl_count,
                    item.boy_count
                  )
                "
              />
            </td>
            <td>
              <button
                class="btn btn-danger"
                @click="removeClass(item.class_id)"
              >
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import {
  createClass,
  deleteClass,
  getClasses,
  updateClass,
} from "../../api/class";
import { useDialogStore } from "../../store/dialog";

const classData = ref({
  id: "",
  girls: 0,
  boys: 0,
});

const classes = ref([]);

const dialogStore = useDialogStore();

const fetchClasses = async () => {
  const fetchedClass = await getClasses();
  classes.value = fetchedClass.data;
};

const submitClass = async (newClass) => {
  try {
    await createClass({
      class_id: newClass.id,
      girl_count: newClass.girls,
      boy_count: newClass.boys,
    });
    classes.value.push({
      class_id: newClass.id,
      girl_count: newClass.girls,
      boy_count: newClass.boys,
    });
  } catch (error) {
    dialogStore.setError({
      title: "Error creating class",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const removeClass = async (classId) => {
  try {
    await deleteClass(classId);
    classes.value = classes.value.filter(
      (schoolClass) => schoolClass.class_id !== classId
    );
  } catch (error) {
    dialogStore.setError({
      title: "Error removing class",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const updateClassData = async (classId, girls, boys) => {
  try {
    if (
      girls !== null &&
      girls !== undefined &&
      boys !== null &&
      boys !== undefined
    ) {
      await updateClass(classId, {
        girl_count: parseInt(girls),
        boy_count: parseInt(boys),
      });
    }
  } catch (error) {
    dialogStore.setError({
      title: "Error updating class",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

onMounted(() => {
  fetchClasses();
});
</script>
