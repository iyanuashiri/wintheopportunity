<script setup>
import { useAuth } from '../lib/auth'
const { isAuthenticated } = useAuth()
</script>

<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4">
    <div class="text-center">
      <div class="text-6xl">🔍</div>
      <h1 class="mt-4 font-display text-3xl font-bold text-navy-900">Page not found</h1>
      <p class="mt-2 text-slate-500">The page you're looking for doesn't exist.</p>
      <RouterLink
        :to="isAuthenticated ? '/dashboard' : '/'"
        class="mt-6 inline-flex items-center justify-center px-5 py-2.5 rounded-lg bg-navy-900 text-white text-sm font-semibold hover:bg-navy-800 transition"
      >
        Go home
      </RouterLink>
    </div>
  </div>
</template>