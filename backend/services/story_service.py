"""
Story Service for managing different story types and lengths
Handles story generation coordination and scene management
"""

import concurrent.futures
from typing import List, Dict, Optional
from services.audio_service import audio_service
from services.narrative_service import narrative_service
from services.character_service import character_service
from services.background_noise_service import background_noise_service
from services.models import Character


class StoryService:
    """Service for managing story generation and coordination"""
    
    def __init__(self):
        self.audio_service = audio_service
        self.narrative_service = narrative_service
        self.character_service = character_service
        self.background_noise_service = background_noise_service
    
    def generate_story(self, prompt: str, style: str, length: str, characters: List[str] = None, background_noise: str = "none", include_audio: bool = True) -> Dict:
        """
        Generate a complete story with scenes, characters, and optional audio
        
        Args:
            prompt: User's story idea
            style: Story style/genre
            length: Story length (short, medium, long)
            characters: List of character names
            background_noise: Type of background noise
            include_audio: Whether to generate audio for scenes
            
        Returns:
            Dictionary with success status, story scenes, characters, introduction, and message
        """
        try:
            print(f"Generating {length} {style} story: {prompt}")
            
            # Generate characters
            story_characters = self.character_service.generate_characters(prompt, style, characters)
            
            # Generate story introduction
            introduction = self.character_service.generate_story_introduction(prompt, style, story_characters)
            
            # Generate structured narrative
            scenes_data = self.narrative_service.generate_structured_narrative(prompt, style, length)
            
            if include_audio:
                # Generate audio and background noise for all scenes
                scenes = self._generate_scenes_with_audio_and_noise(scenes_data, background_noise)
            else:
                # Generate scenes without audio
                scenes = self._generate_scenes_without_audio(scenes_data)
            
            return {
                "success": True,
                "story": scenes,
                "characters": story_characters,
                "introduction": introduction,
                "message": f"Successfully generated {len(scenes)} scenes with {len(story_characters)} characters"
            }
            
        except Exception as e:
            print(f"Error generating story: {e}")
            return {
                "success": False,
                "story": [],
                "characters": [],
                "introduction": "",
                "message": f"Failed to generate story: {str(e)}"
            }
    
    def _generate_scenes_with_audio(self, scenes_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Generate scenes with audio using parallel processing"""
        scenes = []
        
        # Use ThreadPoolExecutor for parallel audio processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all audio generation tasks
            audio_futures = []
            
            for i, scene_data in enumerate(scenes_data):
                print(f"Processing scene {i+1}/{len(scenes_data)}...")
                
                # Submit audio generation task
                audio_future = executor.submit(
                    self.audio_service.generate_scene_audio, 
                    scene_data["text"], 
                    "woman",  # Default to woman's voice
                    i
                )
                audio_futures.append((i, audio_future))
            
            # Process audio results
            audio_results = {}
            for i, future in audio_futures:
                try:
                    audio_url = future.result(timeout=30)
                    audio_results[i] = audio_url
                    print(f"Audio {i+1} generated successfully")
                except Exception as e:
                    print(f"Failed to generate audio {i+1}: {e}")
                    audio_results[i] = None
            
            # Create scenes with audio results
            for i, scene_data in enumerate(scenes_data):
                scene = {
                    "text": scene_data["text"],
                    "audioUrl": audio_results.get(i) or ""
                }
                scenes.append(scene)
        
        return scenes
    
    def _generate_scenes_with_audio_and_noise(self, scenes_data: List[Dict[str, str]], background_noise: str) -> List[Dict[str, str]]:
        """Generate scenes with audio and background noise using parallel processing"""
        scenes = []
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            audio_futures = []
            noise_futures = []
            
            for i, scene_data in enumerate(scenes_data):
                print(f"Processing scene {i+1}/{len(scenes_data)}...")
                
                # Submit audio generation task
                audio_future = executor.submit(
                    self.audio_service.generate_scene_audio, 
                    scene_data["text"], 
                    "woman",  # Default to woman's voice
                    i
                )
                audio_futures.append((i, audio_future))
                
                # Submit background noise generation task
                noise_future = executor.submit(
                    self.background_noise_service.generate_background_noise,
                    background_noise,
                    30  # 30 seconds duration
                )
                noise_futures.append((i, noise_future))
            
            # Process audio results
            audio_results = {}
            for i, future in audio_futures:
                try:
                    audio_url = future.result(timeout=30)
                    audio_results[i] = audio_url
                    print(f"Audio {i+1} generated successfully")
                except Exception as e:
                    print(f"Failed to generate audio {i+1}: {e}")
                    audio_results[i] = None
            
            # Process background noise results
            noise_results = {}
            for i, future in noise_futures:
                try:
                    noise_url = future.result(timeout=30)
                    noise_results[i] = noise_url
                    print(f"Background noise {i+1} generated successfully")
                except Exception as e:
                    print(f"Failed to generate background noise {i+1}: {e}")
                    noise_results[i] = None
            
            # Create scenes with results
            for i, scene_data in enumerate(scenes_data):
                scene = {
                    "text": scene_data["text"],
                    "audioUrl": audio_results.get(i) or "",
                    "backgroundNoiseUrl": noise_results.get(i) or ""
                }
                scenes.append(scene)
        
        return scenes
    
    def _generate_scenes_without_audio(self, scenes_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Generate scenes without audio"""
        scenes = []
        for scene_data in scenes_data:
            scene = {
                "text": scene_data["text"],
                "audioUrl": ""
            }
            scenes.append(scene)
        return scenes
    
    def generate_full_story_audio(self, story_text: str, voice: str = "woman") -> Optional[str]:
        """
        Generate audio for the entire story
        
        Args:
            story_text: Complete story text
            voice: Voice type to use
            
        Returns:
            Audio file path or None if failed
        """
        return self.audio_service.generate_speech(story_text, voice)
    
    def get_available_styles(self) -> List[str]:
        """Get list of available story styles"""
        return ["fantasy", "sci-fi", "mystery", "romance", "adventure", "horror", "comedy", "drama"]
    
    def get_available_lengths(self) -> List[str]:
        """Get list of available story lengths"""
        return self.narrative_service.get_available_lengths()
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices"""
        return self.audio_service.get_available_voices()
    
    def get_available_background_noises(self) -> List[str]:
        """Get list of available background noise types"""
        return self.background_noise_service.get_available_noise_types()
    
    def validate_story_request(self, prompt: str, style: str, length: str) -> Dict[str, str]:
        """
        Validate story generation request
        
        Args:
            prompt: User's story idea
            style: Story style/genre
            length: Story length
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        if not prompt or not prompt.strip():
            errors.append("Story idea cannot be empty")
        
        if not style or not style.strip():
            errors.append("Style cannot be empty")
        
        if not length or not length.strip():
            errors.append("Length cannot be empty")
        
        if length not in self.get_available_lengths():
            errors.append("Invalid length option")
        
        if style not in self.get_available_styles():
            errors.append("Invalid style option")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


# Global story service instance
story_service = StoryService()
