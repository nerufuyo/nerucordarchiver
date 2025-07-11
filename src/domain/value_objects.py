"""
Value objects for the YouTube Archiver application.
"""

import re
from dataclasses import dataclass
from typing import Union
from ..config.constants import YOUTUBE_URL_PATTERNS


@dataclass(frozen=True)
class YouTubeURL:
    """Value object representing a YouTube URL."""
    url: str
    
    def __post_init__(self):
        if not self._is_valid_youtube_url(self.url):
            raise ValueError(f"Invalid YouTube URL: {self.url}")
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Validate if the URL is a valid YouTube URL."""
        return any(re.search(pattern, url) for pattern in YOUTUBE_URL_PATTERNS)
    
    def is_playlist(self) -> bool:
        """Check if the URL is a playlist URL."""
        return any([
            "playlist" in self.url,
            "list=" in self.url,
            "album" in self.url and "music.youtube.com" in self.url,
            "&list=" in self.url
        ])
    
    def is_channel(self) -> bool:
        """Check if the URL is a channel URL."""
        return any([
            "channel" in self.url,
            "user" in self.url,
            "c/" in self.url,
            "@" in self.url and "youtube.com/" in self.url,
            "/videos" in self.url and "youtube.com/" in self.url
        ])

    def is_music_youtube(self) -> bool:
        """Check if the URL is from music.youtube.com."""
        return "music.youtube.com" in self.url
    
    def normalize_url(self) -> str:
        """Normalize the URL for better compatibility."""
        url = self.url
        
        # Remove tracking parameters
        tracking_params = ['si=', 'feature=', 'utm_', 'fbclid=']
        for param in tracking_params:
            if param in url:
                # Find the parameter and remove it along with its value
                param_start = url.find(param)
                if param_start != -1:
                    # Find the next & or end of string
                    param_end = url.find('&', param_start)
                    if param_end == -1:
                        param_end = len(url)
                    # Remove the parameter
                    before = url[:param_start]
                    after = url[param_end:]
                    url = before + after
                    # Clean up double &s or trailing &
                    url = url.replace('&&', '&').rstrip('&').rstrip('?')
        
        return url


@dataclass(frozen=True)
class FilePath:
    """Value object representing a file path."""
    path: str
    
    def __post_init__(self):
        if not self.path or not self.path.strip():
            raise ValueError("File path cannot be empty")
    
    def get_extension(self) -> str:
        """Get file extension."""
        return self.path.split('.')[-1] if '.' in self.path else ""
    
    def get_filename(self) -> str:
        """Get filename without path."""
        return self.path.split('/')[-1] if '/' in self.path else self.path


@dataclass(frozen=True)
class Quality:
    """Value object representing quality settings."""
    value: Union[str, int]
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Quality value cannot be empty")
    
    def __str__(self) -> str:
        return str(self.value)
