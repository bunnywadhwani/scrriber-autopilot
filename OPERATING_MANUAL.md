# Scrriber Autopilot: Operating & Publishing Manual 🚀

This guide explains **exactly how to activate live posting online** whenever you are ready, how the system works end-to-end, and the commands to run on any machine.

---

## 1. How Live Publishing Works Online

Instagram strictly requires publishing through **Meta's Official Content Publishing Graph API**.
Because Meta's servers need to download your video/image during publishing, the asset must be accessible via a public URL (or uploaded directly to your Cloudflare R2 / S3 storage).

The publishing workflow runs like this:

```
[1. Upload to Google Drive]
        │
        ▼
[2. Autopilot Ingests & Composes]
    - Downloads from Drive
    - Gemini AI analyzes emotion & writes caption + hashtags
    - FFmpeg renders 9:16 Ken Burns cinematic video Reel
        │
        ▼
[3. Uploads to Cloud Storage (Cloudflare R2 / Public Temp)]
        │
        ▼
[4. Meta Instagram Graph API Publishes]
    - Creates Instagram media container
    - Meta fetches video
    - Publishes directly to @scrriber!
```

---

## 2. One-Time Setup: Connecting Meta / Instagram API

When you are ready to publish directly online, you only need to fill in these 3 lines in your `.env` file:

```env
META_APP_ID=your_meta_app_id
META_USER_ACCESS_TOKEN=your_long_lived_token
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
```

### Quick Steps to Get These (15 minutes):
1. **Switch @scrriber to Professional:**
   - On the Instagram mobile app: *Settings ➔ Account type and tools ➔ Switch to professional / creator account*.
2. **Connect to a Facebook Page:**
   - In Instagram app settings: *Settings ➔ Creator / Business ➔ Connect or create a Facebook Page* (name it "Scrriber").
3. **Get Free Meta Graph Token:**
   - Go to [Meta Developers Portal](https://developers.facebook.com/).
   - Create an app ➔ Select **Business** type.
   - Add **Instagram Graph API**.
   - Under Graph API Explorer, select permissions:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_show_list`
     - `pages_read_engagement`
   - Generate your Access Token and copy your `INSTAGRAM_ACCOUNT_ID`.

---

## 3. How to Start the System Whenever You Need

### Option A: Run Manually (On-Demand)
Whenever you upload 10–20 photos to your Google Drive folder and want to generate & post them:

```bash
# 1. Open the project folder
cd ~/Desktop/scrriber-autopilot

# 2. Activate Python environment
source .venv/bin/activate

# 3. Run the complete pipeline (Sync Drive -> AI Curate -> Render Reels -> Post)
python -m src.cli.sync_and_produce
```

### Option B: Automatic Daily Schedule (100% Autopilot)
If you want the system to post every day automatically at your preferred time (e.g. 6:30 PM):

Add a simple cron job on your Mac or cloud server:
```bash
crontab -e
```
Add this single line (runs every day at 18:30):
```text
30 18 * * * cd /Users/karmaln/Desktop/scrriber-autopilot && .venv/bin/python -m src.cli.sync_and_produce >> data/autopilot.log 2>&1
```

---

## 4. How to Resume on a Different Computer (Portability)

Since everything is cleanly pushed to your GitHub repository, when you move to a new machine:

```bash
# 1. Clone your private repository
git clone git@github.com:bunnywadhwani/scrriber-autopilot.git
cd scrriber-autopilot

# 2. Create virtual environment & install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gdown

# 3. Create your .env file
cp .env.example .env
# Fill in your GEMINI_API_KEY and META credentials

# 4. Run the pipeline!
python -m src.cli.sync_and_produce
```

---

## 5. Summary of Files in This Repository

| File / Directory | Purpose |
|---|---|
| `OPERATING_MANUAL.md` | This step-by-step master guide. |
| `src/asset_intelligence/` | Gemini multimodal vision & OCR engine. |
| `src/content_engine/` | FFmpeg cinematic Reel composer (9:16 with zoom & audio). |
| `src/publishing/` | Official Meta Graph API publisher for Instagram. |
| `src/cli/sync_and_produce.py` | One-command runner to sync Drive and produce posts. |
| `data/` | Staging area for incoming Drive files and rendered Reels (git-ignored). |
