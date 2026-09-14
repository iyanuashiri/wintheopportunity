<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../lib/api'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { categoryLabel, deadlineInfo, formatDate } from '../lib/format'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const opportunity = ref(null)
const application = ref(null)

const deadline = computed(() => deadlineInfo(opportunity.value?.deadline))

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get(`/opportunities/${route.params.id}/`)
    opportunity.value = data

    // Find the agent-created application for this opportunity (if any)
    try {
      const { data: apps } = await api.get('/applications/', { params: { limit: 100 } })
      application.value = apps.find((a) => a.opportunity_id === data.id) || null
    } catch {
      application.value = null
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load opportunity.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <LoadingSpinner v-if="loading" />

    <div v-else-if="error" class="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
      {{ error }}
    </div>

    <template v-else-if="opportunity">
      <RouterLink to="/dashboard" class="text-sm font-medium text-navy-700 hover:text-navy-900">
        ← Back to dashboard
      </RouterLink>

      <div class="mt-4 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div class="flex flex-wrap items-center gap-2">
          <span class="inline-block rounded-full bg-navy-50 text-navy-700 px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide">
            {{ categoryLabel(opportunity.category) }}
          </span>
          <span class="inline-block rounded-full bg-slate-100 text-slate-600 px-2.5 py-0.5 text-xs font-medium">
            ⏰ {{ deadline.label }}
          </span>
        </div>

        <h1 class="mt-4 font-display text-2xl sm:text-3xl font-bold text-navy-900">
          {{ opportunity.title }}
        </h1>
        <p class="mt-2 text-slate-500">
          {{ opportunity.organization_name }}
          <a
            v-if="opportunity.organization_url"
            :href="opportunity.organization_url"
            target="_blank"
            rel="noopener"
            class="text-navy-700 hover:underline"
          >
            · Visit organization
          </a>
        </p>

        <div class="mt-6 flex flex-col sm:flex-row gap-3">
          <a
            v-if="opportunity.application_url"
            :href="opportunity.application_url"
            target="_blank"
            rel="noopener"
            class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-gold-500 text-navy-950 font-semibold hover:bg-gold-400 transition"
          >
            Apply now →
          </a>
          <RouterLink
            v-if="application"
            :to="`/applications/${application.id}`"
            class="inline-flex items-center justify-center px-6 py-3 rounded-lg border border-slate-300 text-navy-900 font-semibold hover:bg-slate-50 transition"
          >
            View application
          </RouterLink>
        </div>

        <dl class="mt-8 grid gap-4 sm:grid-cols-2">
          <div class="rounded-lg bg-slate-50 p-4">
            <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">Deadline</dt>
            <dd class="mt-1 font-medium text-navy-900">{{ formatDate(opportunity.deadline) }}</dd>
          </div>
          <div class="rounded-lg bg-slate-50 p-4">
            <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">Start date</dt>
            <dd class="mt-1 font-medium text-navy-900">{{ formatDate(opportunity.start_date) }}</dd>
          </div>
        </dl>

        <div v-if="opportunity.description" class="mt-8">
          <h2 class="font-display text-lg font-semibold text-navy-900">About this opportunity</h2>
          <p class="mt-2 text-slate-600 leading-relaxed whitespace-pre-line">{{ opportunity.description }}</p>
        </div>

        <div v-if="opportunity.eligibility_criteria" class="mt-8">
          <h2 class="font-display text-lg font-semibold text-navy-900">Eligibility</h2>
          <p class="mt-2 text-slate-600 leading-relaxed whitespace-pre-line">{{ opportunity.eligibility_criteria }}</p>
        </div>
      </div>
    </template>
  </div>
</template>