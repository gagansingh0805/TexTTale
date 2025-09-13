from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

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

# Create FastAPI app
app = FastAPI(
    title="TextTale API", 
    version="2.0.0",
    description="AI-powered story generation with clean service architecture"
)

# Enable CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel
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

@app.get("/api/story-options")
async def get_story_options():
    """Get available story generation options"""
    return {
        "styles": story_service.get_available_styles(),
        "lengths": story_service.get_available_lengths(),
        "voices": story_service.get_available_voices(),
        "background_noises": story_service.get_available_background_noises()
    }

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)
