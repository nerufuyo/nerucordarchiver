"""
Downloader repository implementation using yt-dlp.
"""

import yt_dlp
import os
from typing import Optional, Callable
from pathlib import Path
from ..repositories.interfaces import IDownloaderRepository, IFileRepository
from ..domain.entities import DownloadTask, DownloadType
from ..config.constants import AUDIO_FORMAT, VIDEO_FORMAT, AUDIO_QUALITY
from ..utils.quality_manager import QualityManager, get_video_format_options, get_audio_format_options


class YTDLPDownloaderRepository(IDownloaderRepository):
    """Implementation of downloader repository using yt-dlp."""
    
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
        self._quality_manager = QualityManager()
    
    async def download_video(
        self, 
        task: DownloadTask, 
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Download video file using yt-dlp."""
        
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_callback(progress)
                elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                    progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                    progress_callback(progress)
        
        filename = self._file_repository.sanitize_filename(task.video_info.title)
        output_template = os.path.join(task.output_path, f"{filename}.%(ext)s")
        
        video_quality = self._quality_manager.get_video_quality()
        format_string = get_video_format_options(video_quality)
        
        ydl_opts = {
            'format': format_string,
            'outtmpl': output_template,
            'progress_hooks': [progress_hook] if progress_callback else [],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls']
                }
            },
            'socket_timeout': 60,
            'retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([task.video_info.url])
        except Exception as e:
            # If specific format fails, try with video+audio merge approach
            if "Requested format is not available" in str(e) or "format" in str(e).lower():
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([task.video_info.url])
                except Exception as e2:
                    # If that fails too, let yt-dlp auto-select without format restrictions
                    del ydl_opts['format']
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([task.video_info.url])
                    except Exception as e3:
                        raise e3
            else:
                raise e
        
        # Find the downloaded file
        expected_path = os.path.join(task.output_path, f"{filename}.{VIDEO_FORMAT}")
        if os.path.exists(expected_path):
            return expected_path
        
        # If exact path doesn't exist, find the actual downloaded file
        for file in os.listdir(task.output_path):
            if file.startswith(filename):
                return os.path.join(task.output_path, file)
        
        raise RuntimeError("Downloaded file not found")
    
    async def download_audio(
        self, 
        task: DownloadTask, 
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Download and convert to audio file using yt-dlp."""
        
        def progress_hook(d):
            if progress_callback:
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        progress = (d['downloaded_bytes'] / d['total_bytes']) * 50  # 50% for download
                        progress_callback(progress)
                    elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                        progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 50
                        progress_callback(progress)
                elif d['status'] == 'finished':
                    progress_callback(75)  # 75% after download, before conversion
        
        filename = self._file_repository.sanitize_filename(task.video_info.title)
        output_template = os.path.join(task.output_path, f"{filename}.%(ext)s")
        
        audio_quality = self._quality_manager.get_audio_quality()
        audio_format = self._quality_manager.get_audio_format()
        audio_postprocessor = get_audio_format_options(audio_quality, audio_format)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook] if progress_callback else [],
            'postprocessors': [audio_postprocessor],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls']
                }
            },
            'socket_timeout': 60,
            'retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([task.video_info.url])
        
        if progress_callback:
            progress_callback(100)  # 100% after conversion
        
        # Find the downloaded audio file
        audio_format = self._quality_manager.get_audio_format()
        expected_path = os.path.join(task.output_path, f"{filename}.{audio_format}")
        if os.path.exists(expected_path):
            return expected_path
        
        # If exact path doesn't exist, find the actual downloaded file
        for file in os.listdir(task.output_path):
            if file.startswith(filename) and file.endswith(f".{audio_format}"):
                return os.path.join(task.output_path, file)
        
        raise RuntimeError("Downloaded audio file not found")
