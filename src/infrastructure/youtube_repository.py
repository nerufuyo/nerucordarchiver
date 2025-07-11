"""
YouTube video repository implementation using yt-dlp.
"""

import yt_dlp
from typing import List, Dict, Any
from ..repositories.interfaces import IVideoRepository
from ..domain.entities import VideoInfo, PlaylistInfo, ChannelInfo
from ..domain.value_objects import YouTubeURL
from ..config.constants import ERROR_VIDEO_NOT_FOUND, ERROR_PLAYLIST_NOT_FOUND


class YouTubeVideoRepository(IVideoRepository):
    """Implementation of video repository using yt-dlp."""
    
    def __init__(self):
        self._ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
    
    async def get_video_info(self, url: YouTubeURL) -> VideoInfo:
        """Get video information from YouTube URL."""
        try:
            with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
                info = ydl.extract_info(url.url, download=False)
                
                if not info:
                    raise RuntimeError(ERROR_VIDEO_NOT_FOUND)
                
                return self._map_to_video_info(info)
                
        except Exception as e:
            raise RuntimeError(f"{ERROR_VIDEO_NOT_FOUND}: {str(e)}")
    
    async def get_playlist_info(self, url: YouTubeURL) -> PlaylistInfo:
        """Get playlist information from YouTube URL."""
        try:
            ydl_opts = {
                **self._ydl_opts,
                'extract_flat': True,  # Only extract metadata, don't download
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.url, download=False)
                
                if not info or 'entries' not in info:
                    raise RuntimeError(ERROR_PLAYLIST_NOT_FOUND)
                
                return self._map_to_playlist_info(info, url.url)
                
        except Exception as e:
            raise RuntimeError(f"{ERROR_PLAYLIST_NOT_FOUND}: {str(e)}")
    
    async def get_channel_info(self, url: YouTubeURL) -> ChannelInfo:
        """Get channel information from YouTube URL."""
        try:
            ydl_opts = {
                **self._ydl_opts,
                'extract_flat': True,  # Only extract metadata, don't download
                'playlistend': 50,  # Limit to first 50 videos for performance
                'ignoreerrors': True,  # Continue on errors
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url.url, download=False)
                
                if not info:
                    raise RuntimeError("Channel not found")
                
                # Handle both channel pages and video listings
                if 'entries' not in info:
                    # This might be a channel page, try to get the videos tab
                    channel_id = info.get('channel_id') or info.get('id')
                    if channel_id:
                        videos_url = f"https://www.youtube.com/channel/{channel_id}/videos"
                        info = ydl.extract_info(videos_url, download=False)
                
                if not info or 'entries' not in info:
                    raise RuntimeError("Channel not found or has no videos")
                
                return self._map_to_channel_info(info, url.url)
                
        except Exception as e:
            raise RuntimeError(f"Error fetching channel info: {str(e)}")
    
    def _map_to_video_info(self, info: Dict[str, Any]) -> VideoInfo:
        """Map yt-dlp info to VideoInfo entity."""
        return VideoInfo(
            title=info.get('title', 'Unknown Title'),
            url=info.get('webpage_url', info.get('url', '')),
            duration=info.get('duration'),
            thumbnail=info.get('thumbnail'),
            uploader=info.get('uploader'),
            view_count=info.get('view_count')
        )
    
    def _map_to_playlist_info(self, info: Dict[str, Any], url: str) -> PlaylistInfo:
        """Map yt-dlp info to PlaylistInfo entity."""
        videos = []
        
        for entry in info.get('entries', []):
            if entry:  # Skip None entries
                video_info = VideoInfo(
                    title=entry.get('title', 'Unknown Title'),
                    url=entry.get('webpage_url', entry.get('url', '')),
                    duration=entry.get('duration'),
                    uploader=entry.get('uploader')
                )
                videos.append(video_info)
        
        return PlaylistInfo(
            title=info.get('title', 'Unknown Playlist'),
            url=url,
            videos=videos,
            uploader=info.get('uploader'),
            video_count=len(videos)
        )
    
    def _map_to_channel_info(self, info: Dict[str, Any], url: str) -> ChannelInfo:
        """Map yt-dlp info to ChannelInfo entity."""
        videos = []
        
        # Limit to first 50 videos to avoid overwhelming the user
        entries = info.get('entries', [])[:50]
        
        for entry in entries:
            if entry:  # Skip None entries
                video_info = VideoInfo(
                    title=entry.get('title', 'Unknown Title'),
                    url=entry.get('webpage_url', entry.get('url', '')),
                    duration=entry.get('duration'),
                    uploader=entry.get('uploader'),
                    view_count=entry.get('view_count')
                )
                videos.append(video_info)
        
        return ChannelInfo(
            title=info.get('title', 'Unknown Channel'),
            url=url,
            videos=videos,
            uploader=info.get('uploader'),
            video_count=len(videos),
            subscriber_count=info.get('subscriber_count')
        )
