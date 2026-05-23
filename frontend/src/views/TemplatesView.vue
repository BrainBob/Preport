<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Report Templates</h2>
      <Button label="New Template" icon="pi pi-plus" @click="openCreate" />
    </div>

    <div v-if="store.loading" class="space-y-3">
      <Skeleton v-for="n in 3" :key="n" height="80px" class="rounded-xl" />
    </div>

    <div v-else-if="store.templates.length === 0" class="text-center py-20 text-gray-400">
      <i class="pi pi-file-edit text-5xl mb-3" />
      <p class="text-lg">No templates yet</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="t in store.templates"
        :key="t.id"
        class="bg-white rounded-xl border border-gray-200 shadow-sm px-5 py-4 flex items-center justify-between"
      >
        <div>
          <div class="flex items-center gap-2">
            <h3 class="font-semibold text-gray-900">{{ t.name }}</h3>
            <span v-if="t.is_default" class="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">Default</span>
          </div>
          <p class="text-sm text-gray-400 mt-0.5">{{ t.description || "No description" }}</p>
        </div>
        <div class="flex gap-2">
          <Button icon="pi pi-pencil" severity="secondary" size="small" @click="openEdit(t)" />
          <Button icon="pi pi-copy" severity="secondary" size="small" v-tooltip="'Clone'" @click="cloneTemplate(t)" />
          <Button icon="pi pi-trash" severity="danger" text size="small" @click="confirmDelete(t)" />
        </div>
      </div>
    </div>

    <!-- Create / Edit Dialog -->
    <Dialog v-model:visible="showDialog" :header="editing ? 'Edit Template' : 'New Template'" :style="{ width: '560px' }" modal>
      <form @submit.prevent="save" class="space-y-4 pt-2">
        <div>
          <label class="field-label">Name *</label>
          <InputText v-model="form.name" class="w-full" required />
        </div>
        <div>
          <label class="field-label">Description</label>
          <InputText v-model="form.description" class="w-full" />
        </div>
        <div class="flex items-center gap-2">
          <Checkbox v-model="form.is_default" inputId="is_default" :binary="true" />
          <label for="is_default" class="text-sm text-gray-700">Set as default template</label>
        </div>
        <div>
          <label class="field-label">CSS Styles</label>
          <Textarea v-model="form.css_styles" rows="5" class="w-full font-mono text-xs" placeholder="/* custom CSS for PDF */" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancel" severity="secondary" @click="showDialog = false" />
          <Button type="submit" :label="editing ? 'Save' : 'Create'" :loading="saving" />
        </div>
      </form>
    </Dialog>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { useTemplatesStore } from "@/stores/templates";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea";
import Checkbox from "primevue/checkbox";
import Dialog from "primevue/dialog";
import Skeleton from "primevue/skeleton";
import ConfirmDialog from "primevue/confirmdialog";

const toast = useToast();
const confirm = useConfirm();
const store = useTemplatesStore();

const showDialog = ref(false);
const editing = ref(null);
const saving = ref(false);
const form = ref(resetForm());

function resetForm() {
  return { name: "", description: "", is_default: false, css_styles: "" };
}

function openCreate() {
  editing.value = null;
  form.value = resetForm();
  showDialog.value = true;
}

function openEdit(t) {
  editing.value = t;
  form.value = { name: t.name, description: t.description, is_default: t.is_default, css_styles: t.css_styles };
  showDialog.value = true;
}

async function save() {
  saving.value = true;
  try {
    if (editing.value) {
      await store.updateTemplate(editing.value.id, form.value);
      toast.add({ severity: "success", summary: "Template updated", life: 3000 });
    } else {
      await store.createTemplate(form.value);
      toast.add({ severity: "success", summary: "Template created", life: 3000 });
    }
    showDialog.value = false;
  } catch {
    toast.add({ severity: "error", summary: "Save failed", life: 3000 });
  } finally {
    saving.value = false;
  }
}

async function cloneTemplate(t) {
  try {
    await store.cloneTemplate(t.id);
    toast.add({ severity: "success", summary: "Template cloned", life: 3000 });
  } catch {
    toast.add({ severity: "error", summary: "Clone failed", life: 3000 });
  }
}

function confirmDelete(t) {
  confirm.require({
    message: `Delete template "${t.name}"?`,
    header: "Confirm Delete",
    icon: "pi pi-trash",
    acceptClass: "p-button-danger",
    accept: async () => {
      await store.deleteTemplate(t.id);
      toast.add({ severity: "success", summary: "Template deleted", life: 3000 });
    },
  });
}

onMounted(() => store.fetchTemplates());
</script>

<style scoped>
.field-label { @apply block text-sm font-medium text-gray-700 mb-1; }
</style>
