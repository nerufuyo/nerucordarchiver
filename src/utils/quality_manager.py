"""
Quality settings and download resume functionality.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from ..config.constants import AUDIO_QUALITY, VIDEO_QUALITY, AUDIO_FORMAT


class QualityManager:
    """Manages quality settings and user preferences."""
    
    def __init__(self):
        self.config_file = Path.home() / '.nerucord' / 'config.json'
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'audio_quality': AUDIO_QUALITY,
            'video_quality': VIDEO_QUALITY,
            'audio_format': AUDIO_FORMAT,
            'output_dir': './downloads'
        }
    
    def get_audio_quality(self) -> str:
        """Get configured audio quality."""
        return self._config.get('audio_quality', AUDIO_QUALITY)
    
    def get_video_quality(self) -> str:
        """Get configured video quality."""
        return self._config.get('video_quality', VIDEO_QUALITY)
    
    def get_audio_format(self) -> str:
        """Get configured audio format."""
        return self._config.get('audio_format', AUDIO_FORMAT)
    
    def get_output_dir(self) -> str:
        """Get configured output directory."""
        return self._config.get('output_dir', './downloads')


class DownloadResume:
    """Manages download resume functionality."""
    
    def __init__(self):
        self.resume_file = Path.home() / '.nerucord' / 'downloads.json'
        self.resume_file.parent.mkdir(exist_ok=True)
        self._downloads = self._load_downloads()
    
    def _load_downloads(self) -> Dict[str, Any]:
        """Load download history from file."""
        if self.resume_file.exists():
            try:
                with open(self.resume_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'completed': [], 'failed': [], 'in_progress': []}
    
    def _save_downloads(self):
        """Save download history to file."""
        with open(self.resume_file, 'w') as f:
            json.dump(self._downloads, f, indent=2)
    
    def is_downloaded(self, url: str, output_path: str) -> bool:
        """Check if URL has been successfully downloaded."""
        for download in self._downloads['completed']:
            if download['url'] == url and download['output_path'] == output_path:
                return True
        return False
    
    def mark_completed(self, url: str, output_path: str, file_path: str):
        """Mark download as completed."""
        download_record = {
            'url': url,
            'output_path': output_path,
            'file_path': file_path,
            'timestamp': self._get_timestamp()
        }
        
        # Remove from in_progress if exists
        self._downloads['in_progress'] = [
            d for d in self._downloads['in_progress'] 
            if not (d['url'] == url and d['output_path'] == output_path)
        ]
        
        # Add to completed
        self._downloads['completed'].append(download_record)
        self._save_downloads()
    
    def mark_failed(self, url: str, output_path: str, error: str):
        """Mark download as failed."""
        download_record = {
            'url': url,
            'output_path': output_path,
            'error': error,
            'timestamp': self._get_timestamp()
        }
        
        # Remove from in_progress if exists
        self._downloads['in_progress'] = [
            d for d in self._downloads['in_progress'] 
            if not (d['url'] == url and d['output_path'] == output_path)
        ]
        
        # Add to failed
        self._downloads['failed'].append(download_record)
        self._save_downloads()
    
    def mark_in_progress(self, url: str, output_path: str):
        """Mark download as in progress."""
        download_record = {
            'url': url,
            'output_path': output_path,
            'timestamp': self._get_timestamp()
        }
        
        # Check if already in progress
        for download in self._downloads['in_progress']:
            if download['url'] == url and download['output_path'] == output_path:
                return
        
        self._downloads['in_progress'].append(download_record)
        self._save_downloads()
    
    def get_failed_downloads(self) -> list:
        """Get list of failed downloads."""
        return self._downloads['failed']
    
    def clear_failed(self):
        """Clear failed downloads list."""
        self._downloads['failed'] = []
        self._save_downloads()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


def get_video_format_options(quality: str) -> str:
    """Get yt-dlp format string for video quality with robust fallback options."""
    # Simplified format selection that works better with YouTube's current format structure
    quality_map = {
        '240p': 'bestvideo[height<=240]+bestaudio/worst',
        '360p': 'bestvideo[height<=360]+bestaudio/best',
        '480p': 'bestvideo[height<=480]+bestaudio/best', 
        '720p': 'bestvideo[height<=720]+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best'
    }
    # Default to 720p
    return quality_map.get(quality, 'bestvideo[height<=720]+bestaudio/best')


def get_audio_format_options(quality: str, format: str) -> Dict[str, Any]:
    """Get yt-dlp audio format options."""
    return {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': format,
        'preferredquality': quality,
    }
