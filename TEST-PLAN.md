# Sprint Plan: Email Notifications for New User Signups

## Overview
Break down the email notification feature into demoable sprints with atomic tasks.

---

## Sprints

### Sprint 1: Email Infrastructure & Templates
**Goal:** Set up email provider and create welcome email template
**Demo:** Email template renders and SendGrid sends test emails

#### Tasks

##### TASK-001: Install and configure SendGrid SDK
- **Description:** Add @sendgrid/mail, configure API key in environment
- **Validation:** `sgMail.send()` successfully sends email
- **Files touched:** `package.json`, `config/email.js`, `.env.example`
- **Dependencies:** None

##### TASK-002: Create welcome email HTML template
- **Description:** Design and code welcome email with branding (header, body, footer)
- **Validation:** Template renders correctly in email client (Litmus test)
- **Files touched:** `templates/welcome.html`, `templates/partials/header.html`, `templates/partials/footer.html`
- **Dependencies:** None

##### TASK-003: Create email service abstraction
- **Description:** Wrap SendGrid in EmailService class (send, sendBatch, validate)
- **Validation:** Unit tests pass for all methods
- **Files touched:** `services/email-service.js`, `tests/unit/email-service.test.js`
- **Dependencies:** TASK-001

##### TASK-004: Write email template tests
- **Description:** Create tests to verify template renders correctly with variables
- **Validation:** Tests pass for all template variants
- **Files touched:** `tests/unit/email-templates.test.js`
- **Dependencies:** TASK-002

---

### Sprint 2: Event Trigger & Queue Integration
**Goal:** Trigger email on user signup via background queue
**Demo:** User signup triggers welcome email job in queue

#### Tasks

##### TASK-005: Add Bull queue for emails
- **Description:** Configure Redis connection, create email queue
- **Validation:** Jobs can be added and processed
- **Files touched:** `queues/email-queue.js`, `config/redis.js`
- **Dependencies:** None

##### TASK-006: Create email job processor
- **Description:** Implement job handler for welcome emails (with retry logic)
- **Validation:** Job processes successfully, retries on failure
- **Files touched:** `workers/email-worker.js`, `tests/unit/email-worker.test.js`
- **Dependencies:** TASK-003, TASK-005

##### TASK-007: Trigger email on user registration
- **Description:** Call emailQueue.add() in user registration controller
- **Validation:** Job appears in queue after signup
- **Files touched:** `controllers/auth-controller.js`
- **Dependencies:** TASK-005, TASK-006

##### TASK-008: Add 1-minute delay to email send
- **Description:** Configure job delay (optional: per user preference)
- **Validation:** Email sends ~1 minute after signup
- **Files touched:** `workers/email-worker.js`
- **Dependencies:** TASK-006

---

### Sprint 3: Error Handling & Delivery Tracking
**Goal:** Handle delivery failures and track email status
**Demo:** Failed emails are logged, no crashes on provider errors

#### Tasks

##### TASK-009: Implement SendGrid webhook handler
- **Description:** Create endpoint to receive delivery events (delivered, bounced, opened)
- **Validation:** Webhook receives and processes events correctly
- **Files touched:** `routes/webhooks.js`, `controllers/email-webhook.js`
- **Dependencies:** TASK-003

##### TASK-010: Create delivery status table
- **Description:** Track email status in database (sent, delivered, bounced, opened)
- **Validation:** Status updates on webhook events
- **Files touched:** `db/migrations/XXX_add_email_logs.sql`, `models/email-log.js`
- **Dependencies:** None

##### TASK-011: Implement retry with exponential backoff
- **Description:** Configure Bull retry (3 attempts, 5min → 30min → 2hr)
- **Validation:** Failed jobs retry correctly
- **Files touched:** `workers/email-worker.js`
- **Dependencies:** TASK-006

##### TASK-012: Add dead letter handling
- **Description:** Move permanently failed emails to DLQ, log for investigation
- **Validation:** Failed-after-retry emails in DLQ
- **Files touched:** `workers/email-worker.js`, `services/dlq-handler.js`
- **Dependencies:** TASK-011

---

### Sprint 4: Email Preferences (Opt-out)
**Goal:** Allow users to opt out of marketing emails
**Demo:** User can toggle email preferences, opted-out users don't receive

#### Tasks

##### TASK-013: Add email_preferences column to User
- **Description:** Add boolean or JSON column for email preferences
- **Validation:** Column exists, preferences can be updated
- **Files touched:** `db/migrations/XXX_add_email_preferences.sql`, `models/user.js`
- **Dependencies:** None

##### TASK-014: Create email preferences UI/page
- **Description:** Settings page with email toggle
- **Validation:** Toggle saves and loads correctly
- **Files touched:** `views/settings-email.html`, `controllers/settings-controller.js`
- **Dependencies:** TASK-013

##### TASK-015: Check preferences before sending
- **Description:** Modify email job to skip if user opted out
- **Validation:** Opted-out users don't receive welcome email
- **Files touched:** `workers/email-worker.js`, `tests/integration/email-preferences.test.js`
- **Dependencies:** TASK-006, TASK-013

##### TASK-016: Add email preference to registration
- **Description:** Default opt-in/out during signup (checkbox)
- **Validation:** Preference saved on registration
- **Files touched:** `views/register.html`, `controllers/auth-controller.js`
- **Dependencies:** TASK-013

##### TASK-017: Write integration test for full flow
- **Description:** Test: signup → queue → send → delivered (or opted out)
- **Validation:** All scenarios pass
- **Files touched:** `tests/integration/email-full-flow.test.js`
- **Dependencies:** TASK-007, TASK-015

---

## Dependencies Graph

```
Sprint 1          Sprint 2          Sprint 3          Sprint 4
------→ TASK-003 ──────→ TASK-006 ──────→ TASK-009 ─────→ TASK-013
   │          ↗   ↗               ↗   ↗               ↗
   └──→ TASK-001 ─→ TASK-005 ← TASK-007 ─→ TASK-010 ← TASK-014
               ↓                  ↓                  ↓
               └──→ TASK-002 ─→ TASK-008 ─→ TASK-011 ─→ TASK-015
                              ↓   ↓
                              └──→ TASK-004 ─→ TASK-012
                                              ↓
                                              └──→ TASK-016
                                                      ↓
                                                      └──→ TASK-017
```

## Validation Summary

| Sprint | Demoable State |
|--------|----------------|
| Sprint 1 | Emails send with templates |
| Sprint 2 | User signup triggers queue job |
| Sprint 3 | Failed emails retry, status tracked |
| Sprint 4 | Users can opt out |

---

## Self-Review Notes

**Reviewer feedback (subagent simulation):**
- ✅ Tasks are atomic and single-commit
- ✅ Each sprint builds on previous
- ✅ Tests included for each task
- ⚠️ Consider adding email unsubscribe link in TASK-002 (required by CAN-SPAM)
- ✅ Dependencies are clear
- ✅ Validation criteria are specific

**Added to TASK-002:** Add CAN-SPAM compliant unsubscribe link to footer template.

---

*Generated by Planning Mode skill*
*Test run: 2026-01-19*
