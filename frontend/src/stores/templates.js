import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/client";

export const useTemplatesStore = defineStore("templates", () => {
  const templates = ref([]);
  const currentTemplate = ref(null);
  const loading = ref(false);

  async function fetchTemplates() {
    loading.value = true;
    try {
      const { data } = await api.get("/reports/templates/");
      templates.value = data.results ?? data;
    } finally {
      loading.value = false;
    }
  }

  async function fetchTemplate(id) {
    const { data } = await api.get(`/reports/templates/${id}/`);
    currentTemplate.value = data;
    return data;
  }

  async function createTemplate(payload) {
    const { data } = await api.post("/reports/templates/", payload);
    templates.value.unshift(data);
    return data;
  }

  async function updateTemplate(id, payload) {
    const { data } = await api.patch(`/reports/templates/${id}/`, payload);
    const idx = templates.value.findIndex((t) => t.id === id);
    if (idx !== -1) templates.value[idx] = data;
    currentTemplate.value = data;
    return data;
  }

  async function cloneTemplate(id) {
    const { data } = await api.post(`/reports/templates/${id}/clone/`);
    templates.value.unshift(data);
    return data;
  }

  async function deleteTemplate(id) {
    await api.delete(`/reports/templates/${id}/`);
    templates.value = templates.value.filter((t) => t.id !== id);
  }

  return { templates, currentTemplate, loading, fetchTemplates, fetchTemplate, createTemplate, updateTemplate, cloneTemplate, deleteTemplate };
});
