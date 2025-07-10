"""
Tests for utility functions.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from src.utils.quality_manager import QualityManager, DownloadResume, get_video_format_options, get_audio_format_options


class TestQualityManager:
    """Test cases for QualityManager."""
    
    def test_default_config(self):
        """Test default configuration values."""
        with patch('pathlib.Path.exists', return_value=False):
            qm = QualityManager()
            assert qm.get_audio_quality() == "192"
            assert qm.get_audio_format() == "mp3"
            assert qm.get_video_quality() == "720p"
            # Output dir should end with NeruCord (platform-specific path)
            assert qm.get_output_dir().endswith("NeruCord")
    
    def test_load_custom_config(self):
        """Test loading custom configuration."""
        config_data = {
            'audio_quality': '320',
            'audio_format': 'flac',
            'video_quality': '1080p',
            'output_dir': '/custom/path'
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
            qm = QualityManager()
            assert qm.get_audio_quality() == "320"
            assert qm.get_audio_format() == "flac"
            assert qm.get_video_quality() == "1080p"
            assert qm.get_output_dir() == "/custom/path"


class TestDownloadResume:
    """Test cases for DownloadResume."""
    
    def test_empty_downloads_file(self):
        """Test behavior with empty downloads file."""
        with patch('pathlib.Path.exists', return_value=False):
            dr = DownloadResume()
            assert not dr.is_downloaded("test_url", "/path")
            assert dr.get_failed_downloads() == []
    
    def test_mark_completed(self):
        """Test marking download as completed."""
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()) as mock_file:
            dr = DownloadResume()
            dr.mark_completed("test_url", "/path", "/file.mp4")
            
            # Check that file was written
            mock_file.assert_called()
            assert not dr.is_downloaded("other_url", "/path")
    
    def test_mark_failed(self):
        """Test marking download as failed."""
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()) as mock_file:
            dr = DownloadResume()
            dr.mark_failed("test_url", "/path", "Error message")
            
            # Check that file was written
            mock_file.assert_called()
            failed = dr.get_failed_downloads()
            assert len(failed) == 1
            assert failed[0]['url'] == "test_url"
            assert failed[0]['error'] == "Error message"
    
    def test_clear_failed(self):
        """Test clearing failed downloads."""
        with patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.open', mock_open()) as mock_file:
            dr = DownloadResume()
            dr.mark_failed("test_url", "/path", "Error")
            dr.clear_failed()
            
            assert dr.get_failed_downloads() == []


class TestFormatOptions:
    """Test cases for format option functions."""
    
    def test_get_video_format_options(self):
        """Test video format options generation."""
        assert get_video_format_options('720p') == 'bestvideo[height<=720]+bestaudio/best'
        assert get_video_format_options('1080p') == 'bestvideo[height<=1080]+bestaudio/best'
        assert get_video_format_options('240p') == 'bestvideo[height<=240]+bestaudio/worst'
        assert get_video_format_options('unknown') == 'bestvideo[height<=720]+bestaudio/best'  # default
    
    def test_get_audio_format_options(self):
        """Test audio format options generation."""
        options = get_audio_format_options('320', 'mp3')
        assert options['key'] == 'FFmpegExtractAudio'
        assert options['preferredcodec'] == 'mp3'
        assert options['preferredquality'] == '320'
        
        options = get_audio_format_options('128', 'flac')
        assert options['preferredcodec'] == 'flac'
        assert options['preferredquality'] == '128'
