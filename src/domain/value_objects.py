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
        return "playlist" in self.url or "list=" in self.url
    
    def is_channel(self) -> bool:
        """Check if the URL is a channel URL."""
        return "channel" in self.url or "user" in self.url or "c/" in self.url


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
