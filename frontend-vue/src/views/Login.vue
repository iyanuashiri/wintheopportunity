<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../lib/auth'

const route = useRoute()
const router = useRouter()
const { login, loading } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    await login(email.value, password.value)
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid email or password. Please try again.'
  }
}
</script>

<template>
  <div class="min-h-[80vh] flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <span class="text-4xl">🏆</span>
        <h1 class="mt-3 font-display text-2xl font-bold text-navy-900">Welcome back</h1>
        <p class="mt-1 text-slate-500">Log in to your Win The Opportunity account</p>
      </div>

      <form @submit.prevent="handleSubmit" class="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div v-if="error" class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
          {{ error }}
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Email</span>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            placeholder="you@ngo.org"
            class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
          />
        </label>

        <label class="block mt-4">
          <span class="text-sm font-medium text-slate-700">Password</span>
          <input
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
            placeholder="••••••••"
            class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-navy-500 focus:ring-2 focus:ring-navy-200 outline-none"
          />
        </label>

        <button
          type="submit"
          :disabled="loading"
          class="mt-6 w-full rounded-lg bg-navy-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-navy-800 disabled:opacity-60 transition"
        >
          {{ loading ? 'Logging in…' : 'Log in' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-500">
        Don't have an account?
        <RouterLink to="/register" class="font-semibold text-navy-700 hover:text-navy-900">
          Create one
        </RouterLink>
      </p>
    </div>
  </div>
</template>