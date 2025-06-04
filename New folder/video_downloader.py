import os
import yt_dlp
from pathlib import Path
from datetime import datetime

def get_unique_filename(output_path):
    base, ext = os.path.splitext(output_path)
    counter = 1
    while os.path.exists(output_path):
        output_path = f"{base}_{counter}{ext}"
        counter += 1
    return output_path

def choose_format():
    print("========== FORMAT OPTIONS ==========")
    print("1. Best Quality Video (MP4)")
    print("2. 720p Video (MP4)")
    print("3. 480p Video (MP4)")
    print("4. Audio Only (MP3)")
    print("====================================")
    choice = input("Enter your choice (1-4): ").strip()
    return choice

def get_ydl_options(choice, filename):
    opts = {
        'outtmpl': filename,
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4'
    }

    if choice == '1':
        opts['format'] = 'bestvideo+bestaudio'
    elif choice == '2':
        opts['format'] = 'bestvideo[height<=720]+bestaudio'
    elif choice == '3':
        opts['format'] = 'bestvideo[height<=480]+bestaudio'
    elif choice == '4':
        opts['format'] = 'bestaudio'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        opts['outtmpl'] = filename.replace(".mp4", ".mp3")
    else:
        print("⚠️ Invalid option. Defaulting to Best Quality.")
        opts['format'] = 'bestvideo+bestaudio'

    return opts

def main():
    print("🎬 YouTube Downloader - Advanced")
    url = input("🔗 Enter YouTube URL: ").strip()
    if not url:
        print("❌ URL is required!")
        return

    format_choice = choose_format()

    # Suggest a base filename based on timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"download_{now}.mp4"
    unique_filename = get_unique_filename(base_filename)

    ydl_opts = get_ydl_options(format_choice, unique_filename)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("⬇️ Starting download...")
            ydl.download([url])
            print("✅ Download and conversion complete.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
