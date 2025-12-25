from googleapiclient.discovery import build
from google.auth import default
import os

def test_drive_access(request):
    creds, _ = default()
    drive = build("drive", "v3", credentials=creds)

    folder_id = os.environ["DRIVE_FOLDER_ID"]

    results = drive.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get("files", [])
    
    print(f"Found {len(files)} files in folder ID {folder_id}.")

    return {
        "file_count": len(files),
        "files": files
    }
