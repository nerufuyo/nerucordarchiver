"""
Enhanced CLI commands for batch operations and configuration management.
"""

import click
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any
from colorama import Fore, Style
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
from ..config.constants import APP_NAME


class BatchDownloader:
    """Extended CLI interface for batch operations."""
    
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
        click.echo(f"{Fore.CYAN}{Style.BRIGHT}{APP_NAME} - Batch Operations")
        click.echo(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}")
        click.echo()
    
    def print_progress(self, current: int, total: int, item_name: str = ""):
        """Print download progress for playlist."""
        progress_bar = "█" * (current * 20 // total) + "░" * (20 - (current * 20 // total))
        percentage = (current / total) * 100
        click.echo(f"\r{Fore.GREEN}[{progress_bar}] {percentage:.1f}% ({current}/{total}) {item_name}", nl=False)
    
    async def download_from_file(self, file_path: str, download_type: str, output_path: str = None):
        """Download videos from a file containing URLs."""
        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                click.echo(f"{Fore.RED}❌ No valid URLs found in file")
                return
            
            click.echo(f"{Fore.BLUE}📋 Found {len(urls)} URLs to download")
            click.echo()
            
            dtype = DownloadType.VIDEO if download_type.lower() == 'video' else DownloadType.AUDIO
            output_dir = output_path or (self.config.get_video_path() if download_type.lower() == 'video' else self.config.get_audio_path())
            
            success_count = 0
            failed_urls = []
            
            for i, url in enumerate(urls, 1):
                try:
                    click.echo(f"{Fore.YELLOW}[{i}/{len(urls)}] Processing: {url[:50]}...")
                    
                    # Check if it's a playlist
                    if 'playlist' in url or 'list=' in url:
                        await self.download_playlist_use_case.execute(
                            url, dtype, output_dir, 
                            lambda current, total, title: self.print_progress(current, total, title)
                        )
                    else:
                        video_info = await self.get_video_info_use_case.execute(url)
                        
                        if dtype == DownloadType.AUDIO:
                            await self.download_audio_use_case.execute(video_info, output_dir)
                        else:
                            await self.download_video_use_case.execute(video_info, output_dir)
                    
                    success_count += 1
                    click.echo(f"{Fore.GREEN}✅ Completed")
                    
                except Exception as e:
                    failed_urls.append((url, str(e)))
                    click.echo(f"{Fore.RED}❌ Failed: {str(e)}")
                
                click.echo()
            
            # Summary
            click.echo(f"{Fore.CYAN}{'='*60}")
            click.echo(f"{Fore.GREEN}✅ Successfully downloaded: {success_count}/{len(urls)}")
            
            if failed_urls:
                click.echo(f"{Fore.RED}❌ Failed downloads: {len(failed_urls)}")
                for url, error in failed_urls:
                    click.echo(f"{Fore.RED}   {url}: {error}")
            
        except FileNotFoundError:
            click.echo(f"{Fore.RED}❌ File not found: {file_path}")
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Error reading file: {str(e)}")


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--type', '-t', 'download_type', 
              type=click.Choice(['video', 'audio'], case_sensitive=False),
              default='audio', help='Download type (video or audio)')
@click.option('--output', '-o', default=None, help='Output directory path')
def batch(file_path: str, download_type: str, output: str):
    """Download multiple videos from a file containing URLs (one per line)."""
    downloader = BatchDownloader()
    downloader.print_banner()
    
    asyncio.run(downloader.download_from_file(file_path, download_type, output))


@click.command()
@click.option('--quality', '-q', default=None, help='Set default audio quality (e.g., 192, 320)')
@click.option('--format', '-f', default=None, help='Set default audio format (mp3, wav, flac)')
@click.option('--video-quality', default=None, help='Set default video quality (720p, 1080p)')
@click.option('--output-dir', default=None, help='Set default output directory')
@click.option('--show', is_flag=True, help='Show current configuration')
def config(quality: str, format: str, video_quality: str, output_dir: str, show: bool):
    """Manage application configuration."""
    config_file = Path.home() / '.nerucord' / 'config.json'
    config_file.parent.mkdir(exist_ok=True)
    
    # Load existing config
    current_config = {}
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                current_config = json.load(f)
        except:
            pass
    
    if show:
        click.echo(f"{Fore.CYAN}Current Configuration:")
        click.echo(f"{Fore.GREEN}  Audio Quality: {current_config.get('audio_quality', '192')} kbps")
        click.echo(f"{Fore.GREEN}  Audio Format: {current_config.get('audio_format', 'mp3')}")
        click.echo(f"{Fore.GREEN}  Video Quality: {current_config.get('video_quality', '720p')}")
        click.echo(f"{Fore.GREEN}  Output Directory: {current_config.get('output_dir', './downloads')}")
        return
    
    # Update config
    if quality:
        current_config['audio_quality'] = quality
        click.echo(f"{Fore.GREEN}✓ Audio quality set to: {quality} kbps")
    
    if format:
        current_config['audio_format'] = format
        click.echo(f"{Fore.GREEN}✓ Audio format set to: {format}")
    
    if video_quality:
        current_config['video_quality'] = video_quality
        click.echo(f"{Fore.GREEN}✓ Video quality set to: {video_quality}")
    
    if output_dir:
        current_config['output_dir'] = output_dir
        click.echo(f"{Fore.GREEN}✓ Output directory set to: {output_dir}")
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(current_config, f, indent=2)
    
    if any([quality, format, video_quality, output_dir]):
        click.echo(f"{Fore.CYAN}Configuration saved to: {config_file}")


# Register new commands with the main CLI
def register_enhanced_commands(cli_group):
    """Register enhanced commands with the main CLI group."""
    cli_group.add_command(batch)
    cli_group.add_command(config)
