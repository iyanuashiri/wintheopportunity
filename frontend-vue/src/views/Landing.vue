<script setup>
import { useAuth } from '../lib/auth'

const { isAuthenticated } = useAuth()
</script>

<template>
  <div class="bg-white">
    <!-- Top nav -->
    <header class="bg-navy-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-2">
            <span class="text-2xl">🏆</span>
            <span class="font-display font-bold text-lg tracking-tight">
              Win The <span class="text-gold-400">Opportunity</span>
            </span>
          </div>
          <div class="flex items-center gap-3">
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
          </div>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="bg-navy-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
        <div class="max-w-3xl">
          <p class="inline-flex items-center gap-2 rounded-full bg-navy-800 px-3 py-1 text-xs font-semibold text-gold-300 uppercase tracking-wide">
            AI-powered grant discovery
          </p>
          <h1 class="mt-6 font-display text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight">
            Win the grants your NGO deserves.
          </h1>
          <p class="mt-6 text-lg text-slate-300 leading-relaxed">
            Win The Opportunity discovers funding opportunities matched to your mission,
            extracts the application questions, and helps you craft winning answers — all in one place.
          </p>
          <div class="mt-8 flex flex-col sm:flex-row gap-3">
            <RouterLink
              to="/register"
              class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-gold-500 text-navy-950 font-semibold hover:bg-gold-400 transition"
            >
              Start winning
            </RouterLink>
            <RouterLink
              to="/login"
              class="inline-flex items-center justify-center px-6 py-3 rounded-lg bg-navy-800 text-white font-semibold hover:bg-navy-700 transition"
            >
              Log in
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-16 lg:py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto">
          <h2 class="font-display text-3xl font-bold text-navy-900">Everything you need to win</h2>
          <p class="mt-3 text-slate-500">From discovery to submission, we handle the busywork.</p>
        </div>

        <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="text-3xl">🎯</div>
            <h3 class="mt-4 font-display text-lg font-semibold text-navy-900">Smart recommendations</h3>
            <p class="mt-2 text-sm text-slate-500">
              Opportunities matched to your mission and focus areas, scored by relevance.
            </p>
          </div>
          <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="text-3xl">📋</div>
            <h3 class="mt-4 font-display text-lg font-semibold text-navy-900">Application extraction</h3>
            <p class="mt-2 text-sm text-slate-500">
              We pull the questions from application forms so you can prepare answers in advance.
            </p>
          </div>
          <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="text-3xl">✍️</div>
            <h3 class="mt-4 font-display text-lg font-semibold text-navy-900">Winning answers</h3>
            <p class="mt-2 text-sm text-slate-500">
              Draft, refine, and evaluate your answers with AI feedback before you submit.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="bg-navy-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h2 class="font-display text-3xl font-bold">Ready to win your next grant?</h2>
        <p class="mt-3 text-slate-300">Join NGOs using Win The Opportunity to secure funding.</p>
        <RouterLink
          to="/register"
          class="mt-6 inline-flex items-center justify-center px-6 py-3 rounded-lg bg-gold-500 text-navy-950 font-semibold hover:bg-gold-400 transition"
        >
          Create your account
        </RouterLink>
      </div>
    </section>

    <footer class="bg-navy-950 text-slate-400">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-sm">
        <p>© {{ new Date().getFullYear() }} Win The Opportunity — Helping NGOs win grants.</p>
      </div>
    </footer>
  </div>
</template>