import os
import hashlib
import uuid
import json
import base64
import urllib.request
from typing import Dict, Any, Optional
from PIL import Image
import imagehash
from src.core.config import settings

def calculate_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_phash(filepath: str) -> str:
    try:
        with Image.open(filepath) as img:
            return str(imagehash.phash(img))
    except Exception:
        return ""

def get_image_metadata(filepath: str) -> Dict[str, Any]:
    with Image.open(filepath) as img:
        width, height = img.size
        img_format = img.format or "UNKNOWN"
    
    file_size = os.path.getsize(filepath)
    ratio_val = width / height if height > 0 else 1.0
    
    if abs(ratio_val - 0.8) < 0.05:
        aspect_ratio = "4:5 (Portrait)"
    elif abs(ratio_val - 1.0) < 0.05:
        aspect_ratio = "1:1 (Square)"
    elif abs(ratio_val - 0.5625) < 0.05:
        aspect_ratio = "9:16 (Story/Reel)"
    else:
        aspect_ratio = f"{ratio_val:.2f}:1 (Custom)"
        
    return {
        "width": width,
        "height": height,
        "format": img_format,
        "file_size_bytes": file_size,
        "aspect_ratio": aspect_ratio
    }

async def analyze_with_gemini(filepath: str) -> Dict[str, Any]:
    """
    Sends the image to Gemini multimodal model to extract OCR text,
    brand classification, quality scoring, and caption recommendations.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in .env")

    with open(filepath, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are the Chief AI Content Curator for the Instagram media brand @scrriber.
Brand identity: Relatable, dark, cinematic, nostalgic, expressive, emotionally engaging.
Target Content Pillars:
- Love & Emotions
- Heartbreak & Relationships
- Deep Thoughts & Quotes
- Movies, Cinema & Storytelling
- Funny, Memes & Relatable
- Nostalgia

Analyze this screenshot / saved image thoroughly and return ONLY a valid JSON object with the following structure:
{
  "extracted_text": "Exact text visible in the image, dialogues, captions, quotes, subtitles, or empty if none",
  "description": "Concise 1-2 sentence description of the visual scene, subject, aesthetic, and context",
  "primary_category": "One of [Love, Heartbreak, Relationships, Emotional, Deep Thoughts, Quotes, Movies, Cinema, Storytelling, Funny, Memes, Relatable, Nostalgia, Other]",
  "tags": ["tag1", "tag2", "tag3"],
  "quality_score": 8.5, // 0.0 to 10.0 scale based on visual clarity and aesthetic quality
  "brand_fit_score": 9.0, // 0.0 to 10.0 scale based on alignment with @scrriber's dark/cinematic/relatable identity
  "movie_or_show_reference": "Name of movie/series if identifiable from subtitles or scene, otherwise null",
  "recommended_modifications": "Specific advice: e.g. 'Crop black video bars', 'Re-render text as clean typography', 'Ready to publish as-is'",
  "suggested_caption": "Engaging, authentic caption in @scrriber tone (nostalgic, expressive, or relatable)",
  "suggested_hashtags": ["#scrriber", "#cinematic", "..."],
  "publishing_suitability": "APPROVED or NEEDS_EDIT or REJECTED"
}
Do not include markdown code block formatting (like ```json), just output the raw JSON string.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return json.loads(raw_text)
    except Exception as e:
        return {
            "error": str(e),
            "extracted_text": "",
            "description": "Analysis failed",
            "primary_category": "Other",
            "tags": [],
            "quality_score": 0.0,
            "brand_fit_score": 0.0,
            "recommended_modifications": "Manual inspection needed",
            "suggested_caption": "",
            "suggested_hashtags": [],
            "publishing_suitability": "NEEDS_EDIT"
        }
