# meeting_pipeline.py
"""Main pipeline to process meeting audio files from Google Drive, transcribe, and summarize them."""

import os
import logging
from drive_client import list_files_in_folder, download_file
from transcribe_and_summarize import transcribe_audio, generate_summary
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meeting_pipeline")

DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")
OUTPUT_FOLDER = Path("outputs")
OUTPUT_FOLDER.mkdir(exist_ok=True)

def main():
    files = list_files_in_folder(DRIVE_FOLDER_ID)
    if not files:
        logger.warning("No audio files found")
        return
    
    for f in files:
        try:
            audio_path = download_file(f["id"])
            logger.info(f"Downloaded {f['name']} -> {audio_path}")
            transcript = transcribe_audio(audio_path)
            logger.info(f"Transcript done for {f['name']}")
            summary = generate_summary(transcript)
            out_path = OUTPUT_FOLDER / f"{f['name']}.txt"
            out_path.write_text(summary, encoding="utf-8")
            logger.info(f"Saved summary -> {out_path}")
        except Exception as e:
            logger.error(f"Failed processing {f['name']}: {e}")

if __name__ == "__main__":
    main()
