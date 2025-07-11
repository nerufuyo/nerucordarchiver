"""
Base CLI components for consistent interface implementation.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, List, Callable
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class BaseInterface(ABC):
    """Base interface for CLI components."""
    
    def __init__(self):
        self.running = True
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title: str):
        """Print section header."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * len(title)}{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Print success message."""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message."""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Print warning message."""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message."""
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")
    
    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation."""
        while True:
            value = input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}").strip()
            if value or not required:
                return value if value else None
            self.print_error("Input cannot be empty. Please try again.")
    
    def get_choice(self, prompt: str, choices: List[str]) -> str:
        """Get user choice from list of options."""
        while True:
            choice = input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}").strip().lower()
            if choice in choices:
                return choice
            valid_choices = ", ".join(choices)
            self.print_error(f"Invalid choice. Valid options: {valid_choices}")
    
    def wait_for_continue(self):
        """Wait for user to press Enter."""
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


class ProgressDisplay:
    """Handles progress display for downloads."""
    
    @staticmethod
    def show_progress(current: int, total: int, title: str = ""):
        """Display progress bar."""
        if total == 0:
            return
        
        percentage = (current / total) * 100
        filled = int(percentage // 5)
        bar = "█" * filled + "░" * (20 - filled)
        
        # Truncate title if too long
        display_title = title[:40] + "..." if len(title) > 40 else title
        print(f"\r{Fore.GREEN}[{bar}] {percentage:.1f}% ({current}/{total}) {display_title}", end="")
    
    @staticmethod
    def show_single_progress(progress: float):
        """Display single download progress."""
        filled = int(progress // 5)
        bar = "█" * filled + "░" * (20 - filled)
        print(f"\r{Fore.YELLOW}[{bar}] {progress:.1f}%", end="")


class ValidationHelper:
    """Input validation utilities."""
    
    @staticmethod
    def parse_selection(selection: str, max_count: int) -> Optional[List[int]]:
        """Parse selection string into list of indices."""
        try:
            indices = []
            for part in selection.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start = int(start) - 1
                    end = int(end) - 1
                    if start < 0 or end >= max_count or start > end:
                        return None
                    indices.extend(range(start, end + 1))
                else:
                    index = int(part) - 1
                    if index < 0 or index >= max_count:
                        return None
                    indices.append(index)
            
            return sorted(list(set(indices)))
        except ValueError:
            return None
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to mm:ss format."""
        if seconds is None:
            return "Unknown"
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    @staticmethod
    def format_count(count: int) -> str:
        """Format count with thousand separators."""
        if count is None:
            return "Unknown"
        return f"{count:,}"
