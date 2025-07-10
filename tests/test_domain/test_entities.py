"""
Tests for domain entities.
"""

import pytest
from src.domain.entities import VideoInfo, PlaylistInfo, DownloadTask, DownloadType, DownloadStatus


class TestVideoInfo:
    """Test cases for VideoInfo entity."""
    
    def test_video_info_creation(self):
        """Test VideoInfo creation with valid data."""
        video = VideoInfo(
            title="Test Video",
            url="https://youtube.com/watch?v=test",
            duration=180,
            uploader="Test Channel"
        )
        
        assert video.title == "Test Video"
        assert video.url == "https://youtube.com/watch?v=test"
        assert video.duration == 180
        assert video.uploader == "Test Channel"
    
    def test_video_info_empty_url_raises_error(self):
        """Test that empty URL raises ValueError."""
        with pytest.raises(ValueError, match="URL cannot be empty"):
            VideoInfo(title="Test", url="")
    
    def test_video_info_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            VideoInfo(title="", url="https://youtube.com/watch?v=test")


class TestPlaylistInfo:
    """Test cases for PlaylistInfo entity."""
    
    def test_playlist_info_creation(self, mock_video_info):
        """Test PlaylistInfo creation with valid data."""
        playlist = PlaylistInfo(
            title="Test Playlist",
            url="https://youtube.com/playlist?list=test",
            videos=[mock_video_info],
            uploader="Test Channel"
        )
        
        assert playlist.title == "Test Playlist"
        assert playlist.url == "https://youtube.com/playlist?list=test"
        assert len(playlist.videos) == 1
        assert playlist.video_count == 1
        assert playlist.uploader == "Test Channel"
    
    def test_playlist_info_empty_url_raises_error(self, mock_video_info):
        """Test that empty URL raises ValueError."""
        with pytest.raises(ValueError, match="Playlist URL cannot be empty"):
            PlaylistInfo(title="Test", url="", videos=[mock_video_info])
    
    def test_playlist_info_empty_title_raises_error(self, mock_video_info):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Playlist title cannot be empty"):
            PlaylistInfo(title="", url="https://youtube.com/playlist?list=test", videos=[mock_video_info])


class TestDownloadTask:
    """Test cases for DownloadTask entity."""
    
    def test_download_task_creation(self, mock_video_info):
        """Test DownloadTask creation with valid data."""
        task = DownloadTask(
            video_info=mock_video_info,
            download_type=DownloadType.VIDEO,
            output_path="/downloads"
        )
        
        assert task.video_info == mock_video_info
        assert task.download_type == DownloadType.VIDEO
        assert task.output_path == "/downloads"
        assert task.status == DownloadStatus.PENDING
        assert task.progress == 0.0
    
    def test_update_progress_valid(self, mock_video_info):
        """Test updating progress with valid values."""
        task = DownloadTask(
            video_info=mock_video_info,
            download_type=DownloadType.AUDIO,
            output_path="/downloads"
        )
        
        task.update_progress(50.0)
        assert task.progress == 50.0
        
        task.update_progress(100.0)
        assert task.progress == 100.0
    
    def test_update_progress_invalid_raises_error(self, mock_video_info):
        """Test that invalid progress values raise ValueError."""
        task = DownloadTask(
            video_info=mock_video_info,
            download_type=DownloadType.AUDIO,
            output_path="/downloads"
        )
        
        with pytest.raises(ValueError, match="Progress must be between 0 and 100"):
            task.update_progress(-10)
        
        with pytest.raises(ValueError, match="Progress must be between 0 and 100"):
            task.update_progress(110)
    
    def test_mark_completed(self, mock_video_info):
        """Test marking task as completed."""
        task = DownloadTask(
            video_info=mock_video_info,
            download_type=DownloadType.VIDEO,
            output_path="/downloads"
        )
        
        task.mark_completed()
        assert task.status == DownloadStatus.COMPLETED
        assert task.progress == 100.0
    
    def test_mark_failed(self, mock_video_info):
        """Test marking task as failed."""
        task = DownloadTask(
            video_info=mock_video_info,
            download_type=DownloadType.VIDEO,
            output_path="/downloads"
        )
        
        error_msg = "Download failed"
        task.mark_failed(error_msg)
        assert task.status == DownloadStatus.FAILED
        assert task.error_message == error_msg
