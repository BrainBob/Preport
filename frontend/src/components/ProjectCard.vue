<template>
  <div
    class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow cursor-pointer"
    @click="$router.push({ name: 'project-detail', params: { id: project.id } })"
  >
    <div class="flex items-start justify-between mb-3">
      <div>
        <h3 class="font-semibold text-gray-900 text-base leading-tight">{{ project.project_name }}</h3>
        <p class="text-sm text-gray-500 mt-0.5">{{ project.client_name }}</p>
      </div>
      <span :class="['status-chip', `status-${project.status}`]">{{ STATUS_LABELS[project.status] }}</span>
    </div>

    <div class="flex items-center gap-1.5 flex-wrap mt-3">
      <span v-for="(count, sev) in project.findings_stats" :key="sev" v-show="count > 0">
        <SeverityBadge :severity="sev" />
        <span class="text-xs text-gray-600 ml-0.5">{{ count }}</span>
      </span>
      <span v-if="!hasFindings" class="text-xs text-gray-400">No findings yet</span>
    </div>

    <div class="flex items-center justify-between mt-4 text-xs text-gray-400">
      <span>{{ project.project_type?.replace("_", " ") }}</span>
      <span v-if="project.end_date">Due {{ formatDate(project.end_date) }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import SeverityBadge from "./SeverityBadge.vue";

const props = defineProps({
  project: { type: Object, required: true },
});

const STATUS_LABELS = {
  planning: "Planning",
  in_progress: "In Progress",
  review: "Review",
  completed: "Completed",
  archived: "Archived",
};

const hasFindings = computed(() => {
  return Object.values(props.project.findings_stats ?? {}).some((c) => c > 0);
});

function formatDate(d) {
  return new Date(d).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}
</script>

<style scoped>
.status-chip {
  @apply text-xs font-medium px-2 py-0.5 rounded-full;
}
.status-planning    { @apply bg-blue-100 text-blue-700; }
.status-in_progress { @apply bg-yellow-100 text-yellow-700; }
.status-review      { @apply bg-purple-100 text-purple-700; }
.status-completed   { @apply bg-green-100 text-green-700; }
.status-archived    { @apply bg-gray-100 text-gray-500; }
</style>
