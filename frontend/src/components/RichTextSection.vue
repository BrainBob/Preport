<template>
  <div class="bg-white rounded-xl border border-gray-200">
    <div class="px-4 py-2.5 border-b border-gray-100 flex items-center justify-between">
      <span class="text-sm font-semibold text-gray-700">{{ label }}</span>
      <div v-if="editor" class="flex gap-0.5">
        <button
          v-for="btn in toolbarButtons"
          :key="btn.action"
          @click="btn.fn()"
          :class="['toolbar-btn', { active: btn.isActive?.() }]"
          type="button"
          v-tooltip="btn.tooltip"
        >
          <i :class="['pi', btn.icon, 'text-xs']" />
        </button>
      </div>
    </div>
    <EditorContent :editor="editor" class="prose prose-sm max-w-none p-4 min-h-[120px] focus-within:outline-none" />
  </div>
</template>

<script setup>
import { watch, onBeforeUnmount } from "vue";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";

const props = defineProps({
  modelValue: { type: String, default: "" },
  label: { type: String, required: true },
});
const emit = defineEmits(["update:modelValue"]);

const editor = useEditor({
  content: props.modelValue,
  extensions: [StarterKit],
  onUpdate({ editor }) {
    emit("update:modelValue", editor.getHTML());
  },
});

watch(
  () => props.modelValue,
  (val) => {
    if (editor.value && editor.value.getHTML() !== val) {
      editor.value.commands.setContent(val, false);
    }
  }
);

const toolbarButtons = [
  { action: "bold", icon: "pi-bold", tooltip: "Bold", fn: () => editor.value?.chain().focus().toggleBold().run(), isActive: () => editor.value?.isActive("bold") },
  { action: "italic", icon: "pi-italic", tooltip: "Italic", fn: () => editor.value?.chain().focus().toggleItalic().run(), isActive: () => editor.value?.isActive("italic") },
  { action: "code", icon: "pi-code", tooltip: "Inline Code", fn: () => editor.value?.chain().focus().toggleCode().run(), isActive: () => editor.value?.isActive("code") },
  { action: "codeBlock", icon: "pi-align-left", tooltip: "Code Block", fn: () => editor.value?.chain().focus().toggleCodeBlock().run(), isActive: () => editor.value?.isActive("codeBlock") },
  { action: "bulletList", icon: "pi-list", tooltip: "Bullet List", fn: () => editor.value?.chain().focus().toggleBulletList().run(), isActive: () => editor.value?.isActive("bulletList") },
];

onBeforeUnmount(() => editor.value?.destroy());
</script>

<style scoped>
.toolbar-btn {
  @apply w-6 h-6 flex items-center justify-center rounded text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors;
}
.toolbar-btn.active {
  @apply text-indigo-600 bg-indigo-50;
}
</style>
