<script setup>
import { computed } from 'vue'
import { categoryLabel, deadlineInfo, scoreColor, scorePercent } from '../lib/format'

const props = defineProps({
  opportunity: { type: Object, required: true },
  recommendation: { type: Object, default: null },
})

const deadline = computed(() => deadlineInfo(props.opportunity.deadline))

const deadlineBadgeClass = computed(() => {
  const tones = {
    overdue: 'bg-red-100 text-red-700',
    urgent: 'bg-red-100 text-red-700',
    soon: 'bg-amber-100 text-amber-800',
    normal: 'bg-slate-100 text-slate-600',
  }
  return tones[deadline.value.tone] || tones.normal
})
</script>

<template>
  <RouterLink
    :to="`/opportunities/${opportunity.id}`"
    class="group block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md hover:border-navy-200 transition"
  >
    <div class="flex items-start justify-between gap-4">
      <div class="min-w-0">
        <span class="inline-block rounded-full bg-navy-50 text-navy-700 px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide">
          {{ categoryLabel(opportunity.category) }}
        </span>
        <h3 class="mt-2 font-display text-lg font-semibold text-navy-900 group-hover:text-navy-700 line-clamp-2">
          {{ opportunity.title }}
        </h3>
        <p class="mt-1 text-sm text-slate-500">{{ opportunity.organization_name }}</p>
      </div>

      <div v-if="recommendation" class="flex flex-col items-end shrink-0">
        <span class="font-display text-2xl font-bold" :class="scoreColor(recommendation.relevance_score)">
          {{ scorePercent(recommendation.relevance_score) }}
        </span>
        <span class="text-xs text-slate-400">match</span>
      </div>
    </div>

    <div class="mt-4 flex items-center gap-2">
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="deadlineBadgeClass">
        ⏰ {{ deadline.label }}
      </span>
    </div>

    <p v-if="recommendation?.match_reason" class="mt-4 text-sm text-slate-600 line-clamp-3">
      {{ recommendation.match_reason }}
    </p>
  </RouterLink>
</template>