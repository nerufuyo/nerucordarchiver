# NeruCord Archiver

A powerful, clean architecture YouTube video and audio downloader with playlist support. Built with Python using clean code principles and comprehensive testing.

> **✅ Status Update (July 2025)**: Downloads are working again! Updated to yt-dlp 2025.6.30 with enhanced anti-bot protection and Android client support.

## Features

- **Download YouTube Videos**: High-quality video downloads up to 2160p (4K)
- **Convert to Audio**: Extract and convert videos to MP3 format with customizable quality
- **Playlist Support**: Download entire playlists with progress tracking
- **Batch Downloads**: Process multiple URLs from text files
- **Quality Control**: Configurable video quality (240p-2160p) and audio bitrates (128-320 kbps)
- **Format Options**: Support for MP3, FLAC, WAV, AAC audio formats
- **Resume Capability**: Track download history and resume failed downloads
- **Configuration Management**: Persistent user preferences and settings
- **Single or Batch Downloads**: Handle individual videos or complete playlists
- **Clean CLI Interface**: Easy-to-use command-line interface with colored output
- **Progress Tracking**: Real-time download progress for both single files and playlists
- **Error Handling**: Robust error handling with informative messages
- **File Management**: Automatic directory creation and filename sanitization
- **Anti-Bot Protection**: Browser-like headers to bypass YouTube's restrictions

## Architecture

This project follows Clean Architecture principles:

```
src/
├── config/          # Configuration and constants
├── domain/          # Business entities and value objects
├── repositories/    # Repository interfaces (ports)
├── use_cases/       # Application business logic
├── infrastructure/  # External adapters (yt-dlp, file system)
└── cli/            # Command-line interface
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nerucordarchiver.git
cd nerucordarchiver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Download Single Video

```bash
# Download video
python main.py video "https://youtube.com/watch?v=VIDEO_ID"

# Download video to specific directory
python main.py video "https://youtube.com/watch?v=VIDEO_ID" --output /path/to/downloads
```

### Download Audio (MP3)

```bash
# Convert and download as MP3
python main.py audio "https://youtube.com/watch?v=VIDEO_ID"

# Download audio to specific directory
python main.py audio "https://youtube.com/watch?v=VIDEO_ID" --output /path/to/downloads
```

### Download Playlist

```bash
# Download playlist as audio (default)
python main.py playlist "https://youtube.com/playlist?list=PLAYLIST_ID"

# Download playlist as video
python main.py playlist "https://youtube.com/playlist?list=PLAYLIST_ID" --type video

# Download playlist to specific directory
python main.py playlist "https://youtube.com/playlist?list=PLAYLIST_ID" --output /path/to/downloads
```

### Batch Download

```bash
# Download multiple videos from a file (one URL per line)
python main.py batch urls.txt

# Download as video format
python main.py batch urls.txt --type video

# Use custom output directory
python main.py batch urls.txt --output /path/to/downloads
```

### Configuration Management

```bash
# Show current configuration
python main.py config --show

# Set audio quality (128, 192, 256, 320 kbps)
python main.py config --quality 320

# Set audio format
python main.py config --format flac

# Set video quality (240p, 360p, 480p, 720p, 1080p, 1440p, 2160p)
python main.py config --video-quality 1080p

# Set default output directory
python main.py config --output-dir /path/to/downloads
```

### Get Information

```bash
# Get video or playlist information
python main.py info "https://youtube.com/watch?v=VIDEO_ID"
python main.py info "https://youtube.com/playlist?list=PLAYLIST_ID"
```

## Command Reference

### Commands

- `video` - Download YouTube video
- `audio` - Download and convert YouTube video to MP3
- `playlist` - Download entire YouTube playlist
- `batch` - Download multiple videos from a file containing URLs
- `config` - Manage application configuration and preferences
- `info` - Get information about video or playlist

### Options

- `--output, -o` - Specify output directory
- `--type, -t` - For playlists and batch: choose 'video' or 'audio' (default: audio)
- `--quality, -q` - Set audio quality (config command)
- `--format, -f` - Set audio format (config command)
- `--video-quality` - Set video quality (config command)
- `--show` - Show current configuration (config command)
- `--help` - Show help message
- `--version` - Show version information

## Configuration

Default settings can be found in `src/config/constants.py`:

- **Audio Quality**: 192 kbps MP3
- **Video Quality**: 720p WebM/MP4  
- **Download Paths**: `~/Downloads/NeruCord/video` and `~/Downloads/NeruCord/audio` (cross-platform)
- **Supported Formats**: MP3, MP4, WebM, MKV, AVI, WAV, FLAC, AAC

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Code Structure

The project follows these principles:

1. **Clean Architecture**: Separation of concerns with clear boundaries
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Single Responsibility**: Each class has one reason to change
4. **Open/Closed Principle**: Open for extension, closed for modification

### Adding New Features

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Implement changes following the existing architecture
3. Add comprehensive tests
4. Update documentation
5. Commit with descriptive messages
6. Create pull request to `dev` branch

## Error Handling

The application provides clear error messages for common issues:

- **Invalid URLs**: Validates YouTube URL format
- **Network Issues**: Handles connection timeouts and errors
- **File System**: Manages directory creation and permissions
- **Download Failures**: Provides specific error information
- **Format Compatibility**: Automatic fallback to compatible formats
- **YouTube Restrictions**: Uses browser-like headers to bypass anti-bot measures

### Troubleshooting

**403 Forbidden Errors:**
- ✅ **RESOLVED**: Updated to yt-dlp 2025.6.30 with enhanced anti-bot protection
- The application now includes Android client support and sleep intervals
- If you still encounter 403 errors:
  - Update yt-dlp: `pip install --upgrade yt-dlp`
  - Wait 15-30 minutes before retrying (rate limiting)
  - Try different videos (some may work while others don't)
  - Use VPN or different network if available
  - Check [yt-dlp GitHub issues](https://github.com/yt-dlp/yt-dlp/issues) for updates

**Format Not Available:**
- The application automatically tries multiple format combinations
- Falls back from quality-specific to general formats if needed
- Always attempts to merge video and audio streams for best quality

**Slow Downloads:**
- Use lower quality settings for faster downloads
- Check your internet connection
- Some videos may have rate limiting applied by YouTube

**Note**: The application now works reliably with yt-dlp 2025.6.30 and enhanced anti-bot protection. Downloads are working normally!

## Dependencies

- **yt-dlp**: YouTube video downloading and metadata extraction
- **click**: Command-line interface framework
- **colorama**: Cross-platform colored terminal output
- **pytest**: Testing framework with coverage support

## Contributing

1. Fork the repository
2. Create a feature branch from `dev`
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0
- Initial release with core functionality
- Clean architecture implementation
- Comprehensive test suite
- CLI interface with progress tracking
- Support for videos, audio, and playlists

### v1.0.1
- **FIXED**: Video format selection compatibility with YouTube's current format structure
- **FIXED**: HTTP 403 Forbidden errors with browser-like headers and anti-bot protection
- **IMPROVED**: Robust three-tier format fallback system
- **ENHANCED**: Support for up to 2160p (4K) video downloads
- **ADDED**: Automatic video/audio stream merging for optimal quality
- **IMPROVED**: Cross-platform Downloads folder detection (Windows/Linux/Mac)
- **CHANGED**: Default download location to `~/Downloads/NeruCord/` for better organization

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) for robust YouTube downloading
- Inspired by clean architecture principles
- Thanks to the Python community for excellent tooling