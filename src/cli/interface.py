"""
Command Line Interface for the YouTube Archiver application.
"""

import click
import asyncio
from typing import Optional
from colorama import Fore, Style, init
from ..domain.entities import DownloadType
from ..infrastructure.youtube_repository import YouTubeVideoRepository
from ..infrastructure.downloader_repository import YTDLPDownloaderRepository
from ..infrastructure.file_repository import FileSystemRepository
from ..use_cases.download_use_cases import (
    GetVideoInfoUseCase,
    GetPlaylistInfoUseCase,
    DownloadVideoUseCase,
    DownloadAudioUseCase,
    DownloadPlaylistUseCase
)
from ..config.settings import Config
from ..config.constants import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    SUCCESS_DOWNLOAD_COMPLETE, PROGRESS_DOWNLOADING, PROGRESS_CONVERTING
)

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class CLIInterface:
    """Command Line Interface for YouTube Archiver."""
    
    def __init__(self):
        self.config = Config()
        self.file_repository = FileSystemRepository()
        self.video_repository = YouTubeVideoRepository()
        self.downloader_repository = YTDLPDownloaderRepository(self.file_repository)
        
        # Initialize use cases
        self.get_video_info_use_case = GetVideoInfoUseCase(self.video_repository)
        self.get_playlist_info_use_case = GetPlaylistInfoUseCase(self.video_repository)
        self.download_video_use_case = DownloadVideoUseCase(
            self.downloader_repository, self.file_repository
        )
        self.download_audio_use_case = DownloadAudioUseCase(
            self.downloader_repository, self.file_repository
        )
        self.download_playlist_use_case = DownloadPlaylistUseCase(
            self.video_repository, self.downloader_repository, self.file_repository
        )
    
    def print_banner(self):
        """Print application banner."""
        click.echo(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}")
        click.echo(f"{Fore.CYAN}{Style.BRIGHT}{APP_NAME} v{APP_VERSION}")
        click.echo(f"{Fore.CYAN}{APP_DESCRIPTION}")
        click.echo(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}")
        click.echo()
    
    def print_progress(self, current: int, total: int, item_name: str = ""):
        """Print download progress for playlist."""
        progress_bar = "█" * (current * 20 // total) + "░" * (20 - (current * 20 // total))
        percentage = (current / total) * 100
        click.echo(f"\r{Fore.GREEN}[{progress_bar}] {percentage:.1f}% ({current}/{total}) {item_name}", nl=False)
    
    def print_single_progress(self, progress: float):
        """Print download progress for single item."""
        progress_bar = "█" * int(progress // 5) + "░" * (20 - int(progress // 5))
        click.echo(f"\r{Fore.YELLOW}[{progress_bar}] {progress:.1f}%", nl=False)


@click.group()
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
def cli():
    """NeruCord Archiver - YouTube Video and Audio Downloader."""
    pass


@cli.command()
@click.argument('url')
@click.option('--output', '-o', default=None, help='Output directory path')
def video(url: str, output: Optional[str]):
    """Download YouTube video."""
    interface = CLIInterface()
    interface.print_banner()
    
    async def download_video():
        try:
            click.echo(f"{Fore.BLUE}📹 Getting video information...")
            video_info = await interface.get_video_info_use_case.execute(url)
            
            output_path = output or interface.config.get_video_path()
            
            click.echo(f"{Fore.GREEN}✓ Title: {video_info.title}")
            click.echo(f"{Fore.GREEN}✓ Uploader: {video_info.uploader}")
            if video_info.duration:
                duration = f"{video_info.duration // 60}:{video_info.duration % 60:02d}"
                click.echo(f"{Fore.GREEN}✓ Duration: {duration}")
            click.echo()
            
            click.echo(f"{Fore.YELLOW}{PROGRESS_DOWNLOADING}...")
            file_path = await interface.download_video_use_case.execute(
                video_info, 
                output_path,
                interface.print_single_progress
            )
            click.echo()  # New line after progress bar
            
            click.echo(f"{Fore.GREEN}✅ {SUCCESS_DOWNLOAD_COMPLETE}")
            click.echo(f"{Fore.CYAN}📁 File saved: {file_path}")
            
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Error: {str(e)}")
    
    asyncio.run(download_video())


@cli.command()
@click.argument('url')
@click.option('--output', '-o', default=None, help='Output directory path')
def audio(url: str, output: Optional[str]):
    """Download and convert YouTube video to MP3."""
    interface = CLIInterface()
    interface.print_banner()
    
    async def download_audio():
        try:
            click.echo(f"{Fore.BLUE}🎵 Getting video information...")
            video_info = await interface.get_video_info_use_case.execute(url)
            
            output_path = output or interface.config.get_audio_path()
            
            click.echo(f"{Fore.GREEN}✓ Title: {video_info.title}")
            click.echo(f"{Fore.GREEN}✓ Uploader: {video_info.uploader}")
            if video_info.duration:
                duration = f"{video_info.duration // 60}:{video_info.duration % 60:02d}"
                click.echo(f"{Fore.GREEN}✓ Duration: {duration}")
            click.echo()
            
            click.echo(f"{Fore.YELLOW}{PROGRESS_DOWNLOADING} and converting...")
            file_path = await interface.download_audio_use_case.execute(
                video_info, 
                output_path,
                interface.print_single_progress
            )
            click.echo()  # New line after progress bar
            
            click.echo(f"{Fore.GREEN}✅ {SUCCESS_DOWNLOAD_COMPLETE}")
            click.echo(f"{Fore.CYAN}📁 File saved: {file_path}")
            
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Error: {str(e)}")
    
    asyncio.run(download_audio())


@cli.command()
@click.argument('url')
@click.option('--type', '-t', 'download_type', 
              type=click.Choice(['video', 'audio'], case_sensitive=False),
              default='audio', help='Download type (video or audio)')
@click.option('--output', '-o', default=None, help='Output directory path')
def playlist(url: str, download_type: str, output: Optional[str]):
    """Download entire YouTube playlist."""
    interface = CLIInterface()
    interface.print_banner()
    
    async def download_playlist():
        try:
            click.echo(f"{Fore.BLUE}📋 Getting playlist information...")
            playlist_info = await interface.get_playlist_info_use_case.execute(url)
            
            click.echo(f"{Fore.GREEN}✓ Playlist: {playlist_info.title}")
            click.echo(f"{Fore.GREEN}✓ Videos: {len(playlist_info.videos)}")
            click.echo(f"{Fore.GREEN}✓ Uploader: {playlist_info.uploader}")
            click.echo()
            
            if download_type.lower() == 'video':
                dtype = DownloadType.VIDEO
                output_path = output or interface.config.get_video_path()
            else:
                dtype = DownloadType.AUDIO
                output_path = output or interface.config.get_audio_path()
            
            click.echo(f"{Fore.YELLOW}📥 Downloading playlist as {download_type}...")
            
            def playlist_progress(current: int, total: int, title: str):
                interface.print_progress(current, total, title[:40] + "..." if len(title) > 40 else title)
            
            downloaded_files = await interface.download_playlist_use_case.execute(
                url, dtype, output_path, playlist_progress
            )
            
            click.echo()  # New line after progress bar
            click.echo(f"{Fore.GREEN}✅ Playlist download completed!")
            click.echo(f"{Fore.CYAN}📁 Downloaded {len(downloaded_files)} files to: {output_path}")
            
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Error: {str(e)}")
    
    asyncio.run(download_playlist())


@cli.command()
@click.argument('url')
def info(url: str):
    """Get information about YouTube video or playlist."""
    interface = CLIInterface()
    interface.print_banner()
    
    async def get_info():
        try:
            # Try to get video info first
            try:
                video_info = await interface.get_video_info_use_case.execute(url)
                click.echo(f"{Fore.BLUE}📹 Video Information:")
                click.echo(f"{Fore.GREEN}  Title: {video_info.title}")
                click.echo(f"{Fore.GREEN}  URL: {video_info.url}")
                click.echo(f"{Fore.GREEN}  Uploader: {video_info.uploader}")
                if video_info.duration:
                    duration = f"{video_info.duration // 60}:{video_info.duration % 60:02d}"
                    click.echo(f"{Fore.GREEN}  Duration: {duration}")
                if video_info.view_count:
                    click.echo(f"{Fore.GREEN}  Views: {video_info.view_count:,}")
                
            except:
                # If video info fails, try playlist info
                playlist_info = await interface.get_playlist_info_use_case.execute(url)
                click.echo(f"{Fore.BLUE}📋 Playlist Information:")
                click.echo(f"{Fore.GREEN}  Title: {playlist_info.title}")
                click.echo(f"{Fore.GREEN}  URL: {playlist_info.url}")
                click.echo(f"{Fore.GREEN}  Uploader: {playlist_info.uploader}")
                click.echo(f"{Fore.GREEN}  Videos: {len(playlist_info.videos)}")
                click.echo()
                click.echo(f"{Fore.CYAN}  Video List:")
                for i, video in enumerate(playlist_info.videos[:10], 1):  # Show first 10
                    click.echo(f"{Fore.YELLOW}    {i}. {video.title}")
                if len(playlist_info.videos) > 10:
                    click.echo(f"{Fore.YELLOW}    ... and {len(playlist_info.videos) - 10} more videos")
            
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Error: {str(e)}")
    
    asyncio.run(get_info())


if __name__ == '__main__':
    cli()
