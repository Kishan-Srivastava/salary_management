# Deploy online (for interviewers / reviewers)

Host the **API** and **Streamlit dashboard** so anyone can open them in a browser.

---

## Option A — Render (recommended: API + UI together)

1. Push `main` to GitHub (already done if you merged).
2. Open **[Deploy to Render](https://render.com/deploy?repo=https://github.com/Kishan-Srivastava/salary_management)**.
3. Sign in with GitHub and approve the blueprint (`render.yaml`).
4. Wait for both services to go **Live** (~5–10 min first build).
5. Copy URLs from the Render dashboard:
   - **salary-management-api** → Swagger: `{API_URL}/docs`
   - **salary-management-ui** → Dashboard: `{UI_URL}`

The API auto-seeds **500** demo employees on first start (`SEED_DEMO_COUNT`).

**Note:** Free Render services sleep after inactivity; first visit may take ~1 minute to wake up.

---

## Option B — Streamlit Community Cloud (UI only) + Render (API)

### API on Render

1. Create a **Web Service** from the repo with:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Env:** `PYTHONPATH=.`, `SEED_DEMO_COUNT=500`, `DATABASE_URL=sqlite:////tmp/salary.db`
2. Copy the service URL (e.g. `https://salary-management-api.onrender.com`).

### UI on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. **New app** → Repository: `Kishan-Srivastava/salary_management`, branch `main`, main file `streamlit_app.py`.
3. **Secrets** (paste, replace with your API URL):

```toml
API_BASE_URL = "https://salary-management-api.onrender.com"
```

4. Deploy and copy the `*.streamlit.app` URL.

---

## After deploy — update README links

Edit `README.md` **Live demo** table with your real URLs, then commit:

```markdown
| **Dashboard** | https://salary-management-ui.onrender.com |
| **API (Swagger)** | https://salary-management-api.onrender.com/docs |
```

---

## Verify deployment

```bash
curl https://YOUR-API.onrender.com/health
curl https://YOUR-API.onrender.com/api/v1/health
```

Expected: `"app_version": "1.0.0"`, `"api_version": "v1"`.
