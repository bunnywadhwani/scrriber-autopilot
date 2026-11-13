# Scrriber Autopilot 🚀

Autonomous, self-improving content operations platform engineered to revive and scale [@scrriber](https://www.instagram.com/scrriber/).

## Brand Essence & Identity
- **Tone:** Dark, cinematic, nostalgic, expressive, emotionally relatable, and witty.
- **Content Pillars:**
  1. *Love & Emotions* (Heartbreak, connection, vulnerability)
  2. *Movies & Storytelling* (Cinematic stills, dialogues, narrative reflections)
  3. *Deep Thoughts & Words* (Quotes, poetry, existential musings)
  4. *Funny & Relatable* (Modern relationship humor, observations, witty banter)

## Architecture Overview
- **Backend:** Python 3.13 / FastAPI (Asynchronous API & worker orchestration)
- **Database:** PostgreSQL + SQLAlchemy 2.0 / Alembic
- **Task Queue & Caching:** Redis
- **Storage:** Cloudflare R2 (S3-compatible, zero egress costs)
- **Asset Intelligence:** Local Perceptual Hashing (pHash) deduplication, Apple Vision/Tesseract OCR, Multimodal Vision AI analysis
- **Publishing:** Official Meta Instagram Graph API (Single images, Carousels, Reels)
- **Self-Improvement:** Closed-loop engagement analytics engine

## Quickstart (Development)
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Fill in your credentials in .env

# 4. Ingest screenshots / image library
python -m src.cli.main ingest --path /path/to/screenshots
```
