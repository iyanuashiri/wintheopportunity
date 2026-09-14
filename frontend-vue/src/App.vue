<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from './lib/auth'

const route = useRoute()
const router = useRouter()
const { isAuthenticated, logout } = useAuth()

const showNav = computed(() => {
  // Hide the full nav on the landing page (it has its own hero nav)
  return route.name !== 'landing'
})

function handleLogout() {
  logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <header v-if="showNav" class="bg-navy-900 text-white shadow-md sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <RouterLink to="/dashboard" class="flex items-center gap-2">
            <span class="text-2xl">🏆</span>
            <span class="font-display font-bold text-lg tracking-tight">
              Win The <span class="text-gold-400">Opportunity</span>
            </span>
          </RouterLink>

          <nav v-if="isAuthenticated" class="hidden md:flex items-center gap-1">
            <RouterLink
              to="/dashboard"
              class="px-3 py-2 rounded-md text-sm font-medium hover:bg-navy-800 transition"
              active-class="bg-navy-800 text-gold-300"
            >
              Dashboard
            </RouterLink>
            <RouterLink
              to="/applications"
              class="px-3 py-2 rounded-md text-sm font-medium hover:bg-navy-800 transition"
              active-class="bg-navy-800 text-gold-300"
            >
              Applications
            </RouterLink>
            <RouterLink
              to="/settings"
              class="px-3 py-2 rounded-md text-sm font-medium hover:bg-navy-800 transition"
              active-class="bg-navy-800 text-gold-300"
            >
              Settings
            </RouterLink>
          </nav>

          <div class="flex items-center gap-3">
            <template v-if="isAuthenticated">
              <button
                @click="handleLogout"
                class="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:bg-navy-800 hover:text-white transition"
              >
                Log out
              </button>
            </template>
            <template v-else>
              <RouterLink
                to="/login"
                class="px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:bg-navy-800 transition"
              >
                Log in
              </RouterLink>
              <RouterLink
                to="/register"
                class="px-4 py-2 rounded-md text-sm font-semibold bg-gold-500 text-navy-950 hover:bg-gold-400 transition"
              >
                Get started
              </RouterLink>
            </template>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer v-if="showNav" class="bg-navy-950 text-slate-400">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-sm">
        <p>© {{ new Date().getFullYear() }} Win The Opportunity — Helping NGOs win grants.</p>
      </div>
    </footer>
  </div>
</template>
