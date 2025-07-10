"""
Tests for infrastructure implementations.
"""

import pytest
import os
from unittest.mock import patch, Mock
from src.infrastructure.file_repository import FileSystemRepository


class TestFileSystemRepository:
    """Test cases for FileSystemRepository."""
    
    def test_file_exists_true(self):
        """Test file_exists returns True for existing file."""
        repo = FileSystemRepository()
        
        with patch('os.path.exists', return_value=True):
            assert repo.file_exists("/path/to/file.txt") is True
    
    def test_file_exists_false(self):
        """Test file_exists returns False for non-existing file."""
        repo = FileSystemRepository()
        
        with patch('os.path.exists', return_value=False):
            assert repo.file_exists("/path/to/file.txt") is False
    
    def test_get_file_size_existing_file(self):
        """Test get_file_size for existing file."""
        repo = FileSystemRepository()
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):
            assert repo.get_file_size("/path/to/file.txt") == 1024
    
    def test_get_file_size_non_existing_file(self):
        """Test get_file_size for non-existing file."""
        repo = FileSystemRepository()
        
        with patch('os.path.exists', return_value=False):
            assert repo.get_file_size("/path/to/file.txt") == 0
    
    def test_create_directory_success(self):
        """Test successful directory creation."""
        repo = FileSystemRepository()
        
        with patch('pathlib.Path.mkdir'):
            assert repo.create_directory("/path/to/directory") is True
    
    def test_create_directory_failure(self):
        """Test directory creation failure."""
        repo = FileSystemRepository()
        
        with patch('pathlib.Path.mkdir', side_effect=Exception("Permission denied")):
            assert repo.create_directory("/path/to/directory") is False
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        repo = FileSystemRepository()
        
        # Test invalid characters removal
        assert repo.sanitize_filename("file<name>:with\"invalid|chars") == "file_name__with_invalid_chars"
        
        # Test length limitation
        long_name = "a" * 250
        sanitized = repo.sanitize_filename(long_name)
        assert len(sanitized) <= 200
        
        # Test empty filename
        assert repo.sanitize_filename("") == "unknown_file"
        assert repo.sanitize_filename("   ") == "unknown_file"
        
        # Test leading/trailing spaces and dots
        assert repo.sanitize_filename("  .filename.  ") == "filename"
