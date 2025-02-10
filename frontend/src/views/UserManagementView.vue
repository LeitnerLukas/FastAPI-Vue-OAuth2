<template>
  <div class="container mt-4">
    <h5>Create New Role</h5>
    <form @submit.prevent="submitRole">
      <div class="mb-3">
        <label for="name" class="form-label">Role Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="roleData.name"
          required
        />
      </div>

      <div class="form-check mb-2">
        <input
          type="checkbox"
          class="form-check-input"
          id="approvement_permission"
          v-model="roleData.approvement_permission"
        />
        <label class="form-check-label" for="approvement_permission">
          Approvement Permission
        </label>
      </div>

      <div class="form-check mb-2">
        <input
          type="checkbox"
          class="form-check-input"
          id="super_approvement_permission"
          v-model="roleData.super_approvement_permission"
        />
        <label class="form-check-label" for="super_approvement_permission">
          Super Approvement Permission
        </label>
      </div>

      <div class="form-check mb-2">
        <input
          type="checkbox"
          class="form-check-input"
          id="request_permission"
          v-model="roleData.request_permission"
        />
        <label class="form-check-label" for="request_permission">
          Request Permission
        </label>
      </div>

      <div class="form-check mb-3">
        <input
          type="checkbox"
          class="form-check-input"
          id="change_permission"
          v-model="roleData.change_permission"
        />
        <label class="form-check-label" for="change_permission">
          Change Permission
        </label>
      </div>

      <button type="submit" class="btn btn-primary">Create Role</button>
    </form>
  </div>
  <div class="container w-100 mt-5">
    <h5>Roles:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Approvement</th>
            <th scope="col">Super-Approvement</th>
            <th scope="col">Reuquest Permission</th>
            <th scope="col">Change Permission</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(role, idx) in roles" :key="idx">
            <th scope="row">{{ role.id }}</th>
            <td>{{ role.name }}</td>
            <td>{{ role.approvement_permission }}</td>
            <td>
              {{ role.super_approvement_permission }}
            </td>
            <td>
              {{ role.request_permission }}
            </td>
            <td>
              {{ role.request_permission }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="container w-100 mt-5">
    <h5>Users:</h5>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Email</th>
            <th scope="col">Name</th>
            <th scope="col">Roles</th>
            <th scope="col">Add Role</th>
            <th scope="col">Remove</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, idx) in users" :key="idx">
            <th scope="row">{{ idx + 1 }}</th>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td>
              <div
                @click="removeUserRole(user.id, role.id)"
                v-for="role in user.roles"
                :key="role.id"
              >
                <span style="color: red; cursor: pointer">x</span>
                {{ role.name }}
              </div>
            </td>
            <td>
              <div
                v-for="role in roles.filter(
                  (role) =>
                    !user.roles.some((userRole) => userRole.id === role.id)
                )"
                :key="role.id"
              >
                <div @click="addUserRole(user.id, role.id)">
                  <span style="color: green; cursor: pointer">+</span>
                  {{ role.name }}
                </div>
              </div>
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
            <td>
              <input
                v-model="item.girls"
                @input="updateClassData(item.id, item.girls, item.boys)"
              />
            </td>
            <td><input
                v-model="item.boys"
                @input="updateClassData(item.id, item.girls, item.boys)"
              /></td>
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
import {
  createClass,
  deleteClass,
  getClasses,
  updateClass,
} from "../api/class";
import { deleteUser, updateUserRole } from "../api/superuser";
import { getUsers } from "../api/user";
import { createRole, deleteUserRole, getRoles } from "../api/roles";

const classData = ref({
  id: "",
  girls: 0,
  boys: 0,
});

const roleData = ref({
  name: "",
  approvement_permission: false,
  super_approvement_permission: false,
  request_permission: false,
  change_permission: false,
});

const roles = ref([]);
const classes = ref([]);
const users = ref([]);

const fetchRoles = async () => {
  roles.value = JSON.parse(await getRoles());
};

const fetchClasses = async () => {
  console.log(JSON.parse(await getClasses()));
  classes.value = JSON.parse(await getClasses());
};

const fetchUsers = async () => {
  users.value = JSON.parse(await getUsers());
};

const submitClass = async (newClass) => {
  createClass(classData.value);
  classData.value.push(newClass);
};

const submitRole = () => {
  createRole(roleData.value);
  roles.value.push(roleData.value);
};

const addUserRole = async (userId, roleId) => {
  updateUserRole(userId, roleId);
  const user = users.value.find((user) => user.id === userId);
  const role = roles.value.find((role) => role.id === roleId);

  if (user && role) {
    const hasRole = user.roles.some((userRole) => userRole.id === roleId);
    if (!hasRole) {
      user.roles.push(role);
    }
  }
};

const removeClass = async (classId) => {
  deleteClass(classId);
  classData.value = classData.value.filter(
    (schoolClass) => schoolClass.id !== classId
  );
};

const removeUser = async (userId) => {
  deleteUser(userId);
  users.value = users.value.filter((user) => user.id !== userId);
};

const removeUserRole = async (userId, roleId) => {
  deleteUserRole(userId, roleId);
  const userIndex = users.value.findIndex((user) => user.id === userId);

  if (userIndex !== -1) {
    users.value[userIndex].roles = users.value[userIndex].roles.filter(
      (role) => role.id !== roleId
    );
  }
};

const updateClassData = async (classId, girls, boys) => {
  updateClass(classId, { girl_count: girls, boy_count: boys });
};

onMounted(() => {
  fetchRoles();
  fetchClasses();
  fetchUsers();
});
</script>
