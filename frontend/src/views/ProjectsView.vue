<template>
  <div class="p-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Projects</h2>
        <p class="text-gray-500 text-sm mt-0.5">{{ store.projects.length }} project{{ store.projects.length !== 1 ? "s" : "" }}</p>
      </div>
      <Button label="New Project" icon="pi pi-plus" @click="showCreateDialog = true" />
    </div>

    <!-- Filters -->
    <div class="flex gap-3 mb-6 flex-wrap">
      <Select
        v-model="filterStatus"
        :options="statusOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="All statuses"
        class="w-44"
        @change="fetchWithFilters"
      />
      <Select
        v-model="filterType"
        :options="typeOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="All types"
        class="w-44"
        @change="fetchWithFilters"
      />
      <InputText v-model="search" placeholder="Search…" class="w-56" @input="onSearchInput" />
    </div>

    <!-- Grid -->
    <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <Skeleton v-for="n in 8" :key="n" height="160px" class="rounded-xl" />
    </div>

    <div v-else-if="store.projects.length === 0" class="text-center py-20 text-gray-400">
      <i class="pi pi-folder-open text-5xl mb-3" />
      <p class="text-lg">No projects found</p>
      <Button label="Create first project" class="mt-4" @click="showCreateDialog = true" />
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <ProjectCard v-for="p in store.projects" :key="p.id" :project="p" />
    </div>

    <!-- Create Project Dialog -->
    <Dialog v-model:visible="showCreateDialog" header="New Project" :style="{ width: '480px' }" modal>
      <form @submit.prevent="createProject" class="space-y-4 pt-2">
        <div>
          <label class="field-label">Client Name *</label>
          <InputText v-model="form.client_name" class="w-full" required />
        </div>
        <div>
          <label class="field-label">Project Name *</label>
          <InputText v-model="form.project_name" class="w-full" required />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="field-label">Type</label>
            <Select v-model="form.project_type" :options="typeOptions.slice(1)" optionLabel="label" optionValue="value" class="w-full" />
          </div>
          <div>
            <label class="field-label">Status</label>
            <Select v-model="form.status" :options="statusOptions.slice(1)" optionLabel="label" optionValue="value" class="w-full" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="field-label">Start Date</label>
            <DatePicker v-model="form.start_date" dateFormat="yy-mm-dd" class="w-full" />
          </div>
          <div>
            <label class="field-label">End Date</label>
            <DatePicker v-model="form.end_date" dateFormat="yy-mm-dd" class="w-full" />
          </div>
        </div>
        <div>
          <label class="field-label">Scope</label>
          <Textarea v-model="form.scope" rows="3" class="w-full" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancel" severity="secondary" @click="showCreateDialog = false" />
          <Button type="submit" label="Create" :loading="creating" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { useProjectsStore } from "@/stores/projects";
import Button from "primevue/button";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Dialog from "primevue/dialog";
import DatePicker from "primevue/datepicker";
import Skeleton from "primevue/skeleton";
import ProjectCard from "@/components/ProjectCard.vue";

const store = useProjectsStore();
const toast = useToast();

const showCreateDialog = ref(false);
const creating = ref(false);
const filterStatus = ref(null);
const filterType = ref(null);
const search = ref("");
let searchTimer = null;

const statusOptions = [
  { label: "All statuses", value: null },
  { label: "Planning", value: "planning" },
  { label: "In Progress", value: "in_progress" },
  { label: "Review", value: "review" },
  { label: "Completed", value: "completed" },
  { label: "Archived", value: "archived" },
];

const typeOptions = [
  { label: "All types", value: null },
  { label: "External", value: "external" },
  { label: "Internal", value: "internal" },
  { label: "Web", value: "web" },
  { label: "Mobile", value: "mobile" },
  { label: "Social Engineering", value: "social" },
  { label: "Physical", value: "physical" },
  { label: "Red Team", value: "red_team" },
];

const form = ref(resetForm());

function resetForm() {
  return { client_name: "", project_name: "", project_type: "web", status: "planning", start_date: null, end_date: null, scope: "" };
}

function buildParams() {
  const p = {};
  if (filterStatus.value) p.status = filterStatus.value;
  if (filterType.value) p.project_type = filterType.value;
  if (search.value) p.search = search.value;
  return p;
}

async function fetchWithFilters() {
  await store.fetchProjects(buildParams());
}

function onSearchInput() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(fetchWithFilters, 350);
}

async function createProject() {
  creating.value = true;
  try {
    const payload = { ...form.value };
    if (payload.start_date instanceof Date) payload.start_date = payload.start_date.toISOString().slice(0, 10);
    if (payload.end_date instanceof Date) payload.end_date = payload.end_date.toISOString().slice(0, 10);
    await store.createProject(payload);
    showCreateDialog.value = false;
    form.value = resetForm();
    toast.add({ severity: "success", summary: "Project created", life: 3000 });
  } catch {
    toast.add({ severity: "error", summary: "Failed to create project", life: 3000 });
  } finally {
    creating.value = false;
  }
}

onMounted(() => store.fetchProjects());
</script>

<style scoped>
.field-label { @apply block text-sm font-medium text-gray-700 mb-1; }
</style>
