<template>
  <div class="p-8 max-w-4xl">
    <!-- Nav -->
    <button class="text-sm text-gray-400 hover:text-gray-600 mb-4 flex items-center gap-1" @click="$router.back()">
      <i class="pi pi-arrow-left text-xs" /> Back to Project
    </button>

    <div v-if="loading" class="space-y-4">
      <Skeleton height="40px" />
      <Skeleton height="200px" />
    </div>

    <template v-else-if="finding">
      <div class="flex items-start justify-between mb-6">
        <div class="flex-1 mr-4">
          <InputText v-model="form.title" class="w-full text-xl font-bold border-0 border-b border-gray-200 rounded-none px-0 focus:border-indigo-500" />
        </div>
        <div class="flex gap-2 shrink-0">
          <Button label="Save" icon="pi pi-check" @click="save" :loading="saving" />
          <Button icon="pi pi-book" severity="secondary" v-tooltip="'Add to Library'" @click="addToLibrary" />
        </div>
      </div>

      <!-- Meta row -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div>
          <label class="field-label">Severity</label>
          <Select v-model="form.severity" :options="severityOptions" optionLabel="label" optionValue="value" class="w-full" />
        </div>
        <div>
          <label class="field-label">Status</label>
          <Select v-model="form.status" :options="statusOptions" optionLabel="label" optionValue="value" class="w-full" />
        </div>
        <div>
          <label class="field-label">CVSS Score</label>
          <InputText v-model="form.cvss_score" placeholder="0.0 – 10.0" class="w-full" />
        </div>
        <div>
          <label class="field-label">CVSS Vector</label>
          <InputText v-model="form.cvss_vector" placeholder="AV:N/AC:L/…" class="w-full font-mono text-xs" />
        </div>
      </div>

      <div class="mb-4">
        <label class="field-label">Affected Components</label>
        <InputText v-model="form.affected_components" class="w-full" placeholder="e.g. /api/login, Auth service" />
      </div>

      <!-- Rich text sections -->
      <div class="space-y-5">
        <RichTextSection v-model="form.description" label="Description" />
        <RichTextSection v-model="form.impact" label="Impact" />
        <RichTextSection v-model="form.steps_to_reproduce" label="Steps to Reproduce" />
        <RichTextSection v-model="form.remediation" label="Remediation" />
      </div>

      <!-- References -->
      <div class="mt-5">
        <div class="flex items-center justify-between mb-2">
          <label class="field-label mb-0">References</label>
          <Button label="Add" icon="pi pi-plus" size="small" severity="secondary" @click="addRef" />
        </div>
        <div v-for="(ref, idx) in form.references" :key="idx" class="flex gap-2 mb-2">
          <InputText v-model="form.references[idx]" class="flex-1" placeholder="https://…" />
          <Button icon="pi pi-times" severity="danger" text @click="form.references.splice(idx, 1)" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useFindingsStore } from "@/stores/findings";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Select from "primevue/select";
import Skeleton from "primevue/skeleton";
import RichTextSection from "@/components/RichTextSection.vue";

const route = useRoute();
const toast = useToast();
const findingsStore = useFindingsStore();

const findingId = route.params.findingId;
const finding = ref(null);
const loading = ref(true);
const saving = ref(false);

const form = ref({
  title: "", severity: "medium", status: "open",
  cvss_score: "", cvss_vector: "", affected_components: "",
  description: "", impact: "", steps_to_reproduce: "", remediation: "",
  references: [],
});

const severityOptions = [
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
  { label: "Info", value: "info" },
];

const statusOptions = [
  { label: "Open", value: "open" },
  { label: "In Review", value: "in_review" },
  { label: "Resolved", value: "resolved" },
  { label: "Accepted", value: "accepted" },
  { label: "False Positive", value: "false_positive" },
];

function loadForm(data) {
  Object.keys(form.value).forEach((k) => {
    if (data[k] !== undefined) form.value[k] = data[k] ?? form.value[k];
  });
  form.value.references = Array.isArray(data.references) ? [...data.references] : [];
}

function addRef() {
  form.value.references.push("");
}

async function save() {
  saving.value = true;
  try {
    await findingsStore.updateFinding(findingId, { ...form.value });
    toast.add({ severity: "success", summary: "Finding saved", life: 2000 });
  } catch {
    toast.add({ severity: "error", summary: "Save failed", life: 3000 });
  } finally {
    saving.value = false;
  }
}

async function addToLibrary() {
  try {
    await findingsStore.addToLibrary(findingId);
    toast.add({ severity: "success", summary: "Added to library", life: 2000 });
  } catch {
    toast.add({ severity: "error", summary: "Failed to add to library", life: 3000 });
  }
}

onMounted(async () => {
  finding.value = await findingsStore.fetchFinding(findingId);
  loadForm(finding.value);
  loading.value = false;
});
</script>

<style scoped>
.field-label { @apply block text-sm font-medium text-gray-700 mb-1; }
</style>
