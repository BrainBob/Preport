<template>
  <div class="p-8">
    <!-- Loading skeleton -->
    <div v-if="loadingProject" class="space-y-4">
      <Skeleton height="60px" />
      <Skeleton height="300px" />
    </div>

    <template v-else-if="project">
      <!-- Header -->
      <div class="flex items-start justify-between mb-6">
        <div>
          <button class="text-sm text-gray-400 hover:text-gray-600 mb-2 flex items-center gap-1" @click="$router.push('/projects')">
            <i class="pi pi-arrow-left text-xs" /> Projects
          </button>
          <h2 class="text-2xl font-bold text-gray-900">{{ project.project_name }}</h2>
          <p class="text-gray-500 text-sm mt-0.5">{{ project.client_name }}</p>
        </div>
        <div class="flex gap-2">
          <Button label="Clone" icon="pi pi-copy" severity="secondary" size="small" @click="cloneProject" :loading="cloning" />
          <Button label="Export" icon="pi pi-download" severity="secondary" size="small" @click="exportProject" />
          <Button label="Generate Report" icon="pi pi-file-pdf" size="small" @click="goToReports" />
        </div>
      </div>

      <!-- Stats row -->
      <div class="flex gap-3 mb-6 flex-wrap">
        <div v-for="sev in SEVERITIES" :key="sev" class="bg-white rounded-lg border border-gray-200 px-4 py-2 flex items-center gap-2">
          <SeverityBadge :severity="sev" />
          <span class="font-semibold text-gray-900">{{ project.findings_stats?.[sev] ?? 0 }}</span>
        </div>
        <div class="bg-white rounded-lg border border-gray-200 px-4 py-2 text-sm text-gray-500">
          {{ findingsStore.findings.length }} total findings
        </div>
      </div>

      <!-- Findings table -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100">
          <h3 class="font-semibold text-gray-900">Findings</h3>
          <div class="flex gap-2">
            <Select v-model="severityFilter" :options="severityOptions" optionLabel="label" optionValue="value" placeholder="All severities" class="w-40" @change="applyFilter" />
            <Button label="Add Finding" icon="pi pi-plus" size="small" @click="showCreateFinding = true" />
          </div>
        </div>

        <DataTable
          :value="findingsStore.findings"
          :loading="findingsStore.loading"
          stripedRows
          rowHover
          @rowClick="openFinding($event.data)"
        >
          <Column field="order" header="#" style="width: 50px" />
          <Column header="Title">
            <template #body="{ data }">
              <span class="font-medium text-gray-900 cursor-pointer hover:text-indigo-600">{{ data.title }}</span>
            </template>
          </Column>
          <Column header="Severity" style="width: 110px">
            <template #body="{ data }">
              <SeverityBadge :severity="data.severity" />
            </template>
          </Column>
          <Column field="cvss_score" header="CVSS" style="width: 80px">
            <template #body="{ data }">
              <span v-if="data.cvss_score" class="font-mono text-sm">{{ data.cvss_score }}</span>
              <span v-else class="text-gray-300">—</span>
            </template>
          </Column>
          <Column header="Status" style="width: 120px">
            <template #body="{ data }">
              <span :class="['status-pill', `status-${data.status}`]">{{ STATUS_LABELS[data.status] }}</span>
            </template>
          </Column>
          <Column style="width: 60px">
            <template #body="{ data }">
              <Button icon="pi pi-trash" severity="danger" text size="small" @click.stop="confirmDelete(data)" />
            </template>
          </Column>
          <template #empty>
            <div class="text-center py-10 text-gray-400">
              <i class="pi pi-shield text-4xl mb-2" />
              <p>No findings yet. Add one to get started.</p>
            </div>
          </template>
        </DataTable>
      </div>
    </template>

    <!-- Create Finding Dialog -->
    <Dialog v-model:visible="showCreateFinding" header="New Finding" :style="{ width: '440px' }" modal>
      <form @submit.prevent="createFinding" class="space-y-4 pt-2">
        <div>
          <label class="field-label">Title *</label>
          <InputText v-model="findingForm.title" class="w-full" required />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="field-label">Severity</label>
            <Select v-model="findingForm.severity" :options="severityOptions.slice(1)" optionLabel="label" optionValue="value" class="w-full" />
          </div>
          <div>
            <label class="field-label">CVSS Score</label>
            <InputText v-model="findingForm.cvss_score" placeholder="0.0 – 10.0" class="w-full" />
          </div>
        </div>
        <div>
          <label class="field-label">Affected Components</label>
          <InputText v-model="findingForm.affected_components" class="w-full" placeholder="e.g. /api/users, Auth module" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancel" severity="secondary" @click="showCreateFinding = false" />
          <Button type="submit" label="Create" :loading="creatingFinding" />
        </div>
      </form>
    </Dialog>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import { useProjectsStore } from "@/stores/projects";
