<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Reports</h2>
      <Button label="New Report" icon="pi pi-plus" @click="showCreateDialog = true" :disabled="!projects.length" />
    </div>

    <!-- Project filter -->
    <div class="mb-5" v-if="projects.length">
      <Select
        v-model="selectedProject"
        :options="projects"
        optionLabel="project_name"
        optionValue="id"
        placeholder="Filter by project"
        class="w-64"
        @change="fetchReports"
        showClear
      />
    </div>

    <div v-if="store.loading" class="space-y-3">
      <Skeleton v-for="n in 4" :key="n" height="72px" class="rounded-xl" />
    </div>

    <div v-else-if="store.reports.length === 0" class="text-center py-20 text-gray-400">
      <i class="pi pi-file-pdf text-5xl mb-3" />
      <p class="text-lg">No reports yet</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="report in store.reports"
        :key="report.id"
        class="bg-white rounded-xl border border-gray-200 shadow-sm px-5 py-4 flex items-center justify-between"
      >
        <div>
          <h3 class="font-semibold text-gray-900">{{ report.title }}</h3>
          <p class="text-sm text-gray-400 mt-0.5">{{ formatDate(report.created_at) }}</p>
        </div>
        <div class="flex items-center gap-3">
          <span :class="['report-status', `rs-${report.status}`]">{{ report.status }}</span>
          <Button
            icon="pi pi-bolt"
            label="Generate"
            size="small"
            severity="secondary"
            :loading="generating[report.id]"
            :disabled="report.status === 'generating'"
            @click="generate(report)"
          />
          <Button
            icon="pi pi-download"
            size="small"
            :disabled="report.status !== 'ready'"
            @click="store.downloadPdf(report.id, `${report.title}.pdf`)"
          />
          <Button icon="pi pi-trash" severity="danger" text size="small" @click="confirmDelete(report)" />
        </div>
      </div>
    </div>

    <!-- Create Report Dialog -->
    <Dialog v-model:visible="showCreateDialog" header="New Report" :style="{ width: '440px' }" modal>
      <form @submit.prevent="createReport" class="space-y-4 pt-2">
        <div>
          <label class="field-label">Project *</label>
          <Select v-model="reportForm.project" :options="projects" optionLabel="project_name" optionValue="id" class="w-full" required />
        </div>
        <div>
          <label class="field-label">Report Title *</label>
          <InputText v-model="reportForm.title" class="w-full" required placeholder="Penetration Test Report – Q3 2026" />
        </div>
        <div>
          <label class="field-label">Template</label>
          <Select v-model="reportForm.template" :options="templates" optionLabel="name" optionValue="id" class="w-full" showClear placeholder="(none)" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancel" severity="secondary" @click="showCreateDialog = false" />
          <Button type="submit" label="Create" :loading="creating" />
        </div>
      </form>
    </Dialog>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { useReportsStore } from "@/stores/reports";
import { useProjectsStore } from "@/stores/projects";
import { useTemplatesStore } from "@/stores/templates";
import Button from "primevue/button";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Skeleton from "primevue/skeleton";
import ConfirmDialog from "primevue/confirmdialog";

const route = useRoute();
const toast = useToast();
const confirm = useConfirm();
const store = useReportsStore();
const projectsStore = useProjectsStore();
const templatesStore = useTemplatesStore();

const projects = ref([]);
const templates = ref([]);
const selectedProject = ref(route.query.project || null);
const showCreateDialog = ref(false);
const creating = ref(false);
const generating = reactive({});

const reportForm = ref({ project: selectedProject.value, title: "", template: null });

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }) : "";
}

async function fetchReports() {
  await store.fetchReports(selectedProject.value);
}

async function generate(report) {
  generating[report.id] = true;
  try {
    await store.generatePdf(report.id);
    toast.add({ severity: "success", summary: "PDF generated", life: 3000 });
  } catch {
    toast.add({ severity: "error", summary: "Generation failed", life: 3000 });
  } finally {
    generating[report.id] = false;
  }
}

async function createReport() {
  creating.value = true;
  try {
    await store.createReport(reportForm.value);
    showCreateDialog.value = false;
    toast.add({ severity: "success", summary: "Report created", life: 3000 });
  } catch {
    toast.add({ severity: "error", summary: "Failed to create report", life: 3000 });
  } finally {
    creating.value = false;
  }
}

function confirmDelete(report) {
  confirm.require({
    message: `Delete "${report.title}"?`,
    header: "Confirm Delete",
    icon: "pi pi-trash",
    acceptClass: "p-button-danger",
    accept: async () => {
      await store.deleteReport(report.id);
      toast.add({ severity: "success", summary: "Report deleted", life: 3000 });
    },
  });
}

onMounted(async () => {
  await Promise.all([projectsStore.fetchProjects(), templatesStore.fetchTemplates()]);
  projects.value = projectsStore.projects;
  templates.value = templatesStore.templates;
  if (selectedProject.value) fetchReports();
});
</script>

<style scoped>
.field-label { @apply block text-sm font-medium text-gray-700 mb-1; }
.report-status { @apply text-xs font-medium px-2.5 py-1 rounded-full capitalize; }
.rs-draft      { @apply bg-gray-100 text-gray-600; }
.rs-generating { @apply bg-yellow-100 text-yellow-700; }
.rs-ready      { @apply bg-green-100 text-green-700; }
.rs-failed     { @apply bg-red-100 text-red-700; }
</style>
