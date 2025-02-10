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
  const approvement_permission = ref(null);
  const super_approvement_permission = ref(null);
  const request_permission = ref(null);
  const change_permission = ref(null);

  const loadingStore = useLoadingStore();
  const dialogStore = useDialogStore();

  const isAuthenticated = computed(() => access_token.value);
  const get_access_token = computed(() => access_token.value);
  const get_approvement_permission = computed(
    () => approvement_permission.value
  );
  const get_super_approvement_permission = computed(
    () => super_approvement_permission.value
  );
  const get_request_permission = computed(() => request_permission.value);
  const get_change_permission = computed(() => change_permission.value);

  async function login(form) {
    access_token.value = null;
    approvement_permission.value = null;
    super_approvement_permission.value = null;
    request_permission.value = null;
    change_permission.value = null;

    loadingStore.setLoading();

    apiLogin(form)
      .then((res) => {
        access_token.value = res.data.access_token;
        approvement_permission.value = res.data.role.approvement_permission;
        super_approvement_permission.value =
          res.data.role.super_approvement_permission;
        request_permission.value = res.data.role.request_permission;
        change_permission.value = res.data.role.change_permission;

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
        approvement_permission.value = null;
        super_approvement_permission.value = null;
        request_permission.value = null;
        change_permission.value = null;
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
    approvement_permission.value = null;
    super_approvement_permission.value = null;
    request_permission.value = null;
    change_permission.value = null;

    loadingStore.setLoading();

    await apiLoginSuperuser(form)
      .then((res) => {
        access_token.value = res.data.access_token;
        approvement_permission.value = true;
        super_approvement_permission.value = true;
        request_permission.value = true;
        change_permission.value = true;

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
        approvement_permission.value = null;
        super_approvement_permission.value = null;
        request_permission.value = null;
        change_permission.value = null;
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
      approvement_permission.value = null;
      super_approvement_permission.value = null;
      request_permission.value = null;
      change_permission.value = null;

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

    apiRefresh()
      .then((res) => {
        access_token.value = res.data.access_token;
        approvement_permission.value = res.data.role.approvement_permission;
        super_approvement_permission.value =
          res.data.role.super_approvement_permission;
        request_permission.value = res.data.role.request_permission;
        change_permission.value = res.data.role.change_permission;

        dialogStore.setSuccess({
          title: "Refresh Success",
          firstLine: "Redirecting to profile page",
          secondLine: "This dialog will close in 1 seconds",
        });
      })
      .catch((err) => {
        console.log(err);
        access_token.value = null;
        approvement_permission.value = null;
        super_approvement_permission.value = null;
        request_permission.value = null;
        change_permission.value = null;

        dialogStore.setError({
          title: "Refresh Failed",
          firstLine: "Please login again",
          secondLine: "This dialog will close in 1 seconds",
        });
      })
      .finally(() => {
        setTimeout(() => {
          if (isAuthenticated.value) {
            router.push("/dashboard");
            console.log("pushed to profile");
          } else {
            router.push("/login");
            console.log("pushed to login");
          }

          dialogStore.reset();
          loadingStore.clearLoading();
        }, 1000);
      });
  }

  function refreshForLogin() {
    loadingStore.setLoading();

    apiRefresh()
      .then((res) => {
        access_token.value = res.data.access_token;
        approvement_permission.value = null;
        super_approvement_permission.value = null;
        request_permission.value = null;
        change_permission.value = null;
      })
      .catch((err) => {
        console.log(err);
        access_token.value = null;
      })
      .finally(() => {
        if (isAuthenticated.value) {
          router.push("/dashboard");
          console.log("pushed to profile");
        } else {
          router.push("/login");
          console.log("pushed to login");
        }

        loadingStore.clearLoading();
      });
  }

  return {
    get_access_token,
    get_approvement_permission,
    get_super_approvement_permission,
    get_request_permission,
    get_change_permission,
    access_token,
    isAuthenticated,
    approvement_permission,
    super_approvement_permission: true,
    request_permission,
    change_permission,
    login,
    logout,
    refresh,
    superuserLogin,
    refreshForLogin,
  };
});
