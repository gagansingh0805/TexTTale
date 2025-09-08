"""
Character Service for managing story characters
Handles character generation, development, and management
"""

import random
from typing import List, Dict, Optional
from services.models import Character


class CharacterService:
    """Service for managing story characters"""
    
    def __init__(self):
        self.character_names = [
            "Alex", "Morgan", "Jordan", "Casey", "Riley", "Taylor", "Avery", "Quinn",
            "Sage", "River", "Phoenix", "Blake", "Cameron", "Drew", "Emery", "Finley",
            "Hayden", "Jamie", "Kendall", "Logan", "Parker", "Reese", "Rowan", "Skyler",
            "Zara", "Kai", "Nova", "Luna", "Atlas", "Orion", "Vega", "Nyx", "Cosmo", "Stella",
            "Felix", "Hazel", "Ivy", "Jasper", "Kira", "Max", "Nora", "Oscar", "Penny", "Quincy",
            "Rosa", "Sam", "Tess", "Uri", "Vera", "Wade", "Xara", "Yara", "Zoe", "Aiden",
            "Bella", "Cora", "Dean", "Eva", "Finn", "Grace", "Hugo", "Ivy", "Jake", "Kate",
            "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rose", "Sam", "Tara", "Uma",
            "Victor", "Willa", "Xander", "Yara", "Zara", "Aaron", "Beth", "Caleb", "Diana",
            "Ethan", "Faith", "Gabe", "Hope", "Ian", "Jade", "Kyle", "Lily", "Mark", "Nina"
        ]
        
        self.character_traits = [
            "brave", "wise", "mysterious", "kind", "cunning", "loyal", "adventurous", "gentle",
            "fierce", "curious", "determined", "compassionate", "clever", "honest", "bold", "patient",
            "creative", "strong", "intelligent", "charismatic", "humble", "passionate", "calm", "energetic"
        ]
        
        self.character_roles = {
            "protagonist": "The main character who drives the story forward",
            "antagonist": "The character who opposes the protagonist",
            "mentor": "A wise character who guides the protagonist",
            "ally": "A loyal friend who supports the protagonist",
            "guardian": "A protective character who watches over others",
            "mystic": "A mysterious character with special knowledge",
            "companion": "A close friend who accompanies the protagonist"
        }
    
    def generate_characters(self, prompt: str, style: str, user_characters: List[str] = None) -> List[Character]:
        """
        Generate characters for the story
        
        Args:
            prompt: Story prompt to base characters on
            style: Story style/genre
            user_characters: User-provided character names
            
        Returns:
            List of Character objects
        """
        characters = []
        
        # Add user-provided characters
        if user_characters:
            for i, name in enumerate(user_characters[:3]):  # Limit to 3 user characters
                role = "protagonist" if i == 0 else "ally"
                character = self._create_character(name, role, prompt, style)
                characters.append(character)
        
        # Generate additional characters if needed
        num_additional = max(0, 3 - len(characters))
        for i in range(num_additional):
            name = self._generate_random_name(exclude=[c.name for c in characters])
            role = self._assign_role(len(characters))
            character = self._create_character(name, role, prompt, style)
            characters.append(character)
        
        return characters
    
    def _create_character(self, name: str, role: str, prompt: str, style: str) -> Character:
        """Create a character with description"""
        traits = random.sample(self.character_traits, 3)
        trait_text = ", ".join(traits)
        
        description = f"{name} is a {trait_text} character in this {style} story. {self.character_roles.get(role, 'A character in the story')}. They play a crucial role in {prompt.lower()}."
        
        return Character(
            name=name,
            description=description,
            role=role
        )
    
    def _generate_random_name(self, exclude: List[str] = None) -> str:
        """Generate a random character name"""
        exclude = exclude or []
        available_names = [name for name in self.character_names if name not in exclude]
        return random.choice(available_names)
    
    def _assign_role(self, character_count: int) -> str:
        """Assign a role based on character count"""
        if character_count == 0:
            return "protagonist"
        elif character_count == 1:
            return "ally"
        else:
            return random.choice(["mentor", "guardian", "mystic", "companion"])
    
    def generate_story_introduction(self, prompt: str, style: str, characters: List[Character]) -> str:
        """
        Generate a story introduction with character information
        
        Args:
            prompt: Story prompt
            style: Story style
            characters: List of characters
            
        Returns:
            Story introduction text
        """
        protagonist = next((c for c in characters if c.role == "protagonist"), characters[0])
        allies = [c for c in characters if c.role in ["ally", "companion"]]
        
        introduction = f"Welcome to '{prompt}', a captivating {style} tale. "
        introduction += f"Our story follows {protagonist.name}, {protagonist.description.split('.')[0].lower()}. "
        
        if allies:
            ally_names = [ally.name for ally in allies]
            if len(ally_names) == 1:
                introduction += f"Joining {protagonist.name} on this adventure is {ally_names[0]}. "
            else:
                introduction += f"Accompanying {protagonist.name} are {', '.join(ally_names[:-1])} and {ally_names[-1]}. "
        
        introduction += f"Together, they will embark on an extraordinary journey filled with wonder, mystery, and adventure. "
        introduction += f"Each character brings their unique strengths and perspectives to this {style} world, creating a rich tapestry of storytelling that will captivate and inspire."
        
        return introduction
    
    def get_available_roles(self) -> List[str]:
        """Get list of available character roles"""
        return list(self.character_roles.keys())
    
    def get_character_traits(self) -> List[str]:
        """Get list of available character traits"""
        return self.character_traits.copy()


# Global character service instance
character_service = CharacterService()
