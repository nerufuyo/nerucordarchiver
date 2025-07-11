"""
File repository implementation for file system operations.
"""

import os
from pathlib import Path
from ..repositories.interfaces import IFileRepository
from ..utils.file_formatter import FileNameFormatter


class FileSystemRepository(IFileRepository):
    """Implementation of file repository for file system operations."""
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path)
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        if not self.file_exists(file_path):
            return 0
        return os.path.getsize(file_path)
    
    def create_directory(self, directory_path: str) -> bool:
        """Create directory if it doesn't exist."""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility."""
        return FileNameFormatter._sanitize_filename(filename)
    
    def format_video_filename(self, title: str, uploader: str = None) -> str:
        """Format video filename with [Channel] Title pattern."""
        return FileNameFormatter.format_filename(title, uploader, "mp4")
    
    def format_audio_filename(self, title: str, uploader: str = None) -> str:
        """Format audio filename with [Channel] Title pattern."""
        return FileNameFormatter.format_filename(title, uploader, "mp3")
    
    def get_unique_filename(self, directory: str, filename: str) -> str:
        """Get unique filename if file already exists."""
        return FileNameFormatter.get_unique_filename(directory, filename)
