#!/usr/bin/env python3
"""
Setup script for NeruCord Archiver
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def install_dependencies():
    """Install required dependencies."""
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True


def run_tests():
    """Run the test suite."""
    return run_command("python -m pytest tests/ -v", "Running test suite")


def create_directories():
    """Create necessary directories."""
    directories = ["downloads", "downloads/audio", "downloads/video"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created download directories")


def main():
    """Main setup function."""
    print("🚀 NeruCord Archiver Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but installation completed")
    
    print("\n🎉 Setup completed successfully!")
    print("\nUsage examples:")
    print("  python main.py video 'https://youtube.com/watch?v=VIDEO_ID'")
    print("  python main.py audio 'https://youtube.com/watch?v=VIDEO_ID'")
    print("  python main.py playlist 'https://youtube.com/playlist?list=PLAYLIST_ID'")
    print("  python main.py batch example_urls.txt")
    print("  python main.py config --show")
    print("\nFor more information, run: python main.py --help")


if __name__ == "__main__":
    main()
