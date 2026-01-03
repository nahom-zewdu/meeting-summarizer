import json

def ingest_drive_file(event, context):
    """
    Triggered on any file creation in Drive.
    Filters for audio files and logs valid candidates.
    """

    data = event.get("data", {})
    file_id = data.get("id")
    name = data.get("name", "")
    mime = data.get("mimeType", "")

    # Hard filters (v1)
    if not mime.startswith("audio/"):
        print(f"Ignored non-audio file: {name} ({mime})")
        return

    if not name.lower().endswith((".mp3", ".m4a", ".wav", ".aac")):
        print(f"Ignored unsupported audio type: {name}")
        return

    print(f"Accepted audio file: {name} ({mime}), id={file_id}")
