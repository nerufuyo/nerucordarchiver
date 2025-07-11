"""
Utilities for file naming and formatting.
"""

import re
import os
from pathlib import Path
from typing import Optional


class FileNameFormatter:
    """Handles file naming conventions and formatting."""
    
    @staticmethod
    def format_filename(title: str, uploader: Optional[str] = None, extension: str = "mp4") -> str:
        """
        Format filename with pattern: [Channel Name] Title.ext
        
        Args:
            title: Video title
            uploader: Channel/uploader name
            extension: File extension
            
        Returns:
            Formatted filename
        """
        # Clean and sanitize title
        clean_title = FileNameFormatter._sanitize_filename(title)
        
        # Format with channel name if available
        if uploader:
            clean_uploader = FileNameFormatter._sanitize_filename(uploader)
            filename = f"[{clean_uploader}] {clean_title}"
        else:
            filename = clean_title
        
        # Ensure extension is included
        if not extension.startswith('.'):
            extension = f".{extension}"
        
        # Limit total length to avoid filesystem issues
        max_length = 255 - len(extension)
        if len(filename) > max_length:
            filename = filename[:max_length].rstrip()
        
        return f"{filename}{extension}"
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for filesystem compatibility.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        filename = re.sub(invalid_chars, '_', filename)
        
        # Remove multiple spaces and trim
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        
        # Handle empty filename
        if not filename:
            filename = "untitled"
        
        return filename
    
    @staticmethod
    def get_unique_filename(directory: str, filename: str) -> str:
        """
        Get unique filename by appending counter if file exists.
        
        Args:
            directory: Target directory
            filename: Desired filename
            
        Returns:
            Unique filename
        """
        base_path = Path(directory)
        file_path = base_path / filename
        
        if not file_path.exists():
            return filename
        
        # Split filename and extension
        stem = file_path.stem
        suffix = file_path.suffix
        
        counter = 1
        while True:
            new_filename = f"{stem}_{counter}{suffix}"
            new_path = base_path / new_filename
            if not new_path.exists():
                return new_filename
            counter += 1
