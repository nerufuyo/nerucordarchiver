# Global Configuration Constants
"""
Global configuration constants for the YouTube Archiver application.
This module contains all configurable values used throughout the application.
"""

import os
from pathlib import Path

def get_default_download_path():
    """Get the default Downloads folder for the current platform."""
    # Get user's home directory
    home = Path.home()
    
    # Try to find Downloads folder (handles different languages/localizations)
    downloads_candidates = [
        home / "Downloads",
        home / "downloads", 
        home / "Download",
        home / "download",
        home / "Téléchargements",  # French
        home / "Descargas",       # Spanish
        home / "下载",             # Chinese
        home / "ダウンロード",        # Japanese
    ]
    
    # Return the first existing Downloads folder, or create Downloads if none exist
    for downloads_path in downloads_candidates:
        if downloads_path.exists() and downloads_path.is_dir():
            return str(downloads_path / "NeruCord")
    
    # Fallback: create Downloads folder if it doesn't exist
    downloads_path = home / "Downloads" / "NeruCord"
    return str(downloads_path)

# Application Information
APP_NAME = "NeruCord Archiver"
APP_VERSION = "1.1.0"
APP_DESCRIPTION = "A powerful YouTube video and audio downloader with playlist support"

# Download Paths
DEFAULT_DOWNLOAD_PATH = get_default_download_path()
AUDIO_DOWNLOAD_PATH = os.path.join(DEFAULT_DOWNLOAD_PATH, "audio")
VIDEO_DOWNLOAD_PATH = os.path.join(DEFAULT_DOWNLOAD_PATH, "video")

# File Formats
AUDIO_FORMAT = "mp3"
VIDEO_FORMAT = "mp4"
AUDIO_QUALITY = "192"  # kbps
VIDEO_QUALITY = "720p"

# Error Messages
ERROR_INVALID_URL = "Invalid YouTube URL provided"
ERROR_DOWNLOAD_FAILED = "Download failed for the provided URL"
ERROR_CONVERSION_FAILED = "Audio conversion failed"
ERROR_NETWORK_ERROR = "Network connection error"
ERROR_PLAYLIST_NOT_FOUND = "Playlist not found or is private"
ERROR_VIDEO_NOT_FOUND = "Video not found or is private"

# Success Messages
SUCCESS_DOWNLOAD_COMPLETE = "Download completed successfully"
SUCCESS_CONVERSION_COMPLETE = "Audio conversion completed successfully"
SUCCESS_PLAYLIST_DOWNLOAD = "Playlist download completed"

# Progress Messages
PROGRESS_DOWNLOADING = "Downloading"
PROGRESS_CONVERTING = "Converting to audio"
PROGRESS_FETCHING_INFO = "Fetching video information"

# File Extensions
SUPPORTED_AUDIO_FORMATS = ["mp3", "wav", "flac", "aac"]
SUPPORTED_VIDEO_FORMATS = ["mp4", "webm", "mkv", "avi"]

# URL Patterns
YOUTUBE_URL_PATTERNS = [
    r"youtube\.com/watch",
    r"youtu\.be/",
    r"youtube\.com/playlist",
    r"youtube\.com/channel",
    r"youtube\.com/user",
    r"youtube\.com/c/",
    r"youtube\.com/@",
    r"youtube\.com/.*/videos",
    r"music\.youtube\.com/watch",
    r"music\.youtube\.com/playlist",
    r"music\.youtube\.com/album",
    r"music\.youtube\.com/browse"
]

# Timeouts
DOWNLOAD_TIMEOUT = 300  # seconds
NETWORK_TIMEOUT = 30  # seconds

# Limits
MAX_PLAYLIST_SIZE = 1000
MAX_FILENAME_LENGTH = 200
