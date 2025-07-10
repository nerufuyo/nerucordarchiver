# Global Configuration Constants
"""
Global configuration constants for the YouTube Archiver application.
This module contains all configurable values used throughout the application.
"""

# Application Information
APP_NAME = "NeruCord Archiver"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A powerful YouTube video and audio downloader with playlist support"

# Download Paths
DEFAULT_DOWNLOAD_PATH = "./downloads"
AUDIO_DOWNLOAD_PATH = "./downloads/audio"
VIDEO_DOWNLOAD_PATH = "./downloads/video"

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
    r"youtube\.com/user"
]

# Timeouts
DOWNLOAD_TIMEOUT = 300  # seconds
NETWORK_TIMEOUT = 30  # seconds

# Limits
MAX_PLAYLIST_SIZE = 1000
MAX_FILENAME_LENGTH = 200
