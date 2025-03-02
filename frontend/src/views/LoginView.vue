<template>
  <div class="row d-flex justify-content-center mx-auto mt-5">
    <div class="col-4 pt-6">
      <form>
        <div class="form-group">
          <label for="passwordField">Password</label>
          <input
            v-model="form.api_key"
            type="password"
            class="form-control"
            id="passwordField"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100" v-on:click="submit">
          Superuser-Login</button
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
  api_key: ""
});

const auth = useAuthStore();

const submit = async (event) => {
  event.preventDefault();
  await auth.superuserLogin(form.value.api_key);
};

onMounted(() => {
  const accessToken = route.query.access_token;
  if (accessToken) {
    auth.access_token = accessToken;
    localStorage.setItem("token", accessToken);
    router.replace({ query: {} });
    if(auth.isAuthenticated) {
      router.push("/dashboard");
    }
  }
});
</script>
