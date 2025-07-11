"""
Use cases for the YouTube Archiver application.
"""

from typing import List, Optional, Callable
from ..domain.entities import VideoInfo, PlaylistInfo, ChannelInfo, DownloadTask, DownloadType, DownloadStatus
from ..domain.value_objects import YouTubeURL
from ..repositories.interfaces import IVideoRepository, IDownloaderRepository, IFileRepository
from ..config.constants import ERROR_INVALID_URL, ERROR_DOWNLOAD_FAILED, SUCCESS_DOWNLOAD_COMPLETE


class GetVideoInfoUseCase:
    """Use case for getting video information."""
    
    def __init__(self, video_repository: IVideoRepository):
        self._video_repository = video_repository
    
    async def execute(self, url: str) -> VideoInfo:
        """Execute the use case to get video information."""
        try:
            youtube_url = YouTubeURL(url)
            
            # Check if this is a playlist URL being used with video command
            if youtube_url.is_playlist():
                suggestion = "playlist" if "playlist" in url or "list=" in url else "playlist"
                if youtube_url.is_music_youtube():
                    raise ValueError(
                        f"This appears to be a playlist/album URL from YouTube Music. "
                        f"Please use the '{suggestion}' command instead: "
                        f"python main.py {suggestion} \"{url}\""
                    )
                else:
                    raise ValueError(
                        f"This appears to be a playlist URL. "
                        f"Please use the '{suggestion}' command instead: "
                        f"python main.py {suggestion} \"{url}\""
                    )
            
            # Use normalized URL for better compatibility
            normalized_url = YouTubeURL(youtube_url.normalize_url())
            return await self._video_repository.get_video_info(normalized_url)
        except ValueError as e:
            raise ValueError(f"{ERROR_INVALID_URL}: {str(e)}")


class GetPlaylistInfoUseCase:
    """Use case for getting playlist information."""
    
    def __init__(self, video_repository: IVideoRepository):
        self._video_repository = video_repository
    
    async def execute(self, url: str) -> PlaylistInfo:
        """Execute the use case to get playlist information."""
        try:
            youtube_url = YouTubeURL(url)
            # Use normalized URL for better compatibility
            normalized_url = YouTubeURL(youtube_url.normalize_url())
            return await self._video_repository.get_playlist_info(normalized_url)
        except ValueError as e:
            raise ValueError(f"{ERROR_INVALID_URL}: {str(e)}")


class GetChannelInfoUseCase:
    """Use case for getting channel information."""
    
    def __init__(self, video_repository: IVideoRepository):
        self._video_repository = video_repository
    
    async def execute(self, url: str) -> ChannelInfo:
        """Execute the use case to get channel information."""
        try:
            youtube_url = YouTubeURL(url)
            # Use normalized URL for better compatibility
            normalized_url = YouTubeURL(youtube_url.normalize_url())
            return await self._video_repository.get_channel_info(normalized_url)
        except ValueError as e:
            raise ValueError(f"{ERROR_INVALID_URL}: {str(e)}")


