<template>
  <div class="row d-flex justify-content-center mx-auto mt-5">
    <div class="col-4 pt-6">
      <form>
        <div class="form-group">
          <label for="usernameField">Username</label>
          <input
            v-model="form.username"
            type="text"
            class="form-control"
            id="usernameField"
          />
        </div>
        <div class="form-group">
          <label for="passwordField">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="form-control"
            id="passwordField"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100" v-on:click="submit">
          Login
        </button>
        <button type="submit" class="btn btn-secondary mt-2 w-100" v-on:click="loginMicrosoft">
          Login with microsoft
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../store/auth";

const form = ref({
  username: "",
  password: "",
});

const auth = useAuthStore();

const submit = async () => {
  await auth.login(form.value);
};

const loginMicrosoft = async () => {
  await auth.loginMicrosoft();
};

onMounted(() => {
  auth.refreshForLogin();
});
</script>
