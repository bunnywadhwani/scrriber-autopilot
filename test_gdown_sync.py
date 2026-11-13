import os
import gdown
from pathlib import Path

folder_url = "https://drive.google.com/drive/folders/1lph4ALlLtAOA-DurDJYkcZLm-IfDdl-Y?usp=sharing"
output_dir = Path("data/drive_staging")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Connecting to Google Drive folder...")
try:
    files = gdown.download_folder(url=folder_url, output=str(output_dir), quiet=False, use_cookies=False)
    print(f"\nSuccessfully synced {len(files) if files else 0} files from Google Drive to {output_dir.resolve()}!")
except Exception as e:
    print(f"Sync error: {e}")
