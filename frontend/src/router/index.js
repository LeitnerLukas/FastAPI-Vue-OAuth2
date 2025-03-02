import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import DashboardView from '../views/DashboardView.vue';
import LoginView from '../views/LoginView.vue';
import UserManagementView from '../views/UserManagementView.vue';
import LogoutView from '../views/LogoutView.vue';
import NewActivity from '../views/NewActivity.vue';
import RefreshView from '../views/RefreshView.vue';
import ActivityView from '../views/ActivityView.vue';
import { useAuthStore } from '../store/auth';
import RegisterView from '../views/RegisterView.vue';
import ClassManagement from '../views/management/ClassManagement.vue';
import UserManagement from '../views/management/UserManagement.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "Register",
    path: "/register",
    name: "Register",
    component: RegisterView,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/user_manage",
    name: "UserManage",
    component: UserManagementView,
    meta: { requiresAuth: true },
  },
  {
    path: "/user_manage/classes",
    name: "UserManageClasses",
    component: ClassManagement,
    meta: { requiresAuth: true },
  },
  {
    path: "/user_manage/users_roles",
    name: "UserManageUsersRoles",
    component: UserManagement,
    meta: { requiresAuth: true },
  },
  {
    path: "/activity/:id",
    name: "ActivityView",
    component: ActivityView, // Use ActivityView for the /activity/:id route
    props: true, // Pass the route params as props
  },
  {
    path: "/activity/new",
    name: "NewActivity",
    component: NewActivity, // Use NewActivityView for the /activity/new route
    meta: { requiresAuth: true },
  },
  {
    path: "/logout",
    name: "Logout",
    component: LogoutView,
  },
  {
    path: "/refresh",
    name: "Refresh",
    component: RefreshView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (
      to.path.includes("/user_manage") &&
      auth.super_user_permission !== true
    ) {
      next("/dashboard");
    }
    
    if (auth.isAuthenticated) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router;
