"""
Audio file cleanup utility for TextTale application
Automatically removes generated audio files when the application exits
"""

import os
import glob
import signal
import sys
import atexit
from pathlib import Path

class AudioCleanup:
    def __init__(self, audio_dir: str = "static/audio"):
        self.audio_dir = Path(audio_dir)
        self.original_files = set()
        self.generated_files = set()
        
        # Register cleanup function
        atexit.register(self.cleanup_generated_files)
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Store original files at startup
        self.store_original_files()
    
    def store_original_files(self):
        """Store list of files that existed at startup"""
        if self.audio_dir.exists():
            self.original_files = set(self.audio_dir.glob("*.mp3"))
            print(f"Stored {len(self.original_files)} original audio files")
    
    def track_generated_file(self, file_path: str):
        """Track a newly generated audio file"""
        file_path = Path(file_path)
        if file_path.exists() and file_path not in self.original_files:
            self.generated_files.add(file_path)
            print(f"Tracking generated file: {file_path.name}")
    
    def cleanup_generated_files(self):
        """Remove all generated audio files"""
        cleaned_count = 0
        for file_path in self.generated_files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    cleaned_count += 1
                    print(f"Cleaned up: {file_path.name}")
            except Exception as e:
                print(f"Error cleaning {file_path.name}: {e}")
        
        # Also clean any remaining generated files by pattern
        if self.audio_dir.exists():
            pattern_files = list(self.audio_dir.glob("speech_*.mp3"))
            for file_path in pattern_files:
                if file_path not in self.original_files:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                            cleaned_count += 1
                            print(f"Pattern cleaned: {file_path.name}")
                    except Exception as e:
                        print(f"Error pattern cleaning {file_path.name}: {e}")
        
        print(f"Audio cleanup completed. Removed {cleaned_count} files.")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}. Cleaning up audio files...")
        self.cleanup_generated_files()
        sys.exit(0)
    
    def cleanup_all_audio(self):
        """Clean all audio files (use with caution)"""
        if self.audio_dir.exists():
            audio_files = list(self.audio_dir.glob("*.mp3"))
            for file_path in audio_files:
                try:
                    file_path.unlink()
                    print(f"Removed: {file_path.name}")
                except Exception as e:
                    print(f"Error removing {file_path.name}: {e}")
            print(f"Cleaned all {len(audio_files)} audio files")

# Global cleanup instance
cleanup_manager = None

def init_cleanup(audio_dir: str = "static/audio"):
    """Initialize the cleanup manager"""
    global cleanup_manager
    cleanup_manager = AudioCleanup(audio_dir)
    return cleanup_manager

def track_audio_file(file_path: str):
    """Track a generated audio file for cleanup"""
    if cleanup_manager:
        cleanup_manager.track_generated_file(file_path)

def cleanup_now():
    """Manually trigger cleanup"""
    if cleanup_manager:
        cleanup_manager.cleanup_generated_files()

def cleanup_all():
    """Clean all audio files"""
    if cleanup_manager:
        cleanup_manager.cleanup_all_audio()
