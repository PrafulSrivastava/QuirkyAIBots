**Project Overview**

This repository runs two services via Docker Compose:

1. **MonitoringBot** – a GitHub ProBot–based bot (directory: `monitoring_bot`).
2. **Assistant** – a CREW-AI framework–based LLM model (directory: `assistant`).

Both services require environment variables configured via `.env` files. To keep secrets out of the repository, `.env` files have been removed. Follow the instructions below to set them up.

---

## 1. Prerequisites

* Docker & Docker Compose installed on your machine.
* A GitHub App created for the MonitoringBot (with App ID, private key, and webhook secret).
* A Smee.io or similar webhook proxy URL (optional for local development).
* A Gemini API key (or equivalent) for the Assistant.

---

## 2. Environment File

Create .env in the root directory based on the templates below.

```dotenv
# GitHub App identifier (integer)
APP_ID=YOUR_GITHUB_APP_ID

# The private key for your GitHub App (PEM format; use \n for newlines)
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...your key...\n-----END RSA PRIVATE KEY-----"

# Webhook secret configured in your GitHub App
WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET

# Smee.io or other webhook proxy URL for local testing
WEBHOOK_PROXY_URL=https://smee.io/YOUR_UNIQUE_PATH

# (Optional OAuth settings for GitHub App installation)
GITHUB_CLIENT_ID=YOUR_CLIENT_ID
GITHUB_CLIENT_SECRET=YOUR_CLIENT_SECRET

# LLM model identifier (e.g. Gemini Flash)
MODEL=gemini/gemini-2.0-flash-001

# API key for your LLM provider (e.g. Gemini)
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

```

> **Tip:** Store your API keys securely and do not commit them to version control.

---

## 3. Docker Compose

At the root of the repository, you have a `docker-compose.yml` that references both services. It will automatically load each `.env` file from the respective folder.

To build and start both services:

```bash
docker-compose up --build
```

## 4. Configure the GitHub App on Your Repository

After your services are running, you need to install and configure the GitHub App so it can respond to events in your target repository. Follow these steps (based on the Probot docs):

1. **Install the GitHub App**:

   * In your browser, go to your GitHub App’s settings page on GitHub.com.
   * Click **Install App** → **Install** next to the repository (or organization) where you want the bot to run.

2. **Set up Webhook URL**:

   * If you’re using a webhook proxy (e.g., Smee.io), copy your proxy URL (e.g., `https://smee.io/YOUR_UNIQUE_PATH`).
   * In your GitHub App settings, under **Webhook URL**, paste this proxy URL (or your public server endpoint if deployed).
   * Ensure that **Webhook secret** matches the `WEBHOOK_SECRET` in `.env`.

3. **Configure Permissions & Events**:

   * In the App settings, grant **Repository permissions** (e.g., **Issues: Read & Write**, **Pull requests: Read & Write**) as your bot requires.
   * Under **Subscribe to events**, select all relevant events (e.g., **Pull request**, **Issues**, **Push**).
   * Click **Save changes**.

4. **Verify the Setup**:

   * Create a test issue or PR in the installed repo.
   * Watch your `MonitoringBot` service logs for incoming webhook deliveries and bot activity.

---

## 5. Permissions needed for the bot

Permissions must be populated in app.yml.

```bash
default_events:
  - issues
  - pull_request
  - pull_request_review
  - pull_request_review_comment

default_permissions:
  issues: write
  metadata: read
  pull_requests: write
```

---
