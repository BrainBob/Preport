import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    meta: { public: true },
  },
  {
    path: "/",
    component: () => import("@/views/AppLayout.vue"),
    children: [
      { path: "", redirect: "/projects" },
      { path: "projects", name: "projects", component: () => import("@/views/ProjectsView.vue") },
      { path: "projects/:id", name: "project-detail", component: () => import("@/views/ProjectDetailView.vue") },
      { path: "projects/:id/findings/:findingId", name: "finding-editor", component: () => import("@/views/FindingEditorView.vue") },
      { path: "reports", name: "reports", component: () => import("@/views/ReportsView.vue") },
      { path: "templates", name: "templates", component: () => import("@/views/TemplatesView.vue") },
      { path: "library", name: "library", component: () => import("@/views/LibraryView.vue") },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: "login" };
  }
});

export default router;
