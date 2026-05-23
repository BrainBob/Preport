import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/client";

export const useLibraryStore = defineStore("library", () => {
  const items = ref([]);
  const loading = ref(false);

  async function fetchItems(params = {}) {
    loading.value = true;
    try {
      const { data } = await api.get("/findings/library/", { params });
      items.value = data.results ?? data;
    } finally {
      loading.value = false;
    }
  }

  async function useInProject(libraryId, projectId) {
    const { data } = await api.post(`/findings/library/${libraryId}/use_in_project/`, { project_id: projectId });
    return data;
  }

  async function deleteItem(id) {
    await api.delete(`/findings/library/${id}/`);
    items.value = items.value.filter((i) => i.id !== id);
  }

  return { items, loading, fetchItems, useInProject, deleteItem };
});
