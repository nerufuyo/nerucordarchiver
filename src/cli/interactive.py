"""
Interactive CLI interface for NeruCord Archiver.
Provides a professional menu-driven interface for users.
"""

import asyncio
from typing import Optional, List

from .base import BaseInterface, ProgressDisplay, ValidationHelper
from .interface import CLIInterface
from ..config.constants import APP_NAME, APP_VERSION
from ..domain.entities import DownloadType


class InteractiveCLI(BaseInterface):
    """Interactive command-line interface for NeruCord Archiver."""
    
    def __init__(self):
        super().__init__()
        self.cli_interface = CLIInterface()
    
    def print_welcome(self):
        """Print welcome message and banner."""
        self.clear_screen()
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ███╗   ██╗███████╗██████╗ ██╗   ██╗ ██████╗ ██████╗ ██████╗ ██████╗       ║
║  ████╗  ██║██╔════╝██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔══██╗██╔══██╗      ║
║  ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██║     ██║   ██║██████╔╝██║  ██║      ║
║  ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██║     ██║   ██║██╔══██╗██║  ██║      ║
║  ██║ ╚████║███████╗██║  ██║╚██████╔╝╚██████╗╚██████╔╝██║  ██║██████╔╝      ║
║  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝       ║
║                                                                              ║
║  YouTube Video & Audio Downloader                     v{APP_VERSION}              ║
║  Professional tool for media archival and conversion                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    def print_main_menu(self):
        """Print the main menu options."""
        print("""
┌─ MAIN MENU ─────────────────────────────────────────────────────────────────┐
│                                                                             │
│  1. Download Video                                                          │
│  2. Download Audio (MP3)                                                    │
│  3. Download Playlist                                                       │
│  4. Browse Channel Videos                                                   │
│  5. Download from Channel                                                   │
│  6. Batch Download from File                                                │
│  7. Get Video/Playlist Info                                                 │
│  8. Settings & Configuration                                                │
│  9. Help & Examples                                                         │
│  0. Exit                                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")
    
    def get_download_type(self) -> str:
        """Get download type choice from user."""
        print("Download type:")
        print("  1. Audio (MP3)")
        print("  2. Video (MP4)")
        choice = self.get_choice("Choose type (1-2): ", ['1', '2'])
        return 'audio' if choice == '1' else 'video'
    
    def get_selection_input(self, max_videos: int) -> Optional[List[int]]:
        """Get video selection from user."""
        print("Selection options:")
        print("  1. Download all videos")
        print("  2. Select specific videos")
        choice = self.get_choice("Choose option (1-2): ", ['1', '2'])
        
        if choice == '1':
            return None  # Download all
        else:
            return self.get_specific_selection(max_videos)
    
    def get_specific_selection(self, max_videos: int) -> List[int]:
        """Get specific video selection from user."""
        while True:
            print("Selection format examples:")
            print("  • Single videos: 1,3,5")
            print("  • Ranges: 1-10")
            print("  • Mixed: 1,3,5-10,15")
            
            selection = self.get_input(f"Enter selection (1-{max_videos}): ")
            indices = ValidationHelper.parse_selection(selection, max_videos)
            if indices is not None:
                return indices
            self.print_error("Invalid selection format or range. Please try again.")
    
    def print_help(self):
        """Print help and examples."""
        print("""
┌─ HELP & EXAMPLES ───────────────────────────────────────────────────────────┐
│                                                                             │
│  Supported URL formats:                                                     │
│                                                                             │
│  Videos:                                                                    │
│    • https://youtube.com/watch?v=VIDEO_ID                                  │
│    • https://youtu.be/VIDEO_ID                                             │
│                                                                             │
│  Playlists:                                                                 │
│    • https://youtube.com/playlist?list=PLAYLIST_ID                         │
│                                                                             │
│  Channels:                                                                  │
│    • https://youtube.com/@channelname/videos                               │
│    • https://youtube.com/channel/CHANNEL_ID/videos                         │
│    • https://youtube.com/user/USERNAME/videos                              │
│                                                                             │
│  YouTube Music:                                                             │
│    • https://music.youtube.com/watch?v=VIDEO_ID                            │
│    • https://music.youtube.com/playlist?list=PLAYLIST_ID                   │
│                                                                             │
│  Tips:                                                                      │
│    • Use Browse Channel first to see available videos                      │
│    • Selection format: 1,3,5 or 1-10 or 1,3,5-10,15                       │
│    • Default downloads go to ~/Downloads/NeruCord/                          │
│    • Some videos may fail if they're private or members-only               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")
    
    async def handle_download_video(self):
        """Handle video download option."""
        self.print_header("DOWNLOAD VIDEO")
        
        url = self.get_input("Enter video URL: ")
        output_path = self.get_input("Output directory (press Enter for default): ", required=False)
        
        try:
            self.print_info("Getting video information...")
            video_info = await self.cli_interface.get_video_info_use_case.execute(url)
            
            output_dir = output_path or self.cli_interface.config.get_video_path()
            
            self.print_success(f"Title: {video_info.title}")
            self.print_success(f"Uploader: {video_info.uploader}")
            if video_info.duration:
                duration = ValidationHelper.format_duration(video_info.duration)
                self.print_success(f"Duration: {duration}")
            
            print("\nDownloading video...")
            file_path = await self.cli_interface.download_video_use_case.execute(
                video_info, output_dir, ProgressDisplay.show_single_progress
            )
            
            print("\n")
            self.print_success("Download completed successfully!")
            print(f"File saved: {file_path}")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_download_audio(self):
        """Handle audio download option."""
        self.print_header("DOWNLOAD AUDIO")
        
        url = self.get_input("Enter video URL: ")
        output_path = self.get_input("Output directory (press Enter for default): ", required=False)
        
        try:
            self.print_info("Getting video information...")
            video_info = await self.cli_interface.get_video_info_use_case.execute(url)
            
            output_dir = output_path or self.cli_interface.config.get_audio_path()
            
            self.print_success(f"Title: {video_info.title}")
            self.print_success(f"Uploader: {video_info.uploader}")
            if video_info.duration:
                duration = ValidationHelper.format_duration(video_info.duration)
                self.print_success(f"Duration: {duration}")
            
            print("\nDownloading and converting to audio...")
            file_path = await self.cli_interface.download_audio_use_case.execute(
                video_info, output_dir, ProgressDisplay.show_single_progress
            )
            
            print("\n")
            self.print_success("Download completed successfully!")
            print(f"File saved: {file_path}")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_download_playlist(self):
        """Handle playlist download option."""
        self.print_header("DOWNLOAD PLAYLIST")
        
        url = self.get_input("Enter playlist URL: ")
        download_type = self.get_download_type()
        output_path = self.get_input("Output directory (press Enter for default): ", required=False)
        
        try:
            self.print_info("Getting playlist information...")
            playlist_info = await self.cli_interface.get_playlist_info_use_case.execute(url)
            
            self.print_success(f"Playlist: {playlist_info.title}")
            self.print_success(f"Videos: {len(playlist_info.videos)}")
            self.print_success(f"Uploader: {playlist_info.uploader}")
            
            if download_type == 'video':
                dtype = DownloadType.VIDEO
                output_dir = output_path or self.cli_interface.config.get_video_path()
            else:
                dtype = DownloadType.AUDIO
                output_dir = output_path or self.cli_interface.config.get_audio_path()
            
            print(f"\nDownloading playlist as {download_type}...")
            
            downloaded_files = await self.cli_interface.download_playlist_use_case.execute(
                url, dtype, output_dir, ProgressDisplay.show_progress
            )
            
            print("\n")
            self.print_success("Playlist download completed!")
            print(f"Downloaded {len(downloaded_files)} files to: {output_dir}")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_browse_channel(self):
        """Handle channel browsing option."""
        self.print_header("BROWSE CHANNEL")
        
        url = self.get_input("Enter channel URL: ")
        
        try:
            self.print_info("Getting channel information...")
            channel_info = await self.cli_interface.get_channel_info_use_case.execute(url)
            
            self.print_success(f"Channel: {channel_info.title}")
            self.print_success(f"Videos: {len(channel_info.videos)}")
            if channel_info.subscriber_count:
                subscriber_count = ValidationHelper.format_count(channel_info.subscriber_count)
                self.print_success(f"Subscribers: {subscriber_count}")
            
            print("\nAvailable Videos:")
            for i, video in enumerate(channel_info.videos, 1):
                duration = ""
                if video.duration:
                    duration = f" ({ValidationHelper.format_duration(video.duration)})"
                views = ""
                if video.view_count:
                    views = f" | {ValidationHelper.format_count(video.view_count)} views"
                print(f"  {i:2d}. {video.title}{duration}{views}")
            
            print("\nUse 'Download from Channel' option to download selected videos.")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_channel_download(self):
        """Handle channel download option."""
        self.print_header("DOWNLOAD FROM CHANNEL")
        
        url = self.get_input("Enter channel URL: ")
        
        try:
            self.print_info("Getting channel information...")
            channel_info = await self.cli_interface.get_channel_info_use_case.execute(url)
            
            self.print_success(f"Channel: {channel_info.title}")
            self.print_success(f"Videos: {len(channel_info.videos)}")
            
            # Show first 10 videos for reference
            print("\nAvailable Videos (showing first 10):")
            for i, video in enumerate(channel_info.videos[:10], 1):
                duration = ""
                if video.duration:
                    duration = f" ({ValidationHelper.format_duration(video.duration)})"
                print(f"  {i:2d}. {video.title}{duration}")
            
            if len(channel_info.videos) > 10:
                print(f"  ... and {len(channel_info.videos) - 10} more videos")
            
            # Get selection
            selected_indices = self.get_selection_input(len(channel_info.videos))
            download_type = self.get_download_type()
            output_path = self.get_input("Output directory (press Enter for default): ", required=False)
            
            if download_type == 'video':
                dtype = DownloadType.VIDEO
                output_dir = output_path or self.cli_interface.config.get_video_path()
            else:
                dtype = DownloadType.AUDIO
                output_dir = output_path or self.cli_interface.config.get_audio_path()
            
            print(f"\nDownloading channel videos as {download_type}...")
            
            downloaded_files = await self.cli_interface.download_channel_use_case.execute(
                url, dtype, output_dir, selected_indices, ProgressDisplay.show_progress
            )
            
            print("\n")
            self.print_success("Channel download completed!")
            print(f"Downloaded {len(downloaded_files)} files to: {output_dir}")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_batch_download(self):
        """Handle batch download option."""
        self.print_header("BATCH DOWNLOAD")
        
        file_path = self.get_input("Enter file path containing URLs: ")
        download_type = self.get_download_type()
        output_path = self.get_input("Output directory (press Enter for default): ", required=False)
        
        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                self.print_error("No valid URLs found in file")
                return
            
            self.print_info(f"Found {len(urls)} URLs to download")
            
            dtype = DownloadType.VIDEO if download_type == 'video' else DownloadType.AUDIO
            output_dir = output_path or (
                self.cli_interface.config.get_video_path() if download_type == 'video' 
                else self.cli_interface.config.get_audio_path()
            )
            
            success_count = 0
            failed_urls = []
            
            for i, url in enumerate(urls, 1):
                try:
                    print(f"\n[{i}/{len(urls)}] Processing: {url[:50]}...")
                    
                    if 'playlist' in url or 'list=' in url:
                        await self.cli_interface.download_playlist_use_case.execute(
                            url, dtype, output_dir, ProgressDisplay.show_progress
                        )
                    else:
                        video_info = await self.cli_interface.get_video_info_use_case.execute(url)
                        
                        if dtype == DownloadType.AUDIO:
                            await self.cli_interface.download_audio_use_case.execute(video_info, output_dir)
                        else:
                            await self.cli_interface.download_video_use_case.execute(video_info, output_dir)
                    
                    success_count += 1
                    self.print_success("Completed")
                    
                except Exception as e:
                    failed_urls.append(url)
                    self.print_error(f"Failed: {str(e)}")
            
            print("\n")
            self.print_success("Batch download completed!")
            print(f"Successfully downloaded: {success_count}/{len(urls)} files")
            
            if failed_urls:
                self.print_warning(f"Failed URLs: {len(failed_urls)}")
                for url in failed_urls:
                    print(f"  • {url}")
            
        except FileNotFoundError:
            self.print_error(f"File not found: {file_path}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    async def handle_get_info(self):
        """Handle get info option."""
        self.print_header("GET INFO")
        
        url = self.get_input("Enter video/playlist URL: ")
        
        try:
            # Try to get video info first
            try:
                video_info = await self.cli_interface.get_video_info_use_case.execute(url)
                print("\nVideo Information:")
                print(f"  Title: {video_info.title}")
                print(f"  URL: {video_info.url}")
                print(f"  Uploader: {video_info.uploader}")
                if video_info.duration:
                    duration = ValidationHelper.format_duration(video_info.duration)
                    print(f"  Duration: {duration}")
                if video_info.view_count:
                    views = ValidationHelper.format_count(video_info.view_count)
                    print(f"  Views: {views}")
                
            except:
                # If video info fails, try playlist info
                playlist_info = await self.cli_interface.get_playlist_info_use_case.execute(url)
                print("\nPlaylist Information:")
                print(f"  Title: {playlist_info.title}")
                print(f"  URL: {playlist_info.url}")
                print(f"  Uploader: {playlist_info.uploader}")
                print(f"  Videos: {len(playlist_info.videos)}")
                print("\n  Video List (first 10):")
                for i, video in enumerate(playlist_info.videos[:10], 1):
                    print(f"    {i}. {video.title}")
                if len(playlist_info.videos) > 10:
                    print(f"    ... and {len(playlist_info.videos) - 10} more videos")
            
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
    
    def handle_settings(self):
        """Handle settings option."""
        self.print_header("SETTINGS & CONFIGURATION")
        
        print("\nCurrent Configuration:")
        print(f"  Audio Path: {self.cli_interface.config.get_audio_path()}")
        print(f"  Video Path: {self.cli_interface.config.get_video_path()}")
        print(f"  Audio Quality: {self.cli_interface.config.get_audio_quality()} kbps")
        print(f"  Video Quality: {self.cli_interface.config.get_video_quality()}")
        
        print("\nTo change settings, use the command line:")
        print("  python main.py config --show")
        print("  python main.py config --quality 320")
        print("  python main.py config --video-quality 1080p")
        print("  python main.py config --output-dir /path/to/downloads")
    
    async def run(self):
        """Main interactive loop."""
        while self.running:
            self.print_welcome()
            self.print_main_menu()
            
            choice = self.get_choice("Enter your choice (0-9): ", 
                                   ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            
            try:
                if choice == '0':
                    self.running = False
                    print("\nThank you for using NeruCord Archiver!")
                    break
                elif choice == '1':
                    await self.handle_download_video()
                elif choice == '2':
                    await self.handle_download_audio()
                elif choice == '3':
                    await self.handle_download_playlist()
                elif choice == '4':
                    await self.handle_browse_channel()
                elif choice == '5':
                    await self.handle_channel_download()
                elif choice == '6':
                    await self.handle_batch_download()
                elif choice == '7':
                    await self.handle_get_info()
                elif choice == '8':
                    self.handle_settings()
                elif choice == '9':
                    self.print_help()
                
                if choice != '0':
                    print()
                    self.wait_for_continue()
                    
            except KeyboardInterrupt:
                self.print_warning("Operation cancelled by user.")
                self.wait_for_continue()
            except Exception as e:
                self.print_error(f"Unexpected error: {str(e)}")
                self.wait_for_continue()


def main():
    """Main entry point for the interactive CLI."""
    interactive_cli = InteractiveCLI()
    asyncio.run(interactive_cli.run())


if __name__ == "__main__":
    main()
