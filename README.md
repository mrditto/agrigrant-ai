# AgriGrant AI

AgriGrant AI is a Streamlit app that helps farmers browse a bundled list of grant opportunities in one place. This repository now supports a safe publishing setup:

- `GitHub Pages` for a public website
- `Streamlit Community Cloud` for the live Python app
- `Streamlit secrets` or environment variables for API keys

## What the app does

The live app reads grant data from `grants_database.json` and shows each opportunity with:

- Grant name
- Agency
- Description
- Maximum funding
- Link to the official grant page

It also includes an optional email input with basic validation.

## Important publishing note

GitHub Pages is a static hosting service. According to GitHub Docs, it publishes HTML, CSS, and JavaScript files from your repository, which means it cannot run this Streamlit app directly. Source: [GitHub Pages docs](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

That means the safe setup is:

1. Publish `docs/index.html` to GitHub Pages as your public homepage.
2. Deploy `app.py` to Streamlit Community Cloud.
3. Store any API keys in Streamlit secrets, not in the repository and not in frontend code.

## Why this is safer for your API

GitHub Pages files are public. If you put an API key into HTML, JavaScript, or a committed config file, visitors can inspect it and copy it.

Streamlit runs server-side, so secrets can stay on the host. Streamlit's docs recommend storing secrets outside the repository, such as in `.streamlit/secrets.toml` locally and in the deployment platform's secret manager in production. Sources:

- [Streamlit secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management)
- [Streamlit Community Cloud secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## Files added for publishing

- `docs/index.html`: public GitHub Pages landing page
- `.github/workflows/pages.yml`: GitHub Actions workflow to deploy the `docs` folder to GitHub Pages
- `.streamlit/secrets.toml.example`: example local secrets file

## How to run locally

```powershell
cd C:\Users\bradl\Documents\GitHub\agrigrant-ai
pip install -r requirements.txt
streamlit run app.py
```

Open:

`http://localhost:8501`

## How to publish safely

### 1. Push this repository to GitHub

Make sure your default branch is `main`, because the included Pages workflow deploys on pushes to `main`.

### 2. Turn on GitHub Pages

In GitHub:

1. Open the repository.
2. Go to `Settings`.
3. Go to `Pages`.
4. Set the source to `GitHub Actions`.

After that, GitHub will publish the `docs` site using `.github/workflows/pages.yml`.

Your site will usually be available at:

`https://YOUR-USERNAME.github.io/agrigrant-ai/`

### 3. Deploy the Streamlit app

Use Streamlit Community Cloud for the real app:

1. Connect your GitHub account at [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create a new app from this repository.
3. Set the main file path to `app.py`.
4. In the app's advanced settings, add any secrets you need.

### 4. Add secrets safely

For local development:

1. Copy `.streamlit/secrets.toml.example`
2. Rename it to `.streamlit/secrets.toml`
3. Put your real API keys there

Do not commit `.streamlit/secrets.toml`. It is already ignored by `.gitignore`.

For deployed apps:

- Add secrets in Streamlit Community Cloud settings
- Do not hardcode them in Python files
- Do not place them in `docs/index.html`

## Before going live

Update these placeholders in `docs/index.html`:

- `https://YOUR-APP.streamlit.app`
- `https://github.com/YOUR-USERNAME/agrigrant-ai`

## Project files

- `app.py`: Streamlit UI
- `grants.py`: grant loading and validation
- `grants_database.json`: bundled grant dataset
- `docs/index.html`: GitHub Pages homepage
- `.github/workflows/pages.yml`: Pages deployment workflow
- `test_app.py` and `test_grants.py`: basic tests

## Security checklist

- Never commit API keys
- Never expose API keys in browser JavaScript
- Keep secrets in Streamlit secrets or environment variables
- Treat GitHub Pages as public-only content
- Use the server-side Streamlit app for any API-backed features
