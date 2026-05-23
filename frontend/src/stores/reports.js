import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/client";

export const useReportsStore = defineStore("reports", () => {
  const reports = ref([]);
  const currentReport = ref(null);
  const loading = ref(false);
  const generating = ref(false);

  async function fetchReports(projectId) {
    loading.value = true;
    try {
      const { data } = await api.get("/reports/", { params: { project: projectId } });
      reports.value = data.results ?? data;
    } finally {
      loading.value = false;
    }
  }

  async function createReport(payload) {
    const { data } = await api.post("/reports/", payload);
    reports.value.unshift(data);
    return data;
  }

  async function generatePdf(id) {
    generating.value = true;
    try {
      const { data } = await api.post(`/reports/${id}/generate/`);
      const idx = reports.value.findIndex((r) => r.id === id);
      if (idx !== -1) reports.value[idx] = data;
      return data;
    } finally {
      generating.value = false;
    }
  }

  async function downloadPdf(id, filename) {
    const resp = await api.get(`/reports/${id}/download/`, { responseType: "blob" });
    const url = URL.createObjectURL(resp.data);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename || `report-${id}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function deleteReport(id) {
    await api.delete(`/reports/${id}/`);
    reports.value = reports.value.filter((r) => r.id !== id);
  }

  return { reports, currentReport, loading, generating, fetchReports, createReport, generatePdf, downloadPdf, deleteReport };
});
