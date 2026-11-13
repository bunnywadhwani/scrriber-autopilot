import asyncio
from pathlib import Path
import gdown
from src.asset_intelligence.analyzer import analyze_with_gemini
from src.content_engine.reel_composer import compose_cinematic_reel

async def run_autopilot_pipeline():
    folder_url = "https://drive.google.com/drive/folders/1lph4ALlLtAOA-DurDJYkcZLm-IfDdl-Y?usp=sharing"
    staging_dir = Path("data/drive_staging")
    output_dir = Path("data/reels_ready")
    staging_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n=======================================================")
    print("  SCRRIBER AUTOPILOT: SYNC & PRODUCTION PIPELINE")
    print("=======================================================\n")

    # 1. Sync from Google Drive
    print(f"📥 1. Checking Google Drive for new uploads...")
    files = gdown.download_folder(url=folder_url, output=str(staging_dir), quiet=True, use_cookies=False)
    
    # Also check local test folder if drive is empty
    target_files = list(staging_dir.glob("*.jpg")) + list(staging_dir.glob("*.png"))
    if not target_files:
        print("   ↳ Drive folder empty, inspecting Desktop test images...")
        target_files = list(Path("/Users/karmaln/Desktop/scrriber-test-images").glob("*.jpg"))

    print(f"   ↳ Found {len(target_files)} assets ready for processing.\n")

    # 2. Process each image into a cinematic Reel
    for idx, img in enumerate(target_files[:3], 1):
        print(f"[{idx}/{len(target_files)}] Processing: {img.name}")
        
        # Multimodal AI Content Strategy
        analysis = await analyze_with_gemini(str(img))
        caption = analysis.get("suggested_caption", "Nostalgic memories.")
        hashtags = " ".join(analysis.get("suggested_hashtags", ["#scrriber", "#cinematic"]))
        full_caption = f"{caption}\n.\n.\n{hashtags}"

        # Render Reel
        reel_filename = f"reel_{img.stem}.mp4"
        out_reel_path = output_dir / reel_filename
        compose_cinematic_reel(str(img), str(out_reel_path), duration_seconds=7)

        print(f"   🎬 Reel Rendered: {out_reel_path.name}")
        print(f"   ✍️ Caption: {caption}")
        print(f"   🏷️ Hashtags: {hashtags}")
        print("-------------------------------------------------------")

    print("\n✅ Batch processed and staged for Instagram publishing!\n")

if __name__ == "__main__":
    asyncio.run(run_autopilot_pipeline())
