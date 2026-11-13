from src.content_engine.reel_composer import compose_cinematic_reel
from pathlib import Path

img_input = "/Users/karmaln/Desktop/scrriber-test-images/Screenshot_2024-03-14-09-28-58-064_com.instagram.android.jpg"
out_video = "data/test_output_reel.mp4"

print(f"Composing test cinematic 9:16 Reel from: {img_input}...")
try:
    res = compose_cinematic_reel(img_input, out_video, duration_seconds=5)
    print(f"🎉 SUCCESS! Cinematic Reel created at: {res}")
    print(f"   Size: {Path(res).stat().st_size / 1024 / 1024:.2f} MB")
except Exception as e:
    print(f"Composition failed: {e}")
