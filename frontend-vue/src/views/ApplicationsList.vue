<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../lib/api'
import PageHeader from '../components/PageHeader.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { formatDate } from '../lib/format'

const loading = ref(true)
const error = ref('')
const applications = ref([])

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/applications/', { params: { limit: 100 } })
    applications.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <PageHeader
      title="Applications"
      subtitle="Your Commonly Answered Questions backlog — every application and its extracted questions."
    />

    <LoadingSpinner v-if="loading" />

    <div v-else-if="error" class="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
      {{ error }}
    </div>

    <div v-else-if="applications.length === 0" class="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center">
      <div class="text-4xl">📋</div>
      <h3 class="mt-4 font-display text-lg font-semibold text-navy-900">No applications yet</h3>
      <p class="mt-2 text-sm text-slate-500 max-w-md mx-auto">
        Applications will appear here once the scraper extracts questions from recommended opportunities.
      </p>
    </div>

    <div v-else class="space-y-4">
      <RouterLink
        v-for="app in applications"
        :key="app.id"
        :to="`/applications/${app.id}`"
        class="group block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md hover:border-navy-200 transition"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <h3 class="font-display text-lg font-semibold text-navy-900 group-hover:text-navy-700 line-clamp-1">
              {{ app.title }}
            </h3>
            <p class="mt-1 text-sm text-slate-500">
              {{ app.questions_count }} question{{ app.questions_count === 1 ? '' : 's' }}
              <span v-if="app.application_url" class="text-slate-400">· {{ app.application_url }}</span>
            </p>
          </div>
          <div class="flex flex-col items-end shrink-0 gap-1">
            <span
              class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
              :class="app.questions_extracted ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-800'"
            >
              {{ app.questions_extracted ? '✓ Questions extracted' : '⚠ No questions' }}
            </span>
            <span class="text-xs text-slate-400">{{ formatDate(app.created_at) }}</span>
          </div>
        </div>

        <p v-if="!app.questions_extracted && app.extraction_reason" class="mt-3 text-sm text-slate-600">
          {{ app.extraction_reason }}
        </p>
      </RouterLink>
    </div>
  </div>
</template>