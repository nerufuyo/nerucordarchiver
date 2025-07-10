"""
Configuration settings for the YouTube Archiver application.
"""

import os
from pathlib import Path
from .constants import *


class Config:
    """Application configuration class."""
    
    def __init__(self):
        self.download_path = self._get_download_path()
        self.audio_quality = AUDIO_QUALITY
        self.video_quality = VIDEO_QUALITY
        self.audio_format = AUDIO_FORMAT
        self.video_format = VIDEO_FORMAT
        
    def _get_download_path(self) -> str:
        """Get the download path, create if doesn't exist."""
        download_dir = Path(DEFAULT_DOWNLOAD_PATH)
        download_dir.mkdir(parents=True, exist_ok=True)
        
        audio_dir = Path(AUDIO_DOWNLOAD_PATH)
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        video_dir = Path(VIDEO_DOWNLOAD_PATH)
        video_dir.mkdir(parents=True, exist_ok=True)
        
        return str(download_dir)
    
    def get_audio_path(self) -> str:
        """Get the audio download path."""
        return AUDIO_DOWNLOAD_PATH
    
    def get_video_path(self) -> str:
        """Get the video download path."""
        return VIDEO_DOWNLOAD_PATH
