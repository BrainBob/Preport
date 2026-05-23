<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-56 bg-gray-900 text-white flex flex-col shrink-0">
      <div class="px-5 py-5 border-b border-gray-700">
        <h1 class="text-lg font-bold tracking-tight">Preport</h1>
        <p class="text-xs text-gray-400 mt-0.5">Pentest Reports</p>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          class="nav-link"
          :class="{ active: isActive(item.to) }"
        >
          <i :class="['pi', item.icon, 'text-sm']" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="px-3 py-4 border-t border-gray-700">
        <div class="flex items-center gap-3 px-2 py-2">
          <div class="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-xs font-semibold">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ auth.user?.username }}</p>
            <p class="text-xs text-gray-400 truncate">{{ auth.user?.email }}</p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="mt-2 w-full text-left px-2 py-1.5 text-xs text-gray-400 hover:text-white rounded transition-colors"
        >
          <i class="pi pi-sign-out mr-1" /> Sign out
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const navItems = [
  { label: "Projects", to: "/projects", icon: "pi-folder" },
  { label: "Reports", to: "/reports", icon: "pi-file-pdf" },
  { label: "Templates", to: "/templates", icon: "pi-file-edit" },
  { label: "Library", to: "/library", icon: "pi-book" },
];

const userInitials = computed(() => {
  const u = auth.user;
  if (!u) return "?";
  return (u.first_name?.[0] || u.username?.[0] || "U").toUpperCase();
});

function isActive(path) {
  return route.path.startsWith(path);
}

async function handleLogout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-gray-800 transition-colors;
}
.nav-link.active {
  @apply text-white bg-gray-800;
}
</style>
