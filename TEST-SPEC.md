# Feature: Email Notifications for New User Signups

## Requirements
- Send welcome email within 1 minute of signup
- Email template with branding
- Handle delivery failures gracefully  
- Support email preferences (opt-out)

## Context
- App uses Node.js/Express
- Database: PostgreSQL with User table
- Email provider: SendGrid
- Background jobs: Bull queue (Redis)
