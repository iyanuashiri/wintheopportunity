<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../lib/api'
import PageHeader from '../components/PageHeader.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import OpportunityCard from '../components/OpportunityCard.vue'

const loading = ref(true)
const error = ref('')
const items = ref([]) // [{ recommendation, opportunity }]

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data: recommendations } = await api.get('/recommendations/')
    const enriched = []
    for (const rec of recommendations) {
      try {
        const { data: opportunity } = await api.get(`/opportunities/${rec.opportunity_id}/`)
        enriched.push({ recommendation: rec, opportunity })
      } catch {
        // Skip recommendations whose opportunity can't be fetched
      }
    }
    items.value = enriched
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load recommendations.'
  } finally {
    loading.value = false
  }
}

const sortedItems = computed(() => {
  return [...items.value].sort(
    (a, b) => (b.recommendation.relevance_score || 0) - (a.recommendation.relevance_score || 0),
  )
})

onMounted(load)
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <PageHeader
      title="Recommended Opportunities"
      subtitle="Funding opportunities matched to your mission, ranked by relevance."
    />

    <!-- First-recommendations welcome banner -->
    <div v-if="!loading && sortedItems.length > 0" class="mb-8 rounded-xl border border-gold-200 bg-gold-50 px-6 py-4">
      <div class="flex items-start gap-3">
        <span class="text-2xl">🎉</span>
        <div>
          <h3 class="font-display font-semibold text-navy-900">Here are your first recommendations!</h3>
          <p class="mt-1 text-sm text-slate-600">
            We've matched these opportunities to your organization. New recommendations will be added daily.
          </p>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="loading" text="Loading your recommendations…" />

    <div v-else-if="error" class="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
      {{ error }}
    </div>

    <div v-else-if="sortedItems.length === 0" class="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center">
      <div class="text-4xl">🎯</div>
      <h3 class="mt-4 font-display text-lg font-semibold text-navy-900">No recommendations yet</h3>
      <p class="mt-2 text-sm text-slate-500 max-w-md mx-auto">
        Our recommender is still matching opportunities to your organization. Check back soon, or
        make sure your organization profile is complete in Settings.
      </p>
      <RouterLink
        to="/settings"
        class="mt-6 inline-flex items-center justify-center px-5 py-2.5 rounded-lg bg-navy-900 text-white text-sm font-semibold hover:bg-navy-800 transition"
      >
        Complete your profile
      </RouterLink>
    </div>

    <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <OpportunityCard
        v-for="item in sortedItems"
        :key="item.recommendation.id"
        :opportunity="item.opportunity"
        :recommendation="item.recommendation"
      />
    </div>
  </div>
</template>