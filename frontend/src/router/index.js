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

const routes = [
  {
    path: '/api',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/apilogin',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/apiregister',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/apiregister',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/apidashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/apiuser_manage',
    name: 'UserManage',
    component: UserManagementView,
    meta: { requiresAuth: true },
  },
  {
    path: '/apiactivity/:id',
    name: 'ActivityView',
    component: ActivityView, // Use ActivityView for the /activity/:id route
    props: true, // Pass the route params as props
  },
  {
    path: '/apiactivity/new',
    name: 'NewActivity',
    component: NewActivity, // Use NewActivityView for the /activity/new route
    meta: { requiresAuth: true },
  },
  {
    path: '/apilogout',
    name: 'Logout',
    component: LogoutView,
  },
  {
    path: '/apirefresh',
    name: 'Refresh',
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
    if (auth.isAuthenticated) {
      next();
      return;
    }
    next('/apilogin');
  } else {
    if (
      to.path === '/apiuser_manage' &&
      auth.super_approvement_permission !== true
    ) {
      next('/apidashboard');
    }
    next();
  }
});

export default router;
