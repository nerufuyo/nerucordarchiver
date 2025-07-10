"""
Test configuration for pytest.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_video_info():
    """Fixture for mock video info."""
    from src.domain.entities import VideoInfo
    return VideoInfo(
        title="Test Video",
        url="https://youtube.com/watch?v=test123",
        duration=180,
        uploader="Test Channel",
        view_count=1000
    )


@pytest.fixture
def mock_playlist_info(mock_video_info):
    """Fixture for mock playlist info."""
    from src.domain.entities import PlaylistInfo
    return PlaylistInfo(
        title="Test Playlist",
        url="https://youtube.com/playlist?list=test123",
        videos=[mock_video_info],
        uploader="Test Channel"
    )


@pytest.fixture
def mock_youtube_url():
    """Fixture for mock YouTube URL."""
    from src.domain.value_objects import YouTubeURL
    return YouTubeURL("https://youtube.com/watch?v=test123")


@pytest.fixture
def mock_file_repository():
    """Fixture for mock file repository."""
    from src.repositories.interfaces import IFileRepository
    mock = Mock(spec=IFileRepository)
    mock.file_exists.return_value = False
    mock.get_file_size.return_value = 1024
    mock.create_directory.return_value = True
    mock.sanitize_filename.return_value = "test_video"
    return mock


@pytest.fixture
def mock_video_repository():
    """Fixture for mock video repository."""
    from src.repositories.interfaces import IVideoRepository
    mock = Mock(spec=IVideoRepository)
    mock.get_video_info = AsyncMock()
    mock.get_playlist_info = AsyncMock()
    return mock


@pytest.fixture
def mock_downloader_repository():
    """Fixture for mock downloader repository."""
    from src.repositories.interfaces import IDownloaderRepository
    mock = Mock(spec=IDownloaderRepository)
    mock.download_video = AsyncMock(return_value="/path/to/video.mp4")
    mock.download_audio = AsyncMock(return_value="/path/to/audio.mp3")
    return mock
