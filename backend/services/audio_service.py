"""
Audio Service for Text-to-Speech functionality
Handles all audio generation and management
"""

import os
import time
import io
from typing import Optional
from gtts import gTTS
from utils.cleanup import track_audio_file


class AudioService:
    """Service for handling text-to-speech audio generation"""
    
    def __init__(self):
        self.voice_configs = {
            "woman": {"lang": "en", "tld": "com", "slow": False},  # American English for clear woman's voice
            "man": {"lang": "en", "tld": "com.au", "slow": False},  # Australian accent for deeper, more masculine voice
            "child": {"lang": "en", "tld": "co.uk", "slow": True}  # Slower speech for child-like voice
        }
        self.default_voice = "woman"
    
    def generate_speech(self, text: str, voice: str = None) -> Optional[str]:
        """
        Generate speech using Google Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            voice: Voice type (woman, man, child)
            
        Returns:
            Audio file path or None if failed
        """
        if not text or not text.strip():
            return None
            
        voice = voice or self.default_voice
        config = self.voice_configs.get(voice, self.voice_configs[self.default_voice])
        
        try:
            print(f"Generating TTS with voice: {voice}, config: {config}")
            
            # Create TTS object with voice configuration
            tts = gTTS(
                text=text, 
                lang=config["lang"], 
                tld=config["tld"],
                slow=config["slow"]
            )
            
            # Save to bytes
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Save audio file with voice identifier
            audio_filename = f"speech_{voice}_{int(time.time())}.mp3"
            audio_path = f"static/audio/{audio_filename}"
            
            with open(audio_path, "wb") as f:
                f.write(audio_buffer.getvalue())
            
            # Track the generated file for cleanup
            track_audio_file(audio_path)
            
            print(f"TTS file saved: {audio_filename}")
            return f"/static/audio/{audio_filename}"
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def generate_scene_audio(self, scene_text: str, voice: str, scene_index: int) -> Optional[str]:
        """
        Generate audio for a single scene
        
        Args:
            scene_text: Text content of the scene
            voice: Voice type to use
            scene_index: Index of the scene for logging
            
        Returns:
            Audio file path or None if failed
        """
        try:
            print(f"Generating audio for scene {scene_index + 1} with voice: {voice}")
            audio_url = self.generate_speech(scene_text, voice)
            if audio_url:
                print(f"SUCCESS: Audio generated for scene {scene_index + 1} with voice {voice}")
                return audio_url
            else:
                print(f"FAILED: Failed to generate audio for scene {scene_index + 1}")
                return None
        except Exception as e:
            print(f"Error generating audio for scene {scene_index + 1}: {e}")
            return None
    
    def get_available_voices(self) -> list:
        """Get list of available voice types"""
        return list(self.voice_configs.keys())
    
    def set_default_voice(self, voice: str) -> bool:
        """
        Set the default voice type
        
        Args:
            voice: Voice type to set as default
            
        Returns:
            True if successful, False if voice not found
        """
        if voice in self.voice_configs:
            self.default_voice = voice
            return True
        return False


# Global audio service instance
audio_service = AudioService()
