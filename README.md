# YouTube Video Downloader

A Python-based application that allows users to download videos from YouTube and other supported platforms using the `yt-dlp` library with a Tkinter graphical interface. The downloader offers features like batch downloading, subtitle downloads, and quality selection.

## Features
- **Download Videos**: Download videos from YouTube and other supported platforms.
- **Quality Selection**: Choose video quality from available formats (Best, 720p, 480p) and audio format (MP3).
- **Subtitle Support**: Download subtitles in multiple languages (English, Spanish).
- **Batch Downloading**: Load multiple URLs from a `.txt` file to download in a batch.
- **Dark/Light Mode**: Toggle between dark and light mode for the user interface.
- **Download History**: Keeps a log of URLs and filenames for all downloaded videos.
- **Video Information**: Display video metadata (title, uploader, duration).

## Supported Platforms
`yt-dlp` supports downloading from a wide variety of video platforms. Below is the list of supported platforms:

- **YouTube**
- **Vimeo**
- **Dailymotion**
- **Facebook**
- **Instagram**
- **Twitter**
- **TikTok**
- **SoundCloud**
- **Twitch**
- **Reddit**
- **YouKu**
- **DailyMotion**
- **Mixer**
- **Bilibili**
- **Pornhub, XVideos, and other adult platforms** (with proper configurations)
- **Spotify** (for audio downloads via special post-processing)
- **Metacafe**
- **Flickr**
- **MySpace**
- **Archive.org** (for public domain videos)

### **How to Use**
1. **Clone the Repository**:
   - Clone the repository using the following command:
     ```bash
     git clone https://github.com/rohaib11/video_downloader_python.git
     ```

2. **Install Dependencies**:
   - Navigate to the project folder and install the required dependencies:
     ```bash
     cd video_downloader_python
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Once dependencies are installed, you can run the application by executing:
     ```bash
     python gui_video_downloader.py
     ```

### **Installation and Setup**
#### 1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rohaib11/video_downloader_python.git
