<template>
  <div class="container w-100 mt-5">
    <h5>Users:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Email</th>
            <th scope="col">Name</th>
            <th scope="col">Role</th>
            <th scope="col">Change Role</th>
            <th scope="col">Remove</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, idx) in users" :key="idx">
            <th scope="row">{{ idx + 1 }}</th>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.role.name }}</td>
            <td>
              <select
                id="roleSelect"
                class="form-select"
                @change="updateRole(user.id, $event.target.value)"
              >
                <option v-for="role in roles" :key="role.name" :value="role.id">
                  {{ role.name }}
                </option>
              </select>
            </td>
            <td>
              <button class="btn btn-danger" @click="removeUser(user.id)">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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
            <td>{{ item.classId }}</td>
            <td>{{ item.girls }}</td>
            <td>{{ item.boys }}</td>
            <td>
              <button class="btn btn-danger" @click="removeClass(item.classId)">
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
import { createClass, deleteClass, getClasses } from "../api/class";
import { deleteUser, updateUserRole } from "../api/superuser";
import { getRoles, getUsers } from "../api/user";

const classData = ref({
  id: "",
  girls: 0,
  boys: 0,
});

const roles = ref([]);
const classes = ref([]);
const users = ref([]);

const fetchRoles = async () => {
  roles.value = JSON.parse(await getRoles());
};

const fetchClasses = async () => {
  classes.value = JSON.parse(await getClasses());
};

const fetchUsers = async () => {
  users.value = JSON.parse(await getUsers());
};

const submitClass = async (newClass) => {
  createClass(classData.value);
};

const removeClass = async (classId) => {
  deleteClass(classId);
};

const removeUser = async (userId) => {
  deleteUser(userId);
};

const updateRole = async (userId, role) => {
  updateUserRole(userId, role);
};

onMounted(() => {
  fetchRoles();
  fetchClasses();
  fetchUsers();
});
</script>
