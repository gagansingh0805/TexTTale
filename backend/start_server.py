#!/usr/bin/env python3
"""
TextTale Backend Startup Script
Starts the FastAPI server with automatic audio cleanup
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    print("🎭 TextTale Backend Starting...")
    print("📁 Audio cleanup enabled - generated files will be removed on exit")
    print("🚀 Starting server on http://localhost:8001")
    print("💡 Press Ctrl+C to stop the server and clean up audio files")
    print("🏗️  Using clean service architecture")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        print("🧹 Audio cleanup will run automatically...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()