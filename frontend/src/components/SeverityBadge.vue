<template>
  <span :class="['severity-badge', `sev-${severity}`]">{{ label }}</span>
</template>

<script setup>
const props = defineProps({
  severity: { type: String, required: true },
});

const LABELS = { critical: "Critical", high: "High", medium: "Medium", low: "Low", info: "Info" };
const label = LABELS[props.severity] ?? props.severity;
</script>

<style scoped>
.severity-badge {
  @apply inline-block px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wide text-white;
}
.sev-critical { background: #FF0000; }
.sev-high     { background: #FF6B00; }
.sev-medium   { background: #FFD700; color: #333; }
.sev-low      { background: #00C853; }
.sev-info     { background: #2196F3; }
</style>