class DownloadVideoUseCase:
    """Use case for downloading video."""
    
    def __init__(
        self, 
        downloader_repository: IDownloaderRepository,
        file_repository: IFileRepository
    ):
        self._downloader_repository = downloader_repository
        self._file_repository = file_repository
    
    async def execute(
        self, 
        video_info: VideoInfo, 
        output_path: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Execute the use case to download video."""
        try:
            # Create directory if it doesn't exist
            self._file_repository.create_directory(output_path)
            
            # Create download task
            task = DownloadTask(
                video_info=video_info,
                download_type=DownloadType.VIDEO,
                output_path=output_path
            )
            
            task.status = DownloadStatus.DOWNLOADING
            file_path = await self._downloader_repository.download_video(task, progress_callback)
            task.mark_completed()
            
            return file_path
        except Exception as e:
            raise RuntimeError(f"{ERROR_DOWNLOAD_FAILED}: {str(e)}")


class DownloadAudioUseCase:
    """Use case for downloading audio."""
    
    def __init__(
        self, 
        downloader_repository: IDownloaderRepository,
        file_repository: IFileRepository
    ):
        self._downloader_repository = downloader_repository
        self._file_repository = file_repository
    
    async def execute(
        self, 
        video_info: VideoInfo, 
        output_path: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Execute the use case to download audio."""
        try:
            # Create directory if it doesn't exist
            self._file_repository.create_directory(output_path)
            
            # Create download task
            task = DownloadTask(
                video_info=video_info,
                download_type=DownloadType.AUDIO,
                output_path=output_path
            )
            
            task.status = DownloadStatus.DOWNLOADING
            file_path = await self._downloader_repository.download_audio(task, progress_callback)
            task.mark_completed()
            
            return file_path
        except Exception as e:
            raise RuntimeError(f"{ERROR_DOWNLOAD_FAILED}: {str(e)}")


class DownloadPlaylistUseCase:
    """Use case for downloading playlist."""
    
    def __init__(
        self,
        video_repository: IVideoRepository,
        downloader_repository: IDownloaderRepository,
        file_repository: IFileRepository
    ):
        self._video_repository = video_repository
        self._downloader_repository = downloader_repository
        self._file_repository = file_repository
    
    async def execute(
        self,
        playlist_url: str,
        download_type: DownloadType,
        output_path: str,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[str]:
        """Execute the use case to download entire playlist."""
        try:
            youtube_url = YouTubeURL(playlist_url)
            playlist_info = await self._video_repository.get_playlist_info(youtube_url)
            
            downloaded_files = []
            total_videos = len(playlist_info.videos)
            
            for index, video_info in enumerate(playlist_info.videos):
                try:
                    if progress_callback:
                        progress_callback(index + 1, total_videos, video_info.title)
                    
                    task = DownloadTask(
                        video_info=video_info,
                        download_type=download_type,
                        output_path=output_path
                    )
                    
                    if download_type == DownloadType.AUDIO:
                        file_path = await self._downloader_repository.download_audio(task)
                    else:
                        file_path = await self._downloader_repository.download_video(task)
                    
                    downloaded_files.append(file_path)
                    
                except Exception as e:
                    # Log error but continue with next video
                    print(f"Failed to download {video_info.title}: {str(e)}")
                    continue
            
            return downloaded_files
            
        except ValueError as e:
            raise ValueError(f"{ERROR_INVALID_URL}: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"{ERROR_DOWNLOAD_FAILED}: {str(e)}")


class DownloadChannelUseCase:
    """Use case for downloading channel videos."""
    
    def __init__(
        self,
        video_repository: IVideoRepository,
        downloader_repository: IDownloaderRepository,
        file_repository: IFileRepository
    ):
        self._video_repository = video_repository
        self._downloader_repository = downloader_repository
        self._file_repository = file_repository
    
    async def execute(
        self,
        channel_url: str,
        download_type: DownloadType,
        output_path: str,
        selected_indices: Optional[List[int]] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[str]:
        """Execute the use case to download channel videos."""
        try:
            youtube_url = YouTubeURL(channel_url)
            channel_info = await self._video_repository.get_channel_info(youtube_url)
            
            # Filter videos by selected indices if provided
            videos_to_download = channel_info.videos
            if selected_indices:
                videos_to_download = [
                    video for i, video in enumerate(channel_info.videos)
                    if i in selected_indices
                ]
            
            downloaded_files = []
            total_videos = len(videos_to_download)
            
            for index, video_info in enumerate(videos_to_download):
                try:
                    if progress_callback:
                        progress_callback(index + 1, total_videos, video_info.title)
                    
                    task = DownloadTask(
                        video_info=video_info,
                        download_type=download_type,
                        output_path=output_path
                    )
                    
                    if download_type == DownloadType.AUDIO:
                        file_path = await self._downloader_repository.download_audio(task)
                    else:
                        file_path = await self._downloader_repository.download_video(task)
                    
                    downloaded_files.append(file_path)
                    
                except Exception as e:
                    # Log error but continue with next video
                    print(f"Failed to download {video_info.title}: {str(e)}")
                    continue
            
            return downloaded_files
            
        except ValueError as e:
            raise ValueError(f"{ERROR_INVALID_URL}: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"{ERROR_DOWNLOAD_FAILED}: {str(e)}")
