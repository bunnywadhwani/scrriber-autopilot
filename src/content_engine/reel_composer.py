import os
import subprocess
from pathlib import Path
from typing import Optional

def compose_cinematic_reel(
    image_path: str,
    output_path: str,
    duration_seconds: int = 7,
    audio_path: Optional[str] = None
) -> str:
    img = Path(image_path).resolve()
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if not img.exists():
        raise FileNotFoundError(f"Source image '{img}' not found.")

    fps = 30
    total_frames = duration_seconds * fps

    # Ken Burns slow zoom (centered) + 1080x1920 crop
    filter_video = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0010,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
        f"format=yuv420p"
    )

    if audio_path and os.path.exists(audio_path):
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-loop", "1", "-i", str(img),
            "-i", str(audio_path),
            "-vf", filter_video,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration_seconds),
            "-movflags", "+faststart",
            str(out)
        ]
    else:
        # High-compatibility silent audio track
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-loop", "1", "-i", str(img),
            "-f", "lavfi", "-t", str(duration_seconds), "-i", "anullsrc=r=44100:cl=stereo",
            "-vf", filter_video,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration_seconds),
            "-movflags", "+faststart",
            str(out)
        ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg reel composition failed: {res.stderr}")

    return str(out)
