import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/client";

export const useFindingsStore = defineStore("findings", () => {
  const findings = ref([]);
  const currentFinding = ref(null);
  const loading = ref(false);

  async function fetchFindings(projectId, params = {}) {
    loading.value = true;
    try {
      const { data } = await api.get("/projects/findings/", { params: { project: projectId, ...params } });
      findings.value = data.results ?? data;
    } finally {
      loading.value = false;
    }
  }

  async function fetchFinding(id) {
    const { data } = await api.get(`/projects/findings/${id}/`);
    currentFinding.value = data;
    return data;
  }

  async function createFinding(payload) {
    const { data } = await api.post("/projects/findings/", payload);
    findings.value.push(data);
    return data;
  }

  async function updateFinding(id, payload) {
    const { data } = await api.patch(`/projects/findings/${id}/`, payload);
    const idx = findings.value.findIndex((f) => f.id === id);
    if (idx !== -1) findings.value[idx] = data;
    currentFinding.value = data;
    return data;
  }

  async function deleteFinding(id) {
    await api.delete(`/projects/findings/${id}/`);
    findings.value = findings.value.filter((f) => f.id !== id);
  }

  async function addToLibrary(id) {
    const { data } = await api.post(`/projects/findings/${id}/add_to_library/`);
    return data;
  }

  async function reorderFindings(projectId, orderedIds) {
    await api.post("/projects/findings/reorder/", { project: projectId, ordered_ids: orderedIds });
    const ordered = orderedIds.map((id) => findings.value.find((f) => f.id === id)).filter(Boolean);
    findings.value = ordered;
  }

  return { findings, currentFinding, loading, fetchFindings, fetchFinding, createFinding, updateFinding, deleteFinding, addToLibrary, reorderFindings };
});
