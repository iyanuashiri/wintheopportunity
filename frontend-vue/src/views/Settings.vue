<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../lib/api'
import PageHeader from '../components/PageHeader.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')

// Onboarding state
const onboarding = ref(false)
const onboardingStep = ref('')
const onboardingSteps = [
  'Scraping opportunities…',
  'Matching opportunities to your organization…',
  'Recommending the best matches…',
  'Extracting application questions…',
]

const form = ref({
  org_name: '',
  website: '',
  mission_statement: '',
  focus_areas: '',
  target_beneficiaries: '',
  background_info: '',
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/organizations/me/')
    form.value = {
      org_name: data.org_name || '',
      website: data.website || '',
      mission_statement: data.mission_statement || '',
      focus_areas: data.focus_areas || '',
      target_beneficiaries: data.target_beneficiaries || '',
      background_info: data.background_info || '',
    }
  } catch (err) {
    // 404 means no profile yet — that's fine, show empty form
    if (err.response?.status !== 404) {
      error.value = err.response?.data?.detail || 'Failed to load your organization profile.'
    }
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    await api.put('/organizations/me/', form.value)
    success.value = 'Your organization profile was saved.'
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save your profile.'
  } finally {
    saving.value = false
  }
}

async function startOnboarding() {
  saving.value = true
  error.value = ''
  success.value = ''
  onboarding.value = true

  try {
    // 1. Save the profile first
    await api.put('/organizations/me/', form.value)

    // 2. Trigger the agent pipeline (fast demo endpoint)
    const recommendPromise = api.post('/onboarding/recommend/')

    // 3. Show a timed loading sequence so the demo video captures the steps
    for (const step of onboardingSteps) {
      onboardingStep.value = step
      await new Promise((resolve) => setTimeout(resolve, 1800))
    }

    // 4. Wait for the (fast) backend call to finish
    await recommendPromise

    // 5. Redirect to the recommendations dashboard
    router.push('/dashboard')
  } catch (err) {
    onboarding.value = false
    error.value = err.response?.data?.detail || 'Something went wrong while generating your recommendations.'
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <PageHeader
      title="Organization Profile"
      subtitle="Tell us about your organization so we can match the right opportunities to your mission."
    />

    <LoadingSpinner v-if="loading" />

    <!-- Onboarding loading sequence -->
    <div v-else-if="onboarding" class="rounded-2xl border border-slate-200 bg-white p-10 shadow-sm text-center">
      <div class="mx-auto w-16 h-16 rounded-full bg-navy-50 flex items-center justify-center">
        <svg class="animate-spin h-8 w-8 text-navy-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>
      <h2 class="mt-6 font-display text-xl font-semibold text-navy-900">Setting up your recommendations</h2>
      <p class="mt-2 text-slate-500">Our agents are working in the background to find the best opportunities for you.</p>
      <p class="mt-6 font-medium text-navy-700">{{ onboardingStep }}</p>
      <div class="mt-4 flex justify-center gap-1.5">
        <span class="h-1.5 w-1.5 rounded-full bg-navy-300 animate-pulse"></span>
        <span class="h-1.5 w-1.5 rounded-full bg-navy-300 animate-pulse" style="animation-delay: 0.2s"></span>
        <span class="h-1.5 w-1.5 rounded-full bg-navy-300 animate-pulse" style="animation-delay: 0.4s"></span>
      </div>
    </div>

    <form v-else @submit.prevent="save" class="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <div v-if="error" class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
        {{ error }}
      </div>
      <div v-if="success" class="mb-4 rounded-lg bg-emerald-50 border border-emerald-200 px-4 py-3 text-sm text-emerald-700">
        {{ success }}
      </div>

      <label class="block">
        <span class="text-sm font-medium text-slate-700">Organization name</span>
        <input
          v-model="form.org_name"
          type="text"
          required
          placeholder="e.g. GreenRoots Youth Initiative"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        />
      </label>

      <label class="block mt-4">
        <span class="text-sm font-medium text-slate-700">Website</span>
        <input
          v-model="form.website"
          type="url"
          placeholder="https://yourngo.org"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        />
      </label>

      <label class="block mt-4">
        <span class="text-sm font-medium text-slate-700">Mission statement</span>
        <textarea
          v-model="form.mission_statement"
          rows="3"
          placeholder="Describe your organization's mission…"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        ></textarea>
      </label>

      <label class="block mt-4">
        <span class="text-sm font-medium text-slate-700">Focus areas</span>
        <textarea
          v-model="form.focus_areas"
          rows="2"
          placeholder="e.g. Climate, Education, Animal Welfare"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        ></textarea>
      </label>

      <label class="block mt-4">
        <span class="text-sm font-medium text-slate-700">Target beneficiaries</span>
        <textarea
          v-model="form.target_beneficiaries"
          rows="2"
          placeholder="Who do you serve?"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        ></textarea>
      </label>

      <label class="block mt-4">
        <span class="text-sm font-medium text-slate-700">Background info</span>
        <textarea
          v-model="form.background_info"
          rows="3"
          placeholder="Any additional context about your organization…"
          class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
        ></textarea>
      </label>

      <div class="mt-6 flex flex-col sm:flex-row gap-3">
        <button
          type="button"
          @click="startOnboarding"
          :disabled="saving"
          class="rounded-lg bg-gold-500 px-6 py-2.5 text-sm font-semibold text-navy-950 hover:bg-gold-400 disabled:opacity-60 transition"
        >
          {{ saving ? 'Working…' : 'Get my recommendations' }}
        </button>
        <button
          type="submit"
          :disabled="saving"
          class="rounded-lg border border-slate-300 px-6 py-2.5 text-sm font-semibold text-navy-900 hover:bg-slate-50 disabled:opacity-60 transition"
        >
          Save profile
        </button>
      </div>
    </form>
  </div>
</template>