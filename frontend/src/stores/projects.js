import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api/client";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref([]);
  const currentProject = ref(null);
  const loading = ref(false);

  async function fetchProjects(params = {}) {
    loading.value = true;
    try {
      const { data } = await api.get("/projects/", { params });
      projects.value = data.results ?? data;
    } finally {
      loading.value = false;
    }
  }

  async function fetchProject(id) {
    const { data } = await api.get(`/projects/${id}/`);
    currentProject.value = data;
    return data;
  }

  async function createProject(payload) {
    const { data } = await api.post("/projects/", payload);
    projects.value.unshift(data);
    return data;
  }

  async function updateProject(id, payload) {
    const { data } = await api.patch(`/projects/${id}/`, payload);
    const idx = projects.value.findIndex((p) => p.id === id);
    if (idx !== -1) projects.value[idx] = data;
    currentProject.value = data;
    return data;
  }

  async function deleteProject(id) {
    await api.delete(`/projects/${id}/`);
    projects.value = projects.value.filter((p) => p.id !== id);
  }

  async function cloneProject(id) {
    const { data } = await api.post(`/projects/${id}/clone/`);
    projects.value.unshift(data);
    return data;
  }

  return { projects, currentProject, loading, fetchProjects, fetchProject, createProject, updateProject, deleteProject, cloneProject };
});
