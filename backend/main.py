"""
TextTale Backend API
Clean, service-based architecture for AI story generation
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Import services
from services import (
    story_service,
    audio_service,
    StoryRequest,
    StoryResponse,
    AudioRequest,
    AudioResponse,
    CleanupResponse
)
from utils.cleanup import init_cleanup, cleanup_now

# Load environment variables
load_dotenv()

# Initialize cleanup manager
cleanup_manager = init_cleanup("static/audio")

# Create FastAPI app
app = FastAPI(
    title="TextTale API", 
    version="2.0.0",
    description="AI-powered story generation with clean service architecture"
)

# Create static directory for audio
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "TextTale API is running!", 
        "version": "2.0.0",
        "features": [
            "Structured narrative generation",
            "Text-to-speech with woman's voice",
            "Multiple story lengths (short, medium, long)",
            "Clean service architecture"
        ]
    }


@app.post("/api/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """Generate a structured story with audio"""
    try:
        # Validate request
        validation = story_service.validate_story_request(
            request.text, 
            request.style, 
            request.length
        )
        
        if not validation["valid"]:
            raise HTTPException(
                status_code=400, 
                detail="; ".join(validation["errors"])
            )
        
        # Generate story using service
        result = story_service.generate_story(
            prompt=request.text,
            style=request.style,
            length=request.length,
            characters=request.characters,
            background_noise=request.background_noise,
            include_audio=True
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])
        
        return StoryResponse(
            success=True,
            story=result["story"],
            characters=result["characters"],
            introduction=result["introduction"],
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in generate_story: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/text-to-speech", response_model=AudioResponse)
async def text_to_speech(request: AudioRequest):
    """Generate audio from text using TTS"""
    try:
        audio_url = audio_service.generate_speech(request.text, request.voice)
        
        if audio_url:
            return AudioResponse(
                success=True,
                audioUrl=audio_url,
                message="Audio generated successfully"
            )
        else:
            return AudioResponse(
                success=False,
                audioUrl=None,
                message="Failed to generate audio"
            )
            
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return AudioResponse(
            success=False,
            audioUrl=None,
            message=f"Error generating audio: {str(e)}"
        )


@app.post("/api/cleanup-audio", response_model=CleanupResponse)
async def cleanup_audio():
    """Manually trigger audio cleanup"""
    try:
        cleanup_now()
        return CleanupResponse(
            success=True,
            message="Audio cleanup completed"
        )
    except Exception as e:
        return CleanupResponse(
            success=False,
            message=f"Cleanup failed: {str(e)}"
        )


@app.get("/api/story-options")
async def get_story_options():
    """Get available story generation options"""
    return {
        "styles": story_service.get_available_styles(),
        "lengths": story_service.get_available_lengths(),
        "voices": story_service.get_available_voices(),
        "background_noises": story_service.get_available_background_noises()
    }


if __name__ == "__main__":
    import uvicorn
    print("TextTale Backend Starting...")
    print("Audio cleanup enabled - generated files will be removed on exit")
    print("Starting server on http://localhost:8001")
    print("Press Ctrl+C to stop the server and clean up audio files")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )