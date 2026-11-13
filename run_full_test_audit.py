import urllib.request, json, base64
from pathlib import Path

with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GEMINI_API_KEY='):
            key = line.strip().split('=', 1)[1]
            break

folder = Path('/Users/karmaln/Desktop/scrriber-test-images')
images = sorted([f for f in folder.glob('*.jpg')])

prompt = """
You are the Chief AI Content Strategist for @scrriber.
Brand identity: Nostalgic, dark, cinematic, emotionally relatable, expressive.
Review this screenshot/image and answer with ONLY JSON:
{
  "dialogue_or_text": "Exact text or subtitle in image, or null if pure visual",
  "source_or_movie": "Name of show/movie/context if identifiable, else null",
  "category": "One of [Love, Heartbreak, Relationships, Emotional, Deep Thoughts, Quotes, Movies, Cinema, Storytelling, Funny, Memes, Relatable, Nostalgia]",
  "can_post_directly_as_is": true or false,
  "publishing_advice": "Detailed formatting advice (e.g. crop black bars, post directly as single image, use as Reel hook, redesign text)",
  "brand_fit_score": 8.5, // 0 to 10
  "caption": "Captivating @scrriber caption",
  "hashtags": ["#scrriber", "#..."]
}
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={key}"

audit_results = []
print(f"\n=======================================================")
print(f"  RUNNING FULL AUDIT ON {len(images)} TEST SCREENSHOTS")
print(f"=======================================================\n")

for idx, img in enumerate(images, 1):
    print(f"[{idx}/{len(images)}] Auditing: {img.name}...")
    with open(img, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
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
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            res = json.loads(data['candidates'][0]['content']['parts'][0]['text'])
            res['filename'] = img.name
            audit_results.append(res)
            print(f"   🎬 Source: {res.get('source_or_movie')} | Category: {res.get('category')} | Brand Fit: {res.get('brand_fit_score')}/10")
            print(f"   💬 Text: \"{res.get('dialogue_or_text')}\"")
            print(f"   🚀 Can Post As-Is: {res.get('can_post_directly_as_is')}")
            print(f"   🛠️ Advice: {res.get('publishing_advice')}")
            print(f"   ✍️ Caption: {res.get('caption')}")
            print(f"   🏷️ Hashtags: {' '.join(res.get('hashtags', []))}")
            print("-" * 55)
    except Exception as e:
        print(f"   ❌ Error analyzing {img.name}: {e}")

Path("data").mkdir(exist_ok=True)
with open("data/test_audit_report.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2)

print("\n🎉 Audit complete! Saved to data/test_audit_report.json")
