"""
File repository implementation for file system operations.
"""

import os
import re
from pathlib import Path
from ..repositories.interfaces import IFileRepository
from ..config.constants import MAX_FILENAME_LENGTH


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
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        
        # Limit filename length
        if len(sanitized) > MAX_FILENAME_LENGTH:
            sanitized = sanitized[:MAX_FILENAME_LENGTH]
        
        # Ensure filename is not empty
        if not sanitized:
            sanitized = "unknown_file"
        
        return sanitized
