<template>
  <div class="container w-100 mt-5">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Email</th>
          <th scope="col">Name</th>
          <th scope="col">Role</th>
          <th scope="col">Change Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, idx) in userList" :key="idx">
          <th scope="row">{{ idx + 1 }}</th>
          <td>{{ user.email }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.role.name }}</td>
          <td>
            <select id="roleSelect" class="form-select">
              <option v-for="role in roles" :key="role.name" :value="role.name">
                {{ role.name }}
              </option>
            </select>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const roles = [
  { name: "Teacher" },
  { name: "SuperUser" },
  { name: "Head of Department" },
  { name: "Principal" },
];

import { useFetchUser } from "../store/user";
// const { userList } = useFetchUser();
const userList = [
  {
    email: "fs@gmail.com",
    name: "Fahad",
    role: {
      name: "Teacher",
    },
  },
  {
    email: "jp@gmail.com",
    name: "Jpid",
    role: {
      name: "Principal",
    },
  },
];
</script>
