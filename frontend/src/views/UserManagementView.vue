<template>
  <div class="container w-100 mt-5">
    <h5>Users:</h5>
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
          <td><button class="btn btn-danger">Remove</button></td>
        </tr>
      </tbody>
    </table>
    <h5>Create Class:</h5>
    <h5>Classes:</h5>
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
        <tr v-for="(item, idx) in classList" :key="idx">
          <th scope="row">{{ idx + 1 }}</th>
          <td>{{ item.classId }}</td>
          <td>{{ item.girls }}</td>
          <td>{{ item.boys }}</td>
          <td><button class="btn btn-danger">Remove</button></td>
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

const classList = [
  {
    classId: "4ahit",
    girls: 10,
    boys: 20,
  },
  {
    classId: "5ahit",
    girls: 10,
    boys: 20,
  },
];
</script>
