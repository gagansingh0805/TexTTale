"""
Narrative Service for structured text-only story generation
Handles different story lengths and narrative structures
"""

from typing import List, Dict
from services.audio_service import audio_service


class NarrativeService:
    """Service for generating structured text-only narratives"""
    
    def __init__(self):
        self.length_configs = {
            "short": {"scenes": 10, "words_per_scene": 200},
            "medium": {"scenes": 20, "words_per_scene": 250},
            "long": {"scenes": 30, "words_per_scene": 300}
        }
    
    def generate_structured_narrative(self, prompt: str, style: str, length: str) -> List[Dict[str, str]]:
        """
        Generate a structured narrative with introduction, setting, conflict, etc.
        
        Args:
            prompt: User's story idea
            style: Story style/genre
            length: Story length (short, medium, long)
            
        Returns:
            List of scene dictionaries with text and image descriptions
        """
        config = self.length_configs.get(length, self.length_configs["medium"])
        num_scenes = config["scenes"]
        
        # Define narrative structure based on length
        structure = self._get_narrative_structure(length)
        
        # Create structured scenes
        scenes = []
        for i in range(num_scenes):
            if i < len(structure):
                structure_type = structure[i]
            else:
                # For longer stories, use generic continuation
                structure_type = "continuation"
            scene_text = self._generate_scene_text(prompt, style, structure_type, i)
            
            scenes.append({
                "text": scene_text,
                "imageDescription": f"A {style} scene featuring {prompt} in a narrative context"
            })
        
        return scenes
    
    def _get_narrative_structure(self, length: str) -> List[str]:
        """Get narrative structure based on story length"""
        if length == "short":
            return [
                "introduction", "setting", "conflict", "rising_action", 
                "climax", "resolution", "conclusion"
            ]
        elif length == "medium":
            return [
                "introduction", "character_development", "setting", "conflict_introduction", 
                "rising_action_1", "rising_action_2", "complications", "climax", 
                "falling_action", "resolution", "conclusion"
            ]
        else:  # long
            return [
                "introduction", "character_background", "setting_establishment", "inciting_incident", 
                "rising_action_1", "character_development", "rising_action_2", "complications_1", 
                "midpoint", "complications_2", "rising_action_3", "climax", "falling_action_1", 
                "falling_action_2", "resolution", "denouement", "conclusion"
            ]
    
    def _generate_scene_text(self, prompt: str, style: str, structure_type: str, scene_index: int) -> str:
        """Generate text for a specific scene based on structure type"""
        scene_templates = {
            "introduction": f"In the heart of a {style} realm, {prompt} awakens to discover their world has changed forever. The morning light reveals extraordinary possibilities that were hidden in the shadows of yesterday. As they step forward into this new reality, every sense comes alive with wonder and anticipation.",
            "setting": f"The {style} landscape stretches endlessly before {prompt}, a tapestry of breathtaking beauty and hidden mysteries. Ancient structures whisper secrets of forgotten times, while the very air hums with magical energy. Every corner holds the promise of adventure and discovery.",
            "conflict": f"A formidable challenge emerges before {prompt}, testing their resolve and courage in ways they never imagined. The stakes rise higher with each passing moment, forcing them to dig deep within themselves to find the strength to continue. Allies and enemies alike watch with bated breath.",
            "rising_action": f"The tension mounts as {prompt} encounters increasingly complex obstacles and unexpected allies. Each step forward reveals new layers of the {style} world's intricate design. The journey becomes more perilous yet more rewarding, pushing them toward their ultimate destiny.",
            "climax": f"The moment of truth arrives for {prompt}, where all their experiences, lessons, and growth culminate in a single defining moment. In this {style} tale, everything they've learned and endured leads to this pivotal confrontation that will determine their fate and the fate of their world.",
            "resolution": f"{prompt} discovers a path forward through the chaos, finding clarity and purpose in the midst of uncertainty. The conflicts that once seemed insurmountable begin to resolve, revealing new possibilities and hope for the future. Wisdom emerges from the trials endured.",
            "conclusion": f"{prompt}'s {style} adventure reaches its natural conclusion, but the echoes of their journey will resonate through time. The story's impact extends far beyond its final pages, inspiring others to embark on their own quests for truth, courage, and transformation.",
            "character_development": f"Through their {style} experiences, {prompt} undergoes profound transformation, discovering hidden strengths and confronting inner demons. Each challenge shapes their character, revealing depths of courage and compassion they never knew they possessed.",
            "complications": f"Unexpected twists and turns complicate {prompt}'s journey, adding layers of intrigue and suspense to their {style} story. New revelations challenge everything they thought they knew, forcing them to adapt and grow in ways they never anticipated.",
            "falling_action": f"The intensity begins to ease as {prompt} moves toward resolution in their {style} adventure. The storm of conflict gives way to moments of reflection and understanding, allowing them to process the profound changes they've undergone.",
            "character_background": f"The layers of {prompt}'s past unfold, revealing the experiences and choices that shaped them into who they are today. In this {style} world, their history becomes a key to understanding their present and future path.",
            "setting_establishment": f"The {style} environment becomes more defined and immersive, showing {prompt} the intricate details of the world they must navigate. Every element tells a story, from the ancient architecture to the mystical creatures that call this place home.",
            "inciting_incident": f"A pivotal event occurs that irrevocably changes {prompt}'s world, setting them on a {style} journey that will test their limits and transform their understanding of reality. Nothing will ever be the same again.",
            "midpoint": f"{prompt} reaches a crucial turning point in their {style} adventure, where everything they've learned and experienced converges. This moment of revelation changes the entire trajectory of their journey, opening new possibilities and challenges.",
            "denouement": f"The final threads of {prompt}'s {style} story are woven together with masterful precision, bringing closure to their journey while leaving room for new beginnings. Every loose end finds its place in the grand tapestry of their adventure."
        }
        
        scene_templates["continuation"] = f"{prompt} continues their {style} journey, facing new challenges and discovering hidden truths about themselves and their world. Each step forward reveals new mysteries and opportunities for growth and adventure."
        
        return scene_templates.get(structure_type, f"{prompt} continues their {style} journey, facing new challenges and discovering hidden truths about themselves and their world. Each step forward reveals new mysteries and opportunities for growth and adventure.")
    
    def get_available_lengths(self) -> List[str]:
        """Get list of available story lengths"""
        return list(self.length_configs.keys())
    
    def get_length_config(self, length: str) -> Dict[str, int]:
        """Get configuration for a specific story length"""
        return self.length_configs.get(length, self.length_configs["medium"])


# Global narrative service instance
narrative_service = NarrativeService()