import { useFindingsStore } from "@/stores/findings";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Skeleton from "primevue/skeleton";
import ConfirmDialog from "primevue/confirmdialog";
import SeverityBadge from "@/components/SeverityBadge.vue";

const route = useRoute();
const router = useRouter();
const confirm = useConfirm();
const toast = useToast();
const projectsStore = useProjectsStore();
const findingsStore = useFindingsStore();

const projectId = route.params.id;
const project = computed(() => projectsStore.currentProject);
const loadingProject = ref(true);
const cloning = ref(false);
const showCreateFinding = ref(false);
const creatingFinding = ref(false);
const severityFilter = ref(null);

const SEVERITIES = ["critical", "high", "medium", "low", "info"];
const STATUS_LABELS = { open: "Open", in_review: "In Review", resolved: "Resolved", accepted: "Accepted", false_positive: "False Positive" };

const severityOptions = [
  { label: "All severities", value: null },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
  { label: "Info", value: "info" },
];

const findingForm = ref(resetFindingForm());

function resetFindingForm() {
  return { title: "", severity: "medium", cvss_score: "", affected_components: "" };
}

function openFinding(finding) {
  router.push({ name: "finding-editor", params: { id: projectId, findingId: finding.id } });
}

async function applyFilter() {
  const params = severityFilter.value ? { severity: severityFilter.value } : {};
  await findingsStore.fetchFindings(projectId, params);
}

async function createFinding() {
  creatingFinding.value = true;
  try {
    await findingsStore.createFinding({ ...findingForm.value, project: projectId });
    showCreateFinding.value = false;
    findingForm.value = resetFindingForm();
    toast.add({ severity: "success", summary: "Finding created", life: 3000 });
    await projectsStore.fetchProject(projectId);
  } catch {
    toast.add({ severity: "error", summary: "Failed to create finding", life: 3000 });
  } finally {
    creatingFinding.value = false;
  }
}

function confirmDelete(finding) {
  confirm.require({
    message: `Delete "${finding.title}"?`,
    header: "Confirm Delete",
    icon: "pi pi-trash",
    acceptClass: "p-button-danger",
    accept: async () => {
      await findingsStore.deleteFinding(finding.id);
      await projectsStore.fetchProject(projectId);
      toast.add({ severity: "success", summary: "Finding deleted", life: 3000 });
    },
  });
}

async function cloneProject() {
  cloning.value = true;
  try {
    const cloned = await projectsStore.cloneProject(projectId);
    toast.add({ severity: "success", summary: "Project cloned", life: 3000 });
    router.push({ name: "project-detail", params: { id: cloned.id } });
  } catch {
    toast.add({ severity: "error", summary: "Failed to clone", life: 3000 });
  } finally {
    cloning.value = false;
  }
}

async function exportProject() {
  const resp = await import("@/api/client").then((m) => m.default.get(`/projects/${projectId}/export/`));
  const blob = new Blob([JSON.stringify(resp.data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `project-${projectId}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function goToReports() {
  router.push({ name: "reports", query: { project: projectId } });
}

onMounted(async () => {
  await Promise.all([
    projectsStore.fetchProject(projectId),
    findingsStore.fetchFindings(projectId),
  ]);
  loadingProject.value = false;
});
</script>

<style scoped>
.field-label { @apply block text-sm font-medium text-gray-700 mb-1; }
.status-pill { @apply text-xs font-medium px-2 py-0.5 rounded-full; }
.status-open          { @apply bg-red-100 text-red-700; }
.status-in_review     { @apply bg-yellow-100 text-yellow-700; }
.status-resolved      { @apply bg-green-100 text-green-700; }
.status-accepted      { @apply bg-blue-100 text-blue-700; }
.status-false_positive { @apply bg-gray-100 text-gray-500; }
</style>
