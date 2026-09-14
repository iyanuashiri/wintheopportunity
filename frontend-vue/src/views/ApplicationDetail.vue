<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../lib/api'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { formatDateTime } from '../lib/format'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const application = ref(null)

const sortedQuestions = computed(() => {
  if (!application.value?.questions) return []
  return [...application.value.questions].sort((a, b) => a.order_index - b.order_index)
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get(`/applications/${route.params.id}/`)
    application.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load application.'
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

    <template v-else-if="application">
      <RouterLink to="/applications" class="text-sm font-medium text-navy-700 hover:text-navy-900">
        ← Back to applications
      </RouterLink>

      <div class="mt-4 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div class="flex flex-wrap items-center gap-2">
          <span
            class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
            :class="application.questions_extracted ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-800'"
          >
            {{ application.questions_extracted ? '✓ Questions extracted' : '⚠ No questions' }}
          </span>
          <span class="inline-block rounded-full bg-slate-100 text-slate-600 px-2.5 py-0.5 text-xs font-medium">
            {{ application.mode }}
          </span>
        </div>

        <h1 class="mt-4 font-display text-2xl sm:text-3xl font-bold text-navy-900">
          {{ application.title }}
        </h1>
        <p v-if="application.application_url" class="mt-2 text-sm text-slate-500 break-all">
          {{ application.application_url }}
        </p>

        <!-- Extraction failed notice -->
        <div
          v-if="!application.questions_extracted"
          class="mt-6 rounded-lg bg-amber-50 border border-amber-200 px-4 py-3"
        >
          <p class="text-sm font-medium text-amber-800">We couldn't extract the questions from this form.</p>
          <p v-if="application.extraction_reason" class="mt-1 text-sm text-amber-700">
            {{ application.extraction_reason }}
          </p>
        </div>
      </div>

      <!-- Questions -->
      <div v-if="sortedQuestions.length" class="mt-8 space-y-6">
        <h2 class="font-display text-xl font-semibold text-navy-900">Questions</h2>

        <div
          v-for="(question, idx) in sortedQuestions"
          :key="question.id"
          class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="min-w-0">
              <p class="text-sm text-slate-400">Question {{ idx + 1 }}</p>
              <h3 class="mt-1 font-display text-lg font-semibold text-navy-900">
                {{ question.question_text }}
              </h3>
              <div class="mt-2 flex flex-wrap items-center gap-2 text-xs">
                <span class="rounded-full bg-slate-100 text-slate-600 px-2 py-0.5">{{ question.field_type }}</span>
                <span
                  v-if="question.is_required"
                  class="rounded-full bg-red-50 text-red-600 px-2 py-0.5 font-medium"
                >
                  Required
                </span>
                <span v-if="question.max_characters" class="text-slate-400">
                  Max {{ question.max_characters }} characters
                </span>
                <span v-if="question.max_words" class="text-slate-400">
                  Max {{ question.max_words }} words
                </span>
              </div>
            </div>
          </div>

          <!-- Answers -->
          <div v-if="question.answers?.length" class="mt-4 space-y-3">
            <div
              v-for="answer in question.answers"
              :key="answer.id"
              class="rounded-lg bg-slate-50 border border-slate-200 p-4"
            >
              <div class="flex items-center justify-between">
                <span class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Answer v{{ answer.version }}
                  <span v-if="answer.is_final" class="ml-1 text-emerald-600">· final</span>
                </span>
                <span class="text-xs text-slate-400">{{ formatDateTime(answer.created_at) }}</span>
              </div>
              <p class="mt-2 text-slate-700 whitespace-pre-line">{{ answer.answer_text }}</p>

              <!-- Evaluations -->
              <div v-if="answer.evaluations?.length" class="mt-3 space-y-2">
                <div
                  v-for="evalItem in answer.evaluations"
                  :key="evalItem.id"
                  class="rounded-lg border border-navy-100 bg-navy-50/50 p-3"
                >
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-semibold text-navy-800">AI Evaluation</span>
                    <span class="font-display text-lg font-bold text-navy-800">
                      {{ evalItem.score }}
                    </span>
                  </div>
                  <p class="mt-1 text-sm text-slate-600">{{ evalItem.reasoning }}</p>
                  <p v-if="evalItem.suggestions" class="mt-2 text-sm text-slate-500">
                    <span class="font-medium text-navy-700">Suggestions:</span> {{ evalItem.suggestions }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <p v-else class="mt-4 text-sm text-slate-400 italic">No answer yet.</p>
        </div>
      </div>

      <div v-else-if="!application.questions_extracted" class="mt-8 rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center">
        <div class="text-4xl">🔒</div>
        <p class="mt-4 text-sm text-slate-500 max-w-md mx-auto">
          This application's questions couldn't be extracted automatically. You may need to open the
          form and answer it directly.
        </p>
        <a
          v-if="application.application_url"
          :href="application.application_url"
          target="_blank"
          rel="noopener"
          class="mt-6 inline-flex items-center justify-center px-5 py-2.5 rounded-lg bg-gold-500 text-navy-950 text-sm font-semibold hover:bg-gold-400 transition"
        >
          Open application form →
        </a>
      </div>
    </template>
  </div>
</template>