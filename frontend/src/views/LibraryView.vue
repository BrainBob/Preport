<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Finding Library</h2>
    </div>

    <!-- Filters -->
    <div class="flex gap-3 mb-5 flex-wrap">
      <Select
        v-model="severityFilter"
        :options="severityOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="All severities"
        class="w-44"
        @change="applyFilters"
      />
      <InputText v-model="search" placeholder="Search…" class="w-56" @input="onSearchInput" />
    </div>

    <div v-if="store.loading" class="space-y-3">
      <Skeleton v-for="n in 6" :key="n" height="72px" class="rounded-xl" />
    </div>

    <div v-else-if="store.items.length === 0" class="text-center py-20 text-gray-400">
      <i class="pi pi-book text-5xl mb-3" />
      <p class="text-lg">No library items yet</p>
      <p class="text-sm mt-1">Use "Add to Library" from a finding to save it here.</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="item in store.items"
        :key="item.id"
        class="bg-white rounded-xl border border-gray-200 shadow-sm px-5 py-4"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <SeverityBadge :severity="item.severity" />
              <h3 class="font-semibold text-gray-900">{{ item.title }}</h3>
            </div>
            <p class="text-sm text-gray-500 line-clamp-2" v-html="item.description" />
          </div>
          <div class="flex gap-2 ml-4 shrink-0">
            <Button label="Use in Project" icon="pi pi-arrow-right" size="small" severity="secondary" @click="openUseDialog(item)" />
            <Button icon="pi pi-trash" severity="danger" text size="small" @click="confirmDelete(item)" />
          </div>
        </div>
      </div>
    </div>

    <!-- Use in Project dialog -->
    <Dialog v-model:visible="showUseDialog" header="Add to Project" :style="{ width: '380px' }" modal>
      <div class="space-y-4 pt-2">
        <p class="text-sm text-gray-600">Select which project to add <strong>{{ selectedItem?.title }}</strong> to:</p>
        <Select v-model="targetProjectId" :options="projects" optionLabel="project_name" optionValue="id" class="w-full" placeholder="Select project…" />
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancel" severity="secondary" @click="showUseDialog = false" />
          <Button label="Add Finding" :loading="using" :disabled="!targetProjectId" @click="useInProject" />
        </div>
      </div>
    </Dialog>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { useLibraryStore } from "@/stores/library";
import { useProjectsStore } from "@/stores/projects";
import Button from "primevue/button";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Skeleton from "primevue/skeleton";
import ConfirmDialog from "primevue/confirmdialog";
import SeverityBadge from "@/components/SeverityBadge.vue";

const toast = useToast();
const confirm = useConfirm();
const store = useLibraryStore();
const projectsStore = useProjectsStore();

const projects = ref([]);
const severityFilter = ref(null);
const search = ref("");
const showUseDialog = ref(false);
const selectedItem = ref(null);
const targetProjectId = ref(null);
const using = ref(false);
let searchTimer = null;

const severityOptions = [
  { label: "All severities", value: null },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
  { label: "Info", value: "info" },
];

function buildParams() {
  const p = {};
  if (severityFilter.value) p.severity = severityFilter.value;
  if (search.value) p.search = search.value;
  return p;
}

async function applyFilters() {
  await store.fetchItems(buildParams());
}

function onSearchInput() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(applyFilters, 350);
}

function openUseDialog(item) {
  selectedItem.value = item;
  targetProjectId.value = null;
  showUseDialog.value = true;
}

async function useInProject() {
  using.value = true;
  try {
    await store.useInProject(selectedItem.value.id, targetProjectId.value);
    showUseDialog.value = false;
    toast.add({ severity: "success", summary: "Finding added to project", life: 3000 });
  } catch {
    toast.add({ severity: "error", summary: "Failed to add finding", life: 3000 });
  } finally {
    using.value = false;
  }
}

function confirmDelete(item) {
  confirm.require({
    message: `Remove "${item.title}" from library?`,
    header: "Confirm Delete",
    icon: "pi pi-trash",
    acceptClass: "p-button-danger",
    accept: async () => {
      await store.deleteItem(item.id);
      toast.add({ severity: "success", summary: "Removed from library", life: 3000 });
    },
  });
}

onMounted(async () => {
  await Promise.all([store.fetchItems(), projectsStore.fetchProjects()]);
  projects.value = projectsStore.projects;
});
</script>
