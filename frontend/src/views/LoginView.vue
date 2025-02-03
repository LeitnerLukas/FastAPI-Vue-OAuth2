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
          Login</button
        ><a
          href="https://localhost:8008/ms/login"
          class="btn btn-secondary mt-2 w-100"
        >
          Login with microsoft
        </a>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../store/auth";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const form = ref({
  username: "",
  password: "",
});

const auth = useAuthStore();

const submit = async () => {
  await auth.login(form.value);
};

onMounted(() => {
  const accessToken = route.query.access_token;
  if (accessToken) {
    auth.access_token = accessToken;
    router.replace({ query: {} });
    if(auth.isAuthenticated) {
      router.push("/dashboard");
    }
  }
});
</script>
