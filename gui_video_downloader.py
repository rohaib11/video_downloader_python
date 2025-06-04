import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import yt_dlp
from plyer import notification


def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename


def start_download():
    url = url_entry.get().strip()
    quality = quality_var.get()
    status_label.config(text="Downloading...", foreground="blue")

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    threading.Thread(target=download_video, args=(url, quality)).start()


def download_video(url, quality):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"download_{now}.mp4"
    unique_filename = get_unique_filename(base_filename)

    opts = {
        'outtmpl': unique_filename,
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook]
    }

    # TikTok specific fix
    if "tiktok.com" in url:
        opts['format'] = 'best'  # Use 'best' for TikTok videos
    elif quality == "Best (MP4)":
        opts['format'] = 'bestvideo+bestaudio'
    elif quality == "720p (MP4)":
        opts['format'] = 'bestvideo[height<=720]+bestaudio'
    elif quality == "480p (MP4)":
        opts['format'] = 'bestvideo[height<=480]+bestaudio'
    elif quality == "Audio Only (MP3)":
        opts['format'] = 'bestaudio'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        opts['outtmpl'] = unique_filename.replace(".mp4", ".mp3")

    # Optional speed limit (example: 100KB/s)
    opts['ratelimit'] = 100000  # Set to 100 KB/s

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        status_label.config(text="✅ Download complete!", foreground="green")
        save_download_history(url, unique_filename)
        notify_user('Download complete!')
    except Exception as e:
        status_label.config(text="❌ Download failed!", foreground="red")
        messagebox.showerror("Download Error", str(e))


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = float(d['downloaded_bytes']) / float(d['total_bytes']) * 100
        status_label.config(text=f"Downloading... {percent:.2f}%", foreground="blue")
    elif d['status'] == 'finished':
        status_label.config(text="✅ Download complete!", foreground="green")


def choose_output_folder():
    folder = filedialog.askdirectory()
    return folder or os.getcwd()


def display_video_info(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'Unknown')
        uploader = info.get('uploader', 'Unknown')
        duration = info.get('duration', 0)
        status_label.config(text=f"Title: {title}\nUploader: {uploader}\nDuration: {duration}s")


def add_to_queue():
    url = url_entry.get().strip()
    if url:
        download_queue.append(url)
        status_label.config(text="Added to download queue.")
        print(f"Added {url} to download queue.")


def download_queue_task():
    while download_queue:
        url = download_queue.pop(0)
        start_download()


def save_download_history(url, filename):
    with open("download_history.txt", "a") as f:
        f.write(f"{url} -> {filename}\n")


def notify_user(message):
    notification.notify(
        title='YouTube Downloader',
        message=message,
        timeout=10
    )


def toggle_theme():
    current_bg = app.cget("bg")
    new_bg = "#333" if current_bg == "#f4f4f4" else "#f4f4f4"
    app.configure(bg=new_bg)
    status_label.config(bg=new_bg)
    url_entry.config(bg=new_bg)
    
    # Adjust the style of the combobox widget
    quality_dropdown.configure(style="Custom.TCombobox")
    
    # Change combobox background dynamically
    style = ttk.Style()
    style.configure("Custom.TCombobox", 
                    fieldbackground=new_bg, 
                    background=new_bg, 
                    foreground="white" if new_bg == "#333" else "black")
    
    # Adjust buttons' colors
    style.configure("TButton", 
                    background=new_bg, 
                    foreground="white" if new_bg == "#333" else "black")


def get_available_formats(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        return [(f['format_id'], f['format_note']) for f in formats]


def load_urls_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    with open(file_path, 'r') as file:
        urls = file.readlines()
    for url in urls:
        add_to_queue(url.strip())


def download_subtitles(url):
    opts = {
        'writesubtitles': True,
        'subtitleslangs': ['en', 'es'],  # Download English and Spanish subtitles
        'outtmpl': get_unique_filename(f"{url.split('/')[-1]}.%(ext)s"),
        'quiet': False
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


# UI Setup
app = tk.Tk()
app.title("YouTube Video Downloader")
app.geometry("600x450")
app.resizable(False, False)
app.configure(bg="#f4f4f4")

# Title
tk.Label(app, text="🎬 YouTube Downloader", font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack(pady=10)

# URL Entry
tk.Label(app, text="YouTube URL:", font=("Segoe UI", 12), bg="#f4f4f4").pack(anchor='w', padx=20)
url_entry = tk.Entry(app, font=("Segoe UI", 11), width=50)
url_entry.pack(padx=20, pady=5)

# Quality Dropdown
tk.Label(app, text="Select Quality:", font=("Segoe UI", 12), bg="#f4f4f4").pack(anchor='w', padx=20)
quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(app, textvariable=quality_var, font=("Segoe UI", 11), state='readonly')
quality_dropdown['values'] = ["Best (MP4)", "720p (MP4)", "480p (MP4)", "Audio Only (MP3)"]
quality_dropdown.current(0)
quality_dropdown.pack(padx=20, pady=5)

# Add to Queue Button
queue_button = ttk.Button(app, text="Add to Queue", command=add_to_queue)
queue_button.pack(pady=5)

# Load URLs from File Button
load_file_button = ttk.Button(app, text="Load URLs from File", command=load_urls_from_file)
load_file_button.pack(pady=5)

# Download Button
download_button = ttk.Button(app, text="⬇ Download", command=start_download)
download_button.pack(pady=10)

# Output Folder Button
folder_button = ttk.Button(app, text="Select Output Folder", command=choose_output_folder)
folder_button.pack(pady=5)

# Toggle Theme Button
theme_button = ttk.Button(app, text="Toggle Dark/Light Mode", command=toggle_theme)
theme_button.pack(pady=5)

# Status Label
status_label = tk.Label(app, text="", font=("Segoe UI", 11), bg="#f4f4f4")
status_label.pack()

# Video Information Button
info_button = ttk.Button(app, text="Video Info", command=lambda: display_video_info(url_entry.get().strip()))
info_button.pack(pady=5)

# Download Queue
download_queue = []

app.mainloop()
