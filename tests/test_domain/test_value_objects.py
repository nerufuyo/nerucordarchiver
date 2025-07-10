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
            "https://youtube.com/user/username",
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://music.youtube.com/playlist?list=PLtest",
            "https://music.youtube.com/album/MPREb_1234567890",
            "https://music.youtube.com/browse/MPREb_1234567890"
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
        playlist_urls = [
            "https://youtube.com/playlist?list=PLtest",
            "https://youtube.com/watch?v=test123&list=PLtest",
            "https://music.youtube.com/playlist?list=PLtest",
            "https://music.youtube.com/album/MPREb_1234567890"
        ]
        video_urls = [
            "https://youtube.com/watch?v=test123",
            "https://music.youtube.com/watch?v=test123"
        ]
        
        for url in playlist_urls:
            youtube_url = YouTubeURL(url)
            assert youtube_url.is_playlist() is True, f"Failed for {url}"
        
        for url in video_urls:
            youtube_url = YouTubeURL(url)
            assert youtube_url.is_playlist() is False, f"Failed for {url}"
    
    def test_is_music_youtube(self):
        """Test music.youtube.com detection."""
        music_urls = [
            "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://music.youtube.com/playlist?list=PLtest",
            "https://music.youtube.com/album/MPREb_1234567890"
        ]
        regular_urls = [
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ"
        ]
        
        for url in music_urls:
            youtube_url = YouTubeURL(url)
            assert youtube_url.is_music_youtube() is True, f"Failed for {url}"
        
        for url in regular_urls:
            youtube_url = YouTubeURL(url)
            assert youtube_url.is_music_youtube() is False, f"Failed for {url}"
    
    def test_normalize_url(self):
        """Test URL normalization."""
        test_cases = [
            (
                "https://youtube.com/watch?v=dQw4w9WgXcQ&si=abc123&feature=share",
                "https://youtube.com/watch?v=dQw4w9WgXcQ"
            ),
            (
                "https://music.youtube.com/playlist?list=PLtest&si=xyz789",
                "https://music.youtube.com/playlist?list=PLtest"
            ),
            (
                "https://youtube.com/watch?v=test&utm_source=share&fbclid=test123",
                "https://youtube.com/watch?v=test"
            ),
            (
                "https://youtube.com/watch?v=test",
                "https://youtube.com/watch?v=test"
            )
        ]
        
        for original, expected in test_cases:
            youtube_url = YouTubeURL(original)
            normalized = youtube_url.normalize_url()
            assert normalized == expected, f"Failed for {original}: got {normalized}, expected {expected}"


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
