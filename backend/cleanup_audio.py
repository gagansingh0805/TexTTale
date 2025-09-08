#!/usr/bin/env python3
"""
Manual Audio Cleanup Script for TextTale
Run this script to manually clean up all generated audio files
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from utils.cleanup import cleanup_all

def main():
    print("🧹 TextTale Audio Cleanup")
    print("=" * 30)
    
    # Confirm before cleaning
    response = input("Are you sure you want to delete ALL audio files? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Cleanup cancelled")
        return
    
    print("🗑️  Cleaning up all audio files...")
    cleanup_all()
    print("✅ Cleanup completed!")

if __name__ == "__main__":
    main()
