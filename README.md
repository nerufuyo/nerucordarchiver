# NeruCord Archiver

A powerful, clean architecture YouTube video and audio downloader with playlist support. Built with Python using clean code principles and comprehensive testing.

## Features

- **Download YouTube Videos**: High-quality video downloads up to 720p
- **Convert to Audio**: Extract and convert videos to MP3 format with customizable quality
- **Playlist Support**: Download entire playlists with progress tracking
- **Single or Batch Downloads**: Handle individual videos or complete playlists
- **Clean CLI Interface**: Easy-to-use command-line interface with colored output
- **Progress Tracking**: Real-time download progress for both single files and playlists
- **Error Handling**: Robust error handling with informative messages
- **File Management**: Automatic directory creation and filename sanitization

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
- `info` - Get information about video or playlist

### Options

- `--output, -o` - Specify output directory
- `--type, -t` - For playlists: choose 'video' or 'audio' (default: audio)
- `--help` - Show help message
- `--version` - Show version information

## Configuration

Default settings can be found in `src/config/constants.py`:

- **Audio Quality**: 192 kbps MP3
- **Video Quality**: 720p MP4
- **Download Paths**: `./downloads/video` and `./downloads/audio`
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

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) for robust YouTube downloading
- Inspired by clean architecture principles
- Thanks to the Python community for excellent tooling