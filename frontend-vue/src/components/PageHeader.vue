<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="mb-8">
    <h1 class="font-display text-2xl sm:text-3xl font-bold text-navy-900">{{ title }}</h1>
    <p v-if="subtitle" class="mt-1 text-slate-500">{{ subtitle }}</p>
  </div>
</template>