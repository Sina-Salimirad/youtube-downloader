import os
import sys
import json
import time
import threading
import yt_dlp as ytd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RAILWAY_APP_URL = os.getenv("RAILWAY_APP_URL", "http://localhost:5000")

SERVER = f"{RAILWAY_APP_URL}/temp/"
TEMP_DIR = "temp"
DOWNLOAD_FORMAT = "bestvideo[height<=480]+bestaudio/best[height<=480]"
EXPIRE = 3600  # 1 hour

os.makedirs(TEMP_DIR, exist_ok=True)

# Ensure terminal output supports UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

playlist_videos = []

def send_status(status, data = None):
    message = {"status": status}

    if data is not None:
        message["data"] = data
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()

def delete_files(file_path, delay = EXPIRE):
    def delete():
        send_status("Deleting file", {"file": file_path, "in": delay})
        time.sleep(delay)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                send_status("File deleted", {"file": file_path})
            except Exception as e:
                send_status("Error deleting file", {"file": file_path, "error": str(e)})
        else:
            send_status("File not found", {"file": file_path})
        
    threading.Thread(target=delete, daemon=True).start()

def progress_hook(progress_data):
    if progress_data['status'] == 'downloading':
        send_status("Downloading", {
            "title": progress_data.get("info_dict", {}).get("title", "Unknown Title"),
            "file_size": progress_data.get("total_bytes", 0),
            "downloaded": progress_data.get("downloaded_bytes", 0),
            "percent": progress_data.get("_percent_str", '0%').strip(),
            "speed": progress_data.get("_speed_str", '0 KiB/s').strip(),
            "eta": progress_data.get("_eta_str", 'N/A').strip(),
        })

def single_video(video_info):
    video_id = video_info.get("id", "unknown")
    title = video_info.get("title", "Unknown Title")
    final_file = os.path.join(TEMP_DIR, f"{video_id}.mp4")
    
    # Retrieve the actual file size after download completion
    file_size = os.stat(final_file).st_size  # Get file size in bytes
    
    # Convert file size from bytes to megabytes for better readability
    file_size_mb = file_size / (1024 * 1024)  # Convert bytes to MB
    
    video_data = {
        "id": video_id,
        "title": title,
        "download_url": f"{SERVER}{video_id}.mp4",
        "file_size": file_size_mb,  # Send the actual file size in MB
    }

    playlist_videos.append(video_data)

    send_status("Video ready", video_data) # Send detailed information of each downloaded video

    delete_files(final_file)


def process_downloaded_info(info):
    # Check if the provided URL is a playlist
    if "entries" in info:
        for entry in info["entries"]:
            single_video(entry)
    else:
        single_video(info)

def download_video(url: str):
    options = {
        "format": DOWNLOAD_FORMAT,
        "outtmpl": os.path.join(TEMP_DIR, "%(id)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "merge_output_format": "mp4",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with ytd.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            process_downloaded_info(info)

    except Exception as e:
        send_status(f"Error: {str(e)}")

def main():
    if len(sys.argv) < 2:
        send_status("No URL provided")
        sys.exit(1)
    url = sys.argv[1]
    download_video(url)

if __name__ == "__main__":
    main()