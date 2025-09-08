"""
Background Noise Service for ambient sound generation
Handles background audio for immersive storytelling
"""

import os
import time
import random
from typing import Optional, Dict, List
from utils.cleanup import track_audio_file


class BackgroundNoiseService:
    """Service for generating background ambient sounds"""
    
    def __init__(self):
        self.noise_types = {
            "forest": {
                "description": "Peaceful forest sounds with birds and wind",
                "elements": ["birds chirping", "wind through trees", "rustling leaves", "distant water"]
            },
            "city": {
                "description": "Urban ambient sounds",
                "elements": ["traffic", "people talking", "city bustle", "distant sirens"]
            },
            "ocean": {
                "description": "Calming ocean waves",
                "elements": ["waves crashing", "seagulls", "ocean breeze", "distant ships"]
            },
            "rain": {
                "description": "Gentle rain sounds",
                "elements": ["rain drops", "thunder", "wind", "dripping water"]
            },
            "fireplace": {
                "description": "Cozy fireplace ambiance",
                "elements": ["crackling fire", "wood popping", "warm crackling", "gentle flames"]
            },
            "library": {
                "description": "Quiet library atmosphere",
                "elements": ["pages turning", "quiet footsteps", "soft whispers", "pencil writing"]
            },
            "none": {
                "description": "No background noise",
                "elements": []
            }
        }
    
    def generate_background_noise(self, noise_type: str, duration: int = 30) -> Optional[str]:
        """
        Generate background noise audio file
        
        Args:
            noise_type: Type of background noise
            duration: Duration in seconds
            
        Returns:
            Audio file path or None if failed
        """
        if noise_type == "none" or noise_type not in self.noise_types:
            return None
        
        try:
            noise_config = self.noise_types[noise_type]
            
            # Create a descriptive text for TTS that represents the ambient sound
            noise_text = f"Ambient {noise_config['description']} sounds playing softly in the background for {duration} seconds"
            
            # Generate audio using gTTS
            from gtts import gTTS
            import io
            
            tts = gTTS(text=noise_text, lang="en", tld="com", slow=False)
            
            # Save to bytes
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Save audio file
            audio_filename = f"background_{noise_type}_{int(time.time())}.mp3"
            audio_path = f"static/audio/{audio_filename}"
            
            with open(audio_path, "wb") as f:
                f.write(audio_buffer.getvalue())
            
            # Track the generated file for cleanup
            track_audio_file(audio_path)
            
            print(f"Background noise generated: {audio_filename}")
            return f"/static/audio/{audio_filename}"
            
        except Exception as e:
            print(f"Background noise generation error: {e}")
            return None
    
    def get_available_noise_types(self) -> List[str]:
        """Get list of available background noise types"""
        return list(self.noise_types.keys())
    
    def get_noise_description(self, noise_type: str) -> str:
        """Get description for a specific noise type"""
        return self.noise_types.get(noise_type, {}).get("description", "Unknown noise type")
    
    def get_noise_elements(self, noise_type: str) -> List[str]:
        """Get sound elements for a specific noise type"""
        return self.noise_types.get(noise_type, {}).get("elements", [])


# Global background noise service instance
background_noise_service = BackgroundNoiseService()
