# 🚀 Deploy SAIL Digital Twin to Streamlit Community Cloud

> **Goal:** Get a permanent public URL like `https://sail-digital-twin.streamlit.app`
> that anyone (including the ICC Grand Jury) can access 24×7.
>
> **Total time:** ~15 minutes for the first deployment.

---

## 📋 Prerequisites (one-time, 5 minutes)

| Account / Tool | Where | Cost |
|---|---|---|
| **GitHub account** | [github.com](https://github.com) | Free |
| **Git installed** | [git-scm.com/downloads](https://git-scm.com/downloads) | Free |
| **Streamlit Cloud account** | [share.streamlit.io](https://share.streamlit.io) (sign in with GitHub) | Free |

---

## 🎯 STEP 1 — Unzip the Project Locally

Unzip `sail-digital-twin-github.zip` somewhere on your laptop:

```bash
unzip sail-digital-twin-github.zip
cd sail-digital-twin-github
```

Verify the structure:

```
sail-digital-twin-github/
├── .gitignore                  ← git ignore rules
├── .streamlit/
│   └── config.toml             ← SAIL brand theming
├── README.md                   ← project overview
├── DEPLOYMENT.md               ← this file
├── requirements.txt            ← trimmed Python deps
├── runtime.txt                 ← Python 3.11 pin
├── models/                     ← 8 pre-trained .pkl files (6.6 MB)
├── data/                       ← 10 Parquet files per-period (~5 MB)
├── streamlit_app/              ← the actual app
│   ├── app.py                  ← entry point
│   ├── pages/                  ← 5 multi-page files
│   └── utils/                  ← styling + data loader
├── notebooks/                  ← Jupyter (not executed in cloud, docs only)
└── docs/TUTORIAL.md
```

Quick sanity check:

```bash
ls models/*.pkl | wc -l         # should be 8
ls data/*.parquet | wc -l        # should be 10
```

---

## 🎯 STEP 2 — Create a GitHub Repository

### 2.1 — On the GitHub website

1. Go to [github.com](https://github.com) → click the **+** icon (top right) → **New repository**
2. Fill the form:
   - **Repository name:** `sail-digital-twin` (or any name you prefer)
   - **Description:** _"AI-Assisted Stoichiometric Optimization — SAIL Digital Twin for ICC Awards 2026"_
   - **Visibility:** ✅ **Public** *(required for free Streamlit Cloud deployment; Private requires Streamlit Teams tier)*
   - **Do NOT** tick "Add a README file" — we already have one
   - **Do NOT** add a `.gitignore` — we already have one
3. Click **Create repository**

GitHub will show a setup page. Copy the repo URL (looks like `https://github.com/YOUR_USERNAME/sail-digital-twin.git`). Keep this tab open.

### 2.2 — Initialize git locally and push

Open a terminal in the `sail-digital-twin-github/` folder and run:

```bash
# Initialize a fresh git repo
git init
git branch -M main

# Stage everything (respects .gitignore)
git add .

# First commit
git commit -m "Initial commit: SAIL Digital Twin v1.1"

# Connect to your GitHub repo (REPLACE 'YOUR_USERNAME' with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sail-digital-twin.git

# Push to GitHub
git push -u origin main
```

> **First-time git users:** When prompted for credentials:
> - **Username:** your GitHub username
> - **Password:** a **Personal Access Token** (not your GitHub password)
>
> Create a token at: GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**.
> Tick the **`repo`** scope. Copy the token, paste it when git asks for a password.

### 2.3 — Verify the upload

Visit `https://github.com/YOUR_USERNAME/sail-digital-twin` in your browser.

You should see the full file tree. **Click on `models/`** — it should contain 8 `.pkl` files.
**Click on `data/`** — it should contain 10 `.parquet` files.

If `models/` or `data/` is empty: your `.gitignore` excluded them. Fix:

```bash
# Remove any accidental ignore on these folders
git add models/ data/ -f
git commit -m "Force-add model + data artifacts"
git push
```

---

## 🎯 STEP 3 — Deploy to Streamlit Cloud

### 3.1 — Sign in

Go to **[share.streamlit.io](https://share.streamlit.io)** → click **Sign in with GitHub**.

First time: authorize Streamlit to access your repositories.

### 3.2 — Create a new app

On the Streamlit Cloud dashboard, click **Create app** (top-right).

**Choose:** "Deploy a public app from GitHub"

Fill the form:

| Field | Value |
|-------|-------|
| **Repository** | `YOUR_USERNAME/sail-digital-twin` |
| **Branch** | `main` |
| **Main file path** | `streamlit_app/app.py` |
| **App URL** | `sail-digital-twin` → becomes `sail-digital-twin.streamlit.app` |

Click **"Advanced settings"**:

| Field | Value |
|-------|-------|
| **Python version** | `3.11` *(should match `runtime.txt`)* |
| **Secrets** | _(leave empty — no secrets needed)_ |

Click **Deploy!**

### 3.3 — Watch the build (~4-6 minutes first time)

A live log panel opens. You'll see:

```
[build] Cloning repository...
[build] Installing dependencies from requirements.txt...
[build] Collecting pandas>=2.0.0
[build] Collecting xgboost>=2.0.0
[build] ...
[build] Successfully installed ...
[run]   You can now view your Streamlit app in your browser.
[run]   Your app is live at https://sail-digital-twin.streamlit.app 🎉
```

Click the URL — **your dashboard is now live publicly**.

---

## 🎯 STEP 4 — Verify Everything Works

Open `https://sail-digital-twin.streamlit.app` in a fresh incognito browser window.

Click through each page in the left sidebar:

| # | Page | Expected |
|---|---|---|
| 1 | 🏠 Home | Headline KPIs: ₹8.48 Cr savings, ~3,930 t CO₂ |
| 2 | 🧪 Live Digital Twin | Sliders respond, AI predictions update in real time |
| 3 | 📊 Period Comparison | 4 tabs (Daily, Power, Mix, Control) with overlaid charts for A/B1/B2 |
| 4 | 🎓 Model Card | 99.83% accuracy displayed, architecture diagram visible |
| 5 | 🌱 Impact & Sustainability | Financial, Quality, Environmental, National tabs |

If something fails, click **"Manage app"** (bottom-right corner of the deployed dashboard) — opens the live log panel.

---

## 🔄 STEP 5 — How to Update the App Later

Any code change — just push to GitHub. Streamlit Cloud auto-redeploys within 1-2 minutes.

```bash
# Edit something, e.g., streamlit_app/app.py
git add .
git commit -m "Updated home page hero KPIs"
git push
```

Check the dashboard at `https://sail-digital-twin.streamlit.app` — refreshed automatically.

---

## 🆘 Troubleshooting

### ❌ Build fails: `ModuleNotFoundError: No module named 'xyz'`
**Fix:** Add the missing package to `requirements.txt`, commit, push. Auto-redeploys.

### ❌ Dashboard shows "Model artifacts not found"
**Cause:** `models/` folder is empty in the GitHub repo.
**Fix:** Navigate to `https://github.com/YOUR_USERNAME/sail-digital-twin/tree/main/models` — if empty, run:
```bash
git add models/ data/ -f
git commit -m "Add model artifacts"
git push
```

### ❌ Repository exceeds GitHub's 100 MB file limit
**Cause:** Someone committed `canonical_dataset/sail_master_5min.csv` (74 MB) or similar.
**Fix:** The `.gitignore` should prevent this. Verify:
```bash
git rm --cached canonical_dataset/ 2>/dev/null
git commit -m "Remove raw dataset from repo"
git push
```

### ❌ Build times out after 10 minutes
**Cause:** `requirements.txt` has heavy deps like `jupyter`.
**Fix:** Only keep packages the Streamlit app imports (see `requirements.txt` — it's already trimmed for you).

### ❌ "Oh no, this app ate all its memory"
**Cause:** Streamlit Cloud free tier limits apps to 1 GB RAM. Our app uses ~300 MB, so you're safe unless someone adds a huge chart or dataset.
**Fix:** Check **Manage app → Logs** for the OOM line, identify the trigger.

### ❌ App hibernates after 7 days inactivity
**Behavior:** Free tier hibernates idle apps. The next visitor waits ~30 seconds for wake-up.
**Mitigation:** Visit the URL yourself the morning of your Jury demo to warm it up.

### ❌ Need a custom domain (e.g., `dt.sail.co.in`)
**Free tier:** Not supported.
**Option:** Upgrade to Streamlit Teams plan, or set up an nginx reverse-proxy on your own server pointing to the `streamlit.app` URL.

---

## 🎬 What to Send the Jury

Once deployed, email the Jury:

```
Subject: SAIL Digital Twin — Interactive Dashboard for ICC Grand Jury Review

Honourable Jury Members,

Please find our working Digital Twin demonstrating the AI-Assisted
Stoichiometric Optimization project at SAIL Bokaro HDGL at:

    → https://sail-digital-twin.streamlit.app

Recommended exploration path (5 minutes):
  1. Home page     — headline KPIs (₹8.48 Cr savings, ~3,930 t CO₂)
  2. Live Digital Twin — try the "Thin-Gauge Strip" preset
  3. Model Card    — 99.83% cross-validated accuracy proof
  4. Impact & Sustainability — certified financial calculations

Works on desktop, tablet, mobile. No login required.
Best viewed in Chrome / Edge / Firefox.

Warm regards,
Parichay Bhattacharjee
SAIL Digital Transformation Division, Ranchi
```

---

## 🗺️ Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════════╗
║ STEP  │ ACTION                                       │ TIME        ║
╠═══════╪══════════════════════════════════════════════╪═════════════╣
║  1    │ Unzip project locally                        │ 1 min       ║
║  2    │ Create GitHub repo + git push                │ 3 min       ║
║  3    │ Create Streamlit Cloud app                   │ 2 min       ║
║  4    │ First build (pip install)                    │ 5 min       ║
║  5    │ Verify pages                                 │ 2 min       ║
╠═══════╪══════════════════════════════════════════════╪═════════════╣
║ TOTAL FIRST DEPLOY                                   │ ~15 min     ║
║ FUTURE UPDATES (git push auto-redeploy)              │ 90 seconds  ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 💡 Pro Tips for the Jury Demo (23 April 2026)

1. **Deploy 2-3 days before the review** to surface any bugs with time to spare
2. **Warm up the app** an hour before demo time — just visit the URL once
3. **Make a shortlink** — use tinyurl.com or bit.ly to shorten `sail-digital-twin.streamlit.app` for slides
4. **Screen-record a backup** using Loom or OBS — if Streamlit Cloud hiccups mid-demo, play the video
5. **Bring a hotspot** — don't trust Jury venue WiFi
6. **Test on mobile** — one Jury member might only have a phone handy

---

## 📞 Support

**SAIL Digital Transformation Division (SDTD)** · Ranchi, Jharkhand

Streamlit Cloud documentation: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
