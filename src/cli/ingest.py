import os
import sys
import asyncio
import json
from pathlib import Path
from src.asset_intelligence.analyzer import (
    calculate_sha256,
    calculate_phash,
    get_image_metadata,
    analyze_with_gemini
)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

async def process_folder(folder_path: str):
    folder = Path(folder_path).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    files = [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    print(f"\n==========================================")
    print(f"  SCRRIBER ASSET INTELLIGENCE INGESTION")
    print(f"  Target: {folder}")
    print(f"  Found {len(files)} image files to analyze")
    print(f"==========================================\n")

    results = []
    seen_hashes = set()

    for idx, file_path in enumerate(files, start=1):
        filename = file_path.name
        print(f"[{idx}/{len(files)}] Processing: {filename}...")

        # 1. Deduplication checks
        sha256 = calculate_sha256(str(file_path))
        phash = calculate_phash(str(file_path))
        is_exact_dup = sha256 in seen_hashes
        seen_hashes.add(sha256)

        # 2. Dimensions & aspect ratio
        meta = get_image_metadata(str(file_path))

        # 3. Multimodal AI Analysis (OCR, Category, Quality, Brand fit, Captions)
        print(f"  ↳ Running Gemini Multimodal Vision analysis...")
        ai_data = await analyze_with_gemini(str(file_path))

        record = {
            "filename": filename,
            "path": str(file_path),
            "sha256": sha256,
            "phash": phash,
            "is_duplicate": is_exact_dup,
            "dimensions": f"{meta['width']}x{meta['height']}",
            "aspect_ratio": meta["aspect_ratio"],
            "category": ai_data.get("primary_category"),
            "quality_score": ai_data.get("quality_score"),
            "brand_fit_score": ai_data.get("brand_fit_score"),
            "extracted_text": ai_data.get("extracted_text"),
            "description": ai_data.get("description"),
            "recommended_modifications": ai_data.get("recommended_modifications"),
            "suggested_caption": ai_data.get("suggested_caption"),
            "suggested_hashtags": ai_data.get("suggested_hashtags"),
            "publishing_suitability": ai_data.get("publishing_suitability")
        }
        results.append(record)

        print(f"  ✅ Category: {record['category']} | Brand Fit: {record['brand_fit_score']}/10 | Suitability: {record['publishing_suitability']}")
        if record['extracted_text']:
            snippet = record['extracted_text'][:80].replace('\n', ' ')
            print(f"  📝 OCR Text: \"{snippet}...\"")
        print(f"  💡 Suggested Caption: {record['suggested_caption'][:90]}...")
        print(f"--------------------------------------------------")

    # Save summary report to JSON
    report_file = Path("data") / "audit_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n🎉 Ingestion complete! Audit report saved to {report_file.resolve()}\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/Users/karmaln/Desktop/scrriber-test-images"
    asyncio.run(process_folder(target))
