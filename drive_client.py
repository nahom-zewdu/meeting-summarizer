# drive_client.py
"""Module to interact with Google Drive API for listing and downloading audio files."""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from pathlib import Path
import logging

logger = logging.getLogger("drive_client")

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

def build_drive_service():
    """Builds and returns a Google Drive service object."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(folder_id):
    """Lists files in a specified Google Drive folder."""
    service = build_drive_service()
    query = f"'{folder_id}' in parents and mimeType contains 'audio/'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    logger.info(f"Found {len(files)} files in Drive folder {folder_id}")
    return files

def download_file(file_id, dest_folder="audio_downloads"):
    """Downloads a file from Google Drive given its file ID."""
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(exist_ok=True)
    service = build_drive_service()
    request = service.files().get_media(fileId=file_id)
    file_path = dest_folder / f"{file_id}.wav"  # all audio converted to wav
    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        logger.info(f"Download {int(status.progress() * 100)}% complete")
    fh.close()
    return file_path
