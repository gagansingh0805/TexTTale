"""
Models Service for data structures and validation
Contains Pydantic models and data validation logic
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class StoryRequest(BaseModel):
    """Request model for story generation"""
    text: str = Field(..., min_length=1, description="Story idea cannot be empty")
    style: str = Field(..., min_length=1, description="Style cannot be empty")
    length: str = Field(..., min_length=1, description="Length cannot be empty")
    characters: Optional[List[str]] = Field(default=[], description="Character names")
    background_noise: Optional[str] = Field(default="none", description="Background noise type")


class Character(BaseModel):
    """Model for story characters"""
    name: str
    description: str
    role: str  # protagonist, antagonist, supporting, etc.


class Scene(BaseModel):
    """Model for individual story scenes"""
    text: str
    audioUrl: Optional[str] = ""
    backgroundNoiseUrl: Optional[str] = ""


class StoryResponse(BaseModel):
    """Response model for story generation"""
    success: bool
    story: List[Scene]
    characters: List[Character]
    introduction: str
    message: str = ""


class AudioRequest(BaseModel):
    """Request model for audio generation"""
    text: str = Field(..., min_length=1, description="Text cannot be empty")
    voice: str = Field(default="woman", description="Voice type")


class AudioResponse(BaseModel):
    """Response model for audio generation"""
    success: bool
    audioUrl: Optional[str] = None
    message: str = ""


class CleanupResponse(BaseModel):
    """Response model for cleanup operations"""
    success: bool
    message: str


# Story length configurations
LENGTH_CONFIG = {
    "short": {"scenes": 6, "words_per_scene": 80},
    "medium": {"scenes": 12, "words_per_scene": 90},
    "long": {"scenes": 18, "words_per_scene": 100}
}
