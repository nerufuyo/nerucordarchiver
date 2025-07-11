"""
Repository interfaces for the YouTube Archiver application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Callable
from ..domain.entities import VideoInfo, PlaylistInfo, ChannelInfo, DownloadTask
from ..domain.value_objects import YouTubeURL


class IVideoRepository(ABC):
    """Interface for video information repository."""
    
    @abstractmethod
    async def get_video_info(self, url: YouTubeURL) -> VideoInfo:
        """Get video information from URL."""
        pass
    
    @abstractmethod
    async def get_playlist_info(self, url: YouTubeURL) -> PlaylistInfo:
        """Get playlist information from URL."""
        pass
    
    @abstractmethod
    async def get_channel_info(self, url: YouTubeURL) -> ChannelInfo:
        """Get channel information from URL."""
        pass


class IDownloaderRepository(ABC):
    """Interface for download operations."""
    
    @abstractmethod
    async def download_video(
        self, 
        task: DownloadTask, 
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Download video file."""
        pass
    
    @abstractmethod
    async def download_audio(
        self, 
        task: DownloadTask, 
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Download and convert to audio file."""
        pass


class IFileRepository(ABC):
    """Interface for file operations."""
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        pass
    
    @abstractmethod
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        pass
    
    @abstractmethod
    def create_directory(self, directory_path: str) -> bool:
        """Create directory if it doesn't exist."""
        pass
    
    @abstractmethod
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility."""
        pass
    
    @abstractmethod
    def format_video_filename(self, title: str, uploader: str = None) -> str:
        """Format video filename with [Channel] Title pattern."""
        pass
    
    @abstractmethod
    def format_audio_filename(self, title: str, uploader: str = None) -> str:
        """Format audio filename with [Channel] Title pattern."""
        pass
    
    @abstractmethod
    def get_unique_filename(self, directory: str, filename: str) -> str:
        """Get unique filename if file already exists."""
        pass
