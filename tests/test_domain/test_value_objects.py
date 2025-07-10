"""
Tests for domain value objects.
"""

import pytest
from src.domain.value_objects import YouTubeURL, FilePath, Quality


class TestYouTubeURL:
    """Test cases for YouTubeURL value object."""
    
    def test_valid_youtube_urls(self):
        """Test valid YouTube URLs."""
        valid_urls = [
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtube.com/playlist?list=PLrAXtmRdnEQy4QpM-dvBETukrNfwQs72x",
            "https://youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw",
            "https://youtube.com/user/username"
        ]
        
        for url in valid_urls:
            youtube_url = YouTubeURL(url)
            assert youtube_url.url == url
    
    def test_invalid_youtube_urls_raise_error(self):
        """Test that invalid URLs raise ValueError."""
        invalid_urls = [
            "https://vimeo.com/123456",
            "https://twitch.tv/channel",
            "not_a_url",
            "",
            "https://example.com"
        ]
        
        for url in invalid_urls:
            with pytest.raises(ValueError, match="Invalid YouTube URL"):
                YouTubeURL(url)
    
    def test_is_playlist(self):
        """Test playlist detection."""
        playlist_url = YouTubeURL("https://youtube.com/playlist?list=PLtest")
        video_url = YouTubeURL("https://youtube.com/watch?v=test123")
        
        assert playlist_url.is_playlist() is True
        assert video_url.is_playlist() is False
    
    def test_is_channel(self):
        """Test channel detection."""
        channel_url = YouTubeURL("https://youtube.com/channel/UCtest")
        user_url = YouTubeURL("https://youtube.com/user/testuser")
        video_url = YouTubeURL("https://youtube.com/watch?v=test123")
        
        assert channel_url.is_channel() is True
        assert user_url.is_channel() is True
        assert video_url.is_channel() is False


class TestFilePath:
    """Test cases for FilePath value object."""
    
    def test_valid_file_path(self):
        """Test valid file path creation."""
        path = FilePath("/downloads/video.mp4")
        assert path.path == "/downloads/video.mp4"
    
    def test_empty_path_raises_error(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError, match="File path cannot be empty"):
            FilePath("")
        
        with pytest.raises(ValueError, match="File path cannot be empty"):
            FilePath("   ")
    
    def test_get_extension(self):
        """Test getting file extension."""
        path = FilePath("/downloads/video.mp4")
        assert path.get_extension() == "mp4"
        
        path_no_ext = FilePath("/downloads/video")
        assert path_no_ext.get_extension() == ""
    
    def test_get_filename(self):
        """Test getting filename without path."""
        path = FilePath("/downloads/subfolder/video.mp4")
        assert path.get_filename() == "video.mp4"
        
        path_no_folder = FilePath("video.mp4")
        assert path_no_folder.get_filename() == "video.mp4"


class TestQuality:
    """Test cases for Quality value object."""
    
    def test_valid_quality_string(self):
        """Test valid quality string."""
        quality = Quality("720p")
        assert quality.value == "720p"
        assert str(quality) == "720p"
    
    def test_valid_quality_int(self):
        """Test valid quality integer."""
        quality = Quality(192)
        assert quality.value == 192
        assert str(quality) == "192"
    
    def test_empty_quality_raises_error(self):
        """Test that empty quality raises ValueError."""
        with pytest.raises(ValueError, match="Quality value cannot be empty"):
            Quality("")
        
        with pytest.raises(ValueError, match="Quality value cannot be empty"):
            Quality(None)
