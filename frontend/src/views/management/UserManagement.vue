<template>
  <div class="container mt-4">
    <router-link to="/user_manage">&lt; Back</router-link>
    <h5 class="mt-3">Create New Role</h5>
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
            <th scope="row">{{ idx }}</th>
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
            <td>{{ user.username }}</td>
            <td>{{ user.name }}</td>
            <td>
              <div
                v-if="user.roles"
                @click="removeUserRole(user.username, role)"
                v-for="role in user.roles"
                :key="role"
              >
                <span style="color: red; cursor: pointer">x</span>
                {{ role }}
              </div>
            </td>
            <td>
              <div
                v-if="user.roles"
                v-for="role in roles.filter(
                  (role) =>
                    !user.roles.some((userRole) => userRole === role.name)
                )"
                :key="role.name"
              >
                <div @click="addUserRole(user.username, role.name)">
                  <span style="color: green; cursor: pointer">+</span>
                  {{ role.name }}
                </div>
              </div>
            </td>
            <td>
              <button class="btn btn-danger" @click="removeUser(user.username)">
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
import { deleteUser } from "../../api/superuser";
import { getUsers } from "../../api/user";
import { createRole, deleteUserRole, getRoles, updateUserRole } from "../../api/roles";
import { useDialogStore } from "../../store/dialog";
import { useAuthStore } from '../../store/auth';

const auth = useAuthStore();

const roleData = ref({
  name: "",
  approvement_permission: false,
  super_approvement_permission: false,
  request_permission: false,
  change_permission: false,
});

const roles = ref([]);
const users = ref([]);

const dialogStore = useDialogStore();

const fetchRoles = async () => {
  const fetchedRoles = await getRoles(auth.access_token);
  roles.value = fetchedRoles.data;
};

const fetchUsers = async () => {
  const fetchedUsers = await getUsers(auth.access_token);
  users.value = fetchedUsers.data;
};

const submitRole = async () => {
  try {
    await createRole(roleData.value, auth.access_token);
    roles.value.push(roleData.value);
  } catch (error) {
    dialogStore.setError({
      title: "Error creating role",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const addUserRole = async (userdata, roledata) => {
  try {
    await updateUserRole(userdata, roledata, auth.access_token);
    const user = users.value.find((user) => user.username === userdata);
    const role = roles.value.find((role) => role.name === roledata);

    if (user && role) {
      const hasRole = user.roles.some((userRole) => userRole.name === roledata);
      if (!hasRole) {
        user.roles.push(role.name);
      }
    }
  } catch (error) {
    dialogStore.setError({
      title: "Error adding role",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const removeUser = async (username) => {
  try {
    await deleteUser(username, auth.access_token);
    users.value = users.value.filter((user) => user.username !== username);
  } catch (error) {
    dialogStore.setError({
      title: "Error removing user",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

const removeUserRole = async (userdata, roledata) => {
  try {
    await deleteUserRole(userdata, roledata, auth.access_token);
    const userIndex = users.value.findIndex((user) => user.username === userdata);

    if (userIndex !== -1) {
      users.value[userIndex].roles = users.value[userIndex].roles.filter(
        (role) => role !== roledata
      );
    }
  } catch (error) {
    dialogStore.setError({
      title: "Error removing role",
      firstLine: "",
      secondLine: "",
    });
    setTimeout(() => {
      dialogStore.reset();
    }, 1000);
  }
};

onMounted(() => {
  fetchRoles();
  fetchUsers();
});
</script>
