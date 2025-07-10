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


class YTDLPDownloaderRepository(IDownloaderRepository):
    """Implementation of downloader repository using yt-dlp."""
    
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
    
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
        
        ydl_opts = {
            'format': f'best[height<=720]/{VIDEO_FORMAT}',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook] if progress_callback else [],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([task.video_info.url])
        
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
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook] if progress_callback else [],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': AUDIO_QUALITY,
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([task.video_info.url])
        
        if progress_callback:
            progress_callback(100)  # 100% after conversion
        
        # Find the downloaded audio file
        expected_path = os.path.join(task.output_path, f"{filename}.{AUDIO_FORMAT}")
        if os.path.exists(expected_path):
            return expected_path
        
        # If exact path doesn't exist, find the actual downloaded file
        for file in os.listdir(task.output_path):
            if file.startswith(filename) and file.endswith(f".{AUDIO_FORMAT}"):
                return os.path.join(task.output_path, file)
        
        raise RuntimeError("Downloaded audio file not found")
