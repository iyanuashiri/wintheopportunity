# Edge Cases & Future Work

This file tracks edge cases and future features that are **not yet implemented**.
They are documented here so the design stays clear without expanding the current
scope.

## 1. User submits an `application_url` directly (no questions, no images)

**Status:** Not implemented (may extend feature scope)

**Scenario:**
- The user creates an Application by submitting just an `application_url`.
- The Application has **no questions** and **no images**.
- This is similar to Agent 4's task — the user needs to provide screenshots
  (or the URL needs scraping) to extract the questions.

**Why it's deferred:**
- It overlaps with Agent 4 (Vision/Screenshot) and Agent 3 (URL scraper).
- Implementing it now would extend the feature scope beyond the current
  cron-driven Agent 3 flow.

**Possible future approach:**
- When a user submits an `application_url` with no questions, trigger a
  scraping attempt (Agent 3) or prompt the user to upload screenshots
  (Agent 4).

## 2. Agent 4: Vision / Screenshot Agent

**Status:** Not implemented

**Scenario:**
- The application form is behind authentication.
- The user uploads screenshots of the form (one at a time via the
  `POST /applications/{id}/images/` endpoint).
- Agent 4 extracts questions from the images and completes the Application.

**Data model:** The `Image` model already exists (in `application.py`).

## 3. Agent 5: Application Answering Agent

**Status:** Not implemented

**Scenario:**
- Uses RAG over the NGO's "Commonly Answered Questions" backlog + NGO context
  to draft tailored answers.

## 4. Agent 6: Analysis & Evaluation Agent

**Status:** Not implemented

**Scenario:**
- Evaluates answer quality against opportunity expectations, scoring answers
  and providing improvement feedback across iterations.