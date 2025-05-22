import { createRouter, createWebHistory } from "vue-router";
import { authStore } from "@/stores/auth";
import Login from "@/components/auth/Login.vue";
import Register from "@/components/auth/Register.vue";
import Dashboard from "@/components/Dashboard.vue";
import RootLayout from "@/components/RootLayout.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: { layout: RootLayout },
    },
    {
      path: "/register",
      name: "register",
      component: Register,
      meta: { layout: RootLayout },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: Dashboard,
      meta: { requiresAuth: true, layout: RootLayout },
    },
  ],
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = authStore.isAuthenticated();

  if (requiresAuth && !isAuthenticated) {
    next("/login");
  } else if (
    (to.path === "/login" || to.path === "/register") &&
    isAuthenticated
  ) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
