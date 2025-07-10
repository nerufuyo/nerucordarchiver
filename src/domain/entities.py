"""
Domain entities for the YouTube Archiver application.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class DownloadType(Enum):
    """Enumeration for download types."""
    AUDIO = "audio"
    VIDEO = "video"
    BOTH = "both"


class DownloadStatus(Enum):
    """Enumeration for download status."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    CONVERTING = "converting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class VideoInfo:
    """Entity representing video information."""
    title: str
    url: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    view_count: Optional[int] = None
    
    def __post_init__(self):
        if not self.url:
            raise ValueError("URL cannot be empty")
        if not self.title:
            raise ValueError("Title cannot be empty")


@dataclass
class PlaylistInfo:
    """Entity representing playlist information."""
    title: str
    url: str
    videos: List[VideoInfo]
    uploader: Optional[str] = None
    video_count: Optional[int] = None
    
    def __post_init__(self):
        if not self.url:
            raise ValueError("Playlist URL cannot be empty")
        if not self.title:
            raise ValueError("Playlist title cannot be empty")
        if self.video_count is None:
            self.video_count = len(self.videos)


@dataclass
class DownloadTask:
    """Entity representing a download task."""
    video_info: VideoInfo
    download_type: DownloadType
    output_path: str
    status: DownloadStatus = DownloadStatus.PENDING
    progress: float = 0.0
    error_message: Optional[str] = None
    
    def update_progress(self, progress: float):
        """Update download progress."""
        if 0 <= progress <= 100:
            self.progress = progress
        else:
            raise ValueError("Progress must be between 0 and 100")
    
    def mark_completed(self):
        """Mark task as completed."""
        self.status = DownloadStatus.COMPLETED
        self.progress = 100.0
    
    def mark_failed(self, error_message: str):
        """Mark task as failed with error message."""
        self.status = DownloadStatus.FAILED
        self.error_message = error_message
