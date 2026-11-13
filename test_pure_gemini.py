import os
import sys
import json
import base64
import urllib.request
from pathlib import Path

def get_jpeg_size(filepath):
    # Pure python JPEG header parser to get dimensions without external libraries
    with open(filepath, 'rb') as f:
        data = f.read()
    i = 0
    if data[:2] != b'\xff\xd8':
        return 1080, 1080
    i += 2
    while i < len(data):
        marker, = data[i:i+2],
        i += 2
        if marker[0] != 0xff:
            break
        if marker[1] in (0xc0, 0xc1, 0xc2, 0xc3): # SOF markers
            h, w = int.from_bytes(data[i+3:i+5], 'big'), int.from_bytes(data[i+5:i+7], 'big')
            return w, h
        length = int.from_bytes(data[i:i+2], 'big')
        i += length
    return 1080, 1080

def analyze_image(filepath, api_key):
    with open(filepath, 'rb') as f:
        img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode('utf-8')

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
  "extracted_text": "Exact text or subtitles visible in the image, or empty if none",
  "description": "Concise 1-2 sentence description of the visual scene, subject, aesthetic, and context",
  "primary_category": "One of [Love, Heartbreak, Relationships, Emotional, Deep Thoughts, Quotes, Movies, Cinema, Storytelling, Funny, Memes, Relatable, Nostalgia, Other]",
  "tags": ["tag1", "tag2", "tag3"],
  "quality_score": 8.5,
  "brand_fit_score": 9.0,
  "movie_or_show_reference": "Name of movie/series if identifiable, otherwise null",
  "can_post_directly_as_is": true,
  "recommended_modifications": "Specific advice: e.g. 'Crop black video bars', 'Directly post as single image', 'Use as video clip', etc.",
  "suggested_caption": "Engaging, authentic caption in @scrriber tone (nostalgic, expressive, or relatable)",
  "suggested_hashtags": ["#scrriber", "#relatable", "..."],
  "publishing_suitability": "APPROVED or NEEDS_EDIT or REJECTED"
}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        raw = data['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw)

def main():
    with open('.env', 'r') as f:
        env_lines = f.readlines()
    api_key = None
    for line in env_lines:
        if line.startswith('GEMINI_API_KEY='):
            api_key = line.strip().split('=', 1)[1]
            break

    folder = Path('/Users/karmaln/Desktop/scrriber-test-images')
    images = sorted([f for f in folder.glob('*.jpg')])
    
    print(f"\n=======================================================")
    print(f"  SCRRIBER ASSET INTELLIGENCE AUDIT (LIVE TEST)")
    print(f"  Target Folder: {folder}")
    print(f"  Found {len(images)} images")
    print(f"=======================================================\n")

    for idx, img in enumerate(images, 1):
        w, h = get_jpeg_size(str(img))
        print(f"[{idx}/{len(images)}] Analyzing: {img.name}")
        print(f"   Resolution: {w}x{h}")
        res = analyze_image(str(img), api_key)
        print(f"   Category: {res.get('primary_category')}")
        print(f"   Brand Fit: {res.get('brand_fit_score')}/10 | Suitability: {res.get('publishing_suitability')}")
        if res.get("movie_or_show_reference"):
            print(f"   Movie/Show: {res.get('movie_or_show_reference')}")
        if res.get("extracted_text"):
            print(f"   Subtitles/Text: \"{res.get('extracted_text')}\"")
        print(f"   Can Post Directly: {res.get('can_post_directly_as_is')}")
        print(f"   Advice: {res.get('recommended_modifications')}")
        print(f"   Suggested Caption: {res.get('suggested_caption')}")
        print(f"   Hashtags: {' '.join(res.get('suggested_hashtags', []))}")
        print("-" * 55)

if __name__ == '__main__':
    main()
