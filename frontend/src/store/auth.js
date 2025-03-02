import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
  apiLogin,
  apiRefresh,
  apiLogout,
  apiLoginSuperuser,
} from "../api/auth";
import { useLoadingStore } from "./loading";
import { useDialogStore } from "./dialog";
import router from "../router";

export const useAuthStore = defineStore("auth", () => {
  const access_token = ref(null);
  const super_user_permission = ref(null);

  const loadingStore = useLoadingStore();
  const dialogStore = useDialogStore();

  const isAuthenticated = computed(() => access_token.value);
  const get_access_token = computed(() => access_token.value);
  const get_super_user_permission = computed(() => super_user_permission.value);
  const isSuperUser = computed(() => super_user_permission.value);

  async function login(form) {
    access_token.value = null;
    super_user_permission.value = null;

    loadingStore.setLoading();

    apiLogin(form)
      .then((res) => {
        access_token.value = res.data.access_token;

        dialogStore.setSuccess({
          title: "Login Success",
          firstLine: "You can login now",
          secondLine: "This dialog will close in 1 seconds",
        });
      })
      .catch((err) => {
        dialogStore.setError({
          title: "Login Failed",
          firstLine: "Please check your input",
          secondLine: "This dialog will close in 1 seconds",
        });
        access_token.value = null;
      })
      .finally(() => {
        loadingStore.clearLoading();
        setTimeout(() => {
          dialogStore.reset();

          console.log(isAuthenticated.value);
          console.log(access_token.value);

          if (isAuthenticated.value) {
            router.push("/dashboard");
            console.log("pushed to profile");
          }
        }, 1000);
      });
  }

  async function superuserLogin(form) {
    access_token.value = null;
    super_user_permission.value = null;
    loadingStore.setLoading();

    await apiLoginSuperuser(form)
      .then((res) => {
        access_token.value = res.data.access_token;
        super_user_permission.value = true;
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("superuser", true);

        dialogStore.setSuccess({
          title: "Login Success",
          firstLine: "You can login now",
          secondLine: "This dialog will close in 1 seconds",
        });
      })
      .catch((err) => {
        dialogStore.setError({
          title: "Login Failed",
          firstLine: "Please check your input",
          secondLine: "This dialog will close in 1 seconds",
        });
        access_token.value = null;
        super_user_permission.value = null;
      })
      .finally(() => {
        loadingStore.clearLoading();
        setTimeout(() => {
          dialogStore.reset();

          console.log(isAuthenticated.value);
          console.log(access_token.value);

          if (isAuthenticated.value) {
            router.push("/dashboard");
            console.log("pushed to profile");
          }
        }, 1000);
      });
  }

  function logout() {
    apiLogout().then((res) => {
      access_token.value = null;
      localStorage.removeItem("token");
      localStorage.removeItem("superuser");

      dialogStore.setSuccess({
        title: "Logout Success",
        firstLine: "Redirecting to login page 1 second",
        secondLine: "",
      });

      setTimeout(() => {
        dialogStore.reset();
        router.push("/login");
      }, 1000);
    });
  }

  function refresh() {
    loadingStore.setLoading();

    access_token.value = localStorage.getItem("token");
    super_user_permission.value = localStorage.getItem("superuser");

    loadingStore.clearLoading();
  }

  function refreshForLogin() {
    loadingStore.setLoading();

    access_token.value = localStorage.getItem("token");
    super_user_permission.value = localStorage.getItem("superuser");

    loadingStore.clearLoading();
  }

  return {
    get_access_token,
    get_super_user_permission,
    access_token,
    isAuthenticated,
    isSuperUser,
    super_user_permission,
    login,
    logout,
    refresh,
    superuserLogin,
    refreshForLogin,
  };
});
