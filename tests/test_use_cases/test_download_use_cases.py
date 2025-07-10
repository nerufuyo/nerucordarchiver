"""
Tests for use cases.
"""

import pytest
from unittest.mock import AsyncMock
from src.use_cases.download_use_cases import (
    GetVideoInfoUseCase,
    GetPlaylistInfoUseCase,
    DownloadVideoUseCase,
    DownloadAudioUseCase
)
from src.domain.entities import DownloadType


class TestGetVideoInfoUseCase:
    """Test cases for GetVideoInfoUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_success(self, mock_video_repository, mock_video_info):
        """Test successful video info retrieval."""
        mock_video_repository.get_video_info.return_value = mock_video_info
        use_case = GetVideoInfoUseCase(mock_video_repository)
        
        result = await use_case.execute("https://youtube.com/watch?v=test123")
        
        assert result == mock_video_info
        mock_video_repository.get_video_info.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_invalid_url_raises_error(self, mock_video_repository):
        """Test that invalid URL raises ValueError."""
        use_case = GetVideoInfoUseCase(mock_video_repository)
        
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            await use_case.execute("invalid_url")


class TestGetPlaylistInfoUseCase:
    """Test cases for GetPlaylistInfoUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_success(self, mock_video_repository, mock_playlist_info):
        """Test successful playlist info retrieval."""
        mock_video_repository.get_playlist_info.return_value = mock_playlist_info
        use_case = GetPlaylistInfoUseCase(mock_video_repository)
        
        result = await use_case.execute("https://youtube.com/playlist?list=test123")
        
        assert result == mock_playlist_info
        mock_video_repository.get_playlist_info.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_invalid_url_raises_error(self, mock_video_repository):
        """Test that invalid URL raises ValueError."""
        use_case = GetPlaylistInfoUseCase(mock_video_repository)
        
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            await use_case.execute("invalid_url")


class TestDownloadVideoUseCase:
    """Test cases for DownloadVideoUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_success(
        self, 
        mock_downloader_repository, 
        mock_file_repository, 
        mock_video_info
    ):
        """Test successful video download."""
        expected_path = "/downloads/video.mp4"
        mock_downloader_repository.download_video.return_value = expected_path
        
        use_case = DownloadVideoUseCase(mock_downloader_repository, mock_file_repository)
        
        result = await use_case.execute(mock_video_info, "/downloads")
        
        assert result == expected_path
        mock_file_repository.create_directory.assert_called_once_with("/downloads")
        mock_downloader_repository.download_video.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_download_failure_raises_error(
        self, 
        mock_downloader_repository, 
        mock_file_repository, 
        mock_video_info
    ):
        """Test that download failure raises RuntimeError."""
        mock_downloader_repository.download_video.side_effect = Exception("Download failed")
        
        use_case = DownloadVideoUseCase(mock_downloader_repository, mock_file_repository)
        
        with pytest.raises(RuntimeError, match="Download failed for the provided URL"):
            await use_case.execute(mock_video_info, "/downloads")


class TestDownloadAudioUseCase:
    """Test cases for DownloadAudioUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_success(
        self, 
        mock_downloader_repository, 
        mock_file_repository, 
        mock_video_info
    ):
        """Test successful audio download."""
        expected_path = "/downloads/audio.mp3"
        mock_downloader_repository.download_audio.return_value = expected_path
        
        use_case = DownloadAudioUseCase(mock_downloader_repository, mock_file_repository)
        
        result = await use_case.execute(mock_video_info, "/downloads")
        
        assert result == expected_path
        mock_file_repository.create_directory.assert_called_once_with("/downloads")
        mock_downloader_repository.download_audio.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_download_failure_raises_error(
        self, 
        mock_downloader_repository, 
        mock_file_repository, 
        mock_video_info
    ):
        """Test that download failure raises RuntimeError."""
        mock_downloader_repository.download_audio.side_effect = Exception("Download failed")
        
        use_case = DownloadAudioUseCase(mock_downloader_repository, mock_file_repository)
        
        with pytest.raises(RuntimeError, match="Download failed for the provided URL"):
            await use_case.execute(mock_video_info, "/downloads")
