"""
Personalized Content Engine - Comprehensive Solution for Element Descriptions
Generates deeply personalized content for ALL cosmic elements using AI and fallback templates
"""

import os
import json
import anthropic
from typing import Dict, Any, Optional
from cosmic_elements_database import *

class PersonalizedContentEngine:
    """Advanced engine for generating personalized cosmic element content"""
    
    def __init__(self):
        # Initialize Anthropic client
        self.anthropic_client = None
        try:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            print(f"Anthropic client initialization failed: {e}")
            
        # Element type mapping using unified system
        from unified_maya_system import unified_maya_calculator
        
        # Map element types to unified calculator data
        self.element_databases = {
            "daySign": {sign["name"]: {"name": sign["name"], "meaning": sign["meaning"], "detailed_description": f"Sacred {sign['name']} energy of {sign['meaning']}"} for sign in unified_maya_calculator.DAY_SIGNS},
            "galacticTone": {tone["name"]: {"name": tone["name"], "meaning": tone["meaning"], "detailed_description": f"Sacred {tone['name']} energy of {tone['meaning']}"} for tone in unified_maya_calculator.GALACTIC_TONES},
            "spiritAnimal": {animal: {"name": animal, "meaning": f"{animal} Spirit", "detailed_description": f"Sacred {animal} spirit guide"} for animal in unified_maya_calculator.SPIRIT_ANIMALS},
            "crystalAlly": {crystal: {"name": crystal, "meaning": f"{crystal} Crystal", "detailed_description": f"Sacred {crystal} crystal ally"} for crystal in unified_maya_calculator.CRYSTAL_ALLIES},
            "plantMedicine": {plant: {"name": plant, "meaning": f"{plant} Medicine", "detailed_description": f"Sacred {plant} plant medicine"} for plant in unified_maya_calculator.PLANT_MEDICINES},
            "chakraResonance": {chakra: {"name": chakra, "meaning": f"{chakra} Chakra", "detailed_description": f"Sacred {chakra} chakra energy"} for chakra in unified_maya_calculator.CHAKRAS},
            "humanDesignType": {hd_type: {"name": hd_type, "meaning": f"{hd_type} Type", "detailed_description": f"Sacred {hd_type} human design type"} for hd_type in unified_maya_calculator.HUMAN_DESIGN_TYPES},
            "treeOfLifePrimary": {pos: {"name": pos, "meaning": f"{pos} Position", "detailed_description": f"Sacred {pos} tree of life position"} for pos in unified_maya_calculator.TREE_OF_LIFE},
            "treeOfLifeSecondary": {pos: {"name": pos, "meaning": f"{pos} Position", "detailed_description": f"Sacred {pos} tree of life position"} for pos in unified_maya_calculator.TREE_OF_LIFE}
        }
        
        # Add element mappings
        elements = ["Fire", "Water", "Earth", "Air"]
        directions = ["East", "North", "West", "South"]
        colors = ["Red", "White", "Blue", "Yellow"]
        
        self.element_databases.update({
            "element": {elem: {"name": elem, "meaning": f"{elem} Element", "detailed_description": f"Sacred {elem} elemental energy"} for elem in elements},
            "direction": {direction: {"name": direction, "meaning": f"{direction} Direction", "detailed_description": f"Sacred {direction} directional energy"} for direction in directions},
            "colorFamily": {color: {"name": color, "meaning": f"{color} Color", "detailed_description": f"Sacred {color} color energy"} for color in colors},
            "tribe": {sign["name"]: {"name": sign["name"], "meaning": sign["meaning"], "detailed_description": f"Sacred {sign['name']} tribe energy"} for sign in unified_maya_calculator.DAY_SIGNS},
            "guideSign": {sign["name"]: {"name": sign["name"], "meaning": sign["meaning"], "detailed_description": f"Sacred {sign['name']} guide energy"} for sign in unified_maya_calculator.DAY_SIGNS},
            "antipodeSign": {sign["name"]: {"name": sign["name"], "meaning": sign["meaning"], "detailed_description": f"Sacred {sign['name']} antipode energy"} for sign in unified_maya_calculator.DAY_SIGNS},
            "occultSign": {sign["name"]: {"name": sign["name"], "meaning": sign["meaning"], "detailed_description": f"Sacred {sign['name']} occult energy"} for sign in unified_maya_calculator.DAY_SIGNS}
        })
        
        # Element display names
        self.element_display_names = {
            "daySign": "Maya Day Sign",
            "galacticTone": "Galactic Tone",
            "spiritAnimal": "Spirit Animal",
            "crystalAlly": "Crystal Ally", 
            "plantMedicine": "Plant Medicine",
            "chakraResonance": "Chakra Resonance",
            "humanDesignType": "Human Design Type",
            "treeOfLifePrimary": "Tree of Life Primary",
            "treeOfLifeSecondary": "Tree of Life Secondary",
            "element": "Maya Element",
            "direction": "Sacred Direction",
            "colorFamily": "Color Family",
            "tribe": "Maya Tribe",
            "guideSign": "Guide Sign",
            "antipodeSign": "Antipode Sign",
            "occultSign": "Occult Sign",
            "trecena": "Trecena Cycle",
            "wavespell": "Wavespell Energy",
            "castle": "Maya Castle",
            "harmonic": "Harmonic Frequency",
            "lordOfNight": "Lord of the Night",
            "haabDate": "Haab Date",
            "longCount": "Long Count",
            "yearBearer": "Year Bearer",
            "moonPhase": "Moon Phase",
            "galacticActivationPortal": "Galactic Activation Portal",
            "kinNumber": "Kin Number"
        }
        
    def generate_personalized_explanation(self, element_type: str, element_value: str, user_data: Dict[str, Any]) -> str:
        """Generate comprehensive personalized explanation for any cosmic element"""
        
        # Get user information
        user_name = user_data.get("first_name", "Soul Seeker")
        day_sign_data = user_data.get("day_sign", {})
        if isinstance(day_sign_data, str):
            try:
                day_sign_data = json.loads(day_sign_data)
            except:
                day_sign_data = {"name": "Unknown"}
        
        day_sign_name = day_sign_data.get("name", "Unknown")
        element_display_name = self.element_display_names.get(element_type, element_type)
        
        # Try AI-powered personalization first
        if self.anthropic_client:
            try:
                ai_explanation = self._generate_ai_explanation(element_type, element_value, user_data)
                if ai_explanation and len(ai_explanation) > 500:
                    return ai_explanation
            except Exception as e:
                print(f"AI explanation failed: {e}")
        
        # Use comprehensive fallback with personalized templates
        return self._generate_fallback_explanation(element_type, element_value, user_data)
    
    def _generate_ai_explanation(self, element_type: str, element_value: str, user_data: Dict[str, Any]) -> str:
        """Generate AI-powered personalized explanation"""
        
        user_name = user_data.get("first_name", "Soul Seeker")
        day_sign_data = user_data.get("day_sign", {})
        if isinstance(day_sign_data, str):
            try:
                day_sign_data = json.loads(day_sign_data)
            except:
                day_sign_data = {"name": "Unknown"}
        
        day_sign_name = day_sign_data.get("name", "Unknown")
        element_display_name = self.element_display_names.get(element_type, element_type)
        
        # Get comprehensive context from user data
        context_elements = []
        for key, value in user_data.items():
            if value and value != "Unknown":
                context_elements.append(f"{key}: {value}")
        
        user_context = "\n".join(context_elements[:10])  # Limit context for API
        
        prompt = f"""You are an expert Maya spiritual guide and ancient wisdom keeper. Create a deeply personalized spiritual explanation for {user_name}'s {element_display_name}: {element_value}.

User's Cosmic Profile:
- Name: {user_name}
- Day Sign: {day_sign_name}
- Current Element: {element_display_name} = {element_value}
- Additional Context: {user_context}

Create a comprehensive, personalized explanation that includes:

1. **Personal Spiritual Alliance**: How this {element_display_name} specifically serves {user_name}'s spiritual journey
2. **Ancient Maya Wisdom**: Historical and cultural significance in Maya cosmology
3. **Practical Application**: How {user_name} can work with this energy daily
4. **Integration with Day Sign**: How this element enhances their {day_sign_name} nature
5. **Spiritual Gifts**: Unique abilities this element provides
6. **Sacred Mission**: How this element supports their life purpose

Requirements:
- Use {user_name}'s name throughout for personalization
- Write 800-1200 words of deeply spiritual, transformative content
- Include specific references to their {day_sign_name} Day Sign
- Provide practical spiritual guidance and daily practices
- End with "The Magic is YOU, {user_name}" followed by a personalized affirmation
- Write in an inspiring, mystical tone that makes them feel deeply seen and understood

Generate the complete personalized explanation now:"""

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text if response.content else ""
            if len(content) > 500:
                return content
                
        except Exception as e:
            print(f"Anthropic API error: {e}")
            
        return ""
    
    def _generate_fallback_explanation(self, element_type: str, element_value: str, user_data: Dict[str, Any]) -> str:
        """Generate comprehensive fallback explanation with personalized templates"""
        
        user_name = user_data.get("first_name", "Soul Seeker")
        day_sign_data = user_data.get("day_sign", {})
        if isinstance(day_sign_data, str):
            try:
                day_sign_data = json.loads(day_sign_data)
            except:
                day_sign_data = {"name": "Unknown"}
        
        day_sign_name = day_sign_data.get("name", "Unknown")
        element_display_name = self.element_display_names.get(element_type, element_type)
        
        # Get element data from database
        element_data = self._get_element_data(element_type, element_value)
        
        if not element_data:
            # Create basic personalized explanation if no database entry
            return self._create_basic_personalized_explanation(element_type, element_value, user_name, day_sign_name)
        
        # Extract data from element database
        element_name = element_data.get("name", element_value)
        element_meaning = element_data.get("meaning", "Sacred Energy")
        element_description = element_data.get("detailed_description", "")
        
        # Create personalized explanation using template
        personalized_explanation = f"""
🌟 **{element_display_name} - Your Sacred {element_name} Alliance**

Dear {user_name}, your {element_display_name} of {element_name} carries profound spiritual significance for your unique cosmic journey. This sacred element is intricately connected to your {day_sign_name} Day Sign, creating a powerful alliance that enhances your spiritual gifts and life purpose.

**🏛️ Ancient Maya Wisdom & {element_name} Teachings:**
Throughout Maya spiritual traditions, {element_name} represents {element_meaning} and serves as a bridge between earthly consciousness and divine wisdom. Ancient Maya wisdom keepers understood that {element_name} energy carries the cellular memory of cosmic creation itself, providing guidance and support for souls on their evolutionary journey.

**🌌 Your {element_name} Sacred Alliance Integration:**
Your {element_display_name} enhances your {day_sign_name} blueprint with unique spiritual qualities:
- **Cosmic Resonance**: {user_name}, you carry the vibrational frequency of {element_name} that aligns with your highest spiritual purpose
- **Divine Gift Amplification**: This element amplifies your natural {day_sign_name} abilities and spiritual gifts
- **Sacred Mission Support**: {element_name} provides the energetic foundation for your life's spiritual work
- **Conscious Evolution**: This alliance supports your transformation and spiritual awakening journey

**✨ Core {element_name} Spiritual Medicine:**
- **Energetic Alignment**: You embody the sacred essence of {element_name} in your daily spiritual practices
- **Healing Transmission**: You channel {element_name} energy for personal and collective healing
- **Wisdom Integration**: You access ancient knowledge through your connection to {element_name}
- **Divine Service**: You serve others through the unique gifts that {element_name} provides

**🎯 Sacred Mission & Divine Purpose:**
Your {element_name} alliance serves your spiritual evolution through:
- Embodying the sacred qualities of {element_name} in your daily life and relationships
- Sharing the wisdom and healing energy of {element_name} with those who need spiritual support
- Integrating {element_name} teachings with your {day_sign_name} nature for maximum spiritual impact
- Serving as a living example of how {element_name} energy can transform consciousness

**🔮 Daily {element_name} Spiritual Practices:**
- **Sacred Connection**: {user_name}, spend time daily connecting with {element_name} energy through meditation or prayer
- **Energetic Embodiment**: Visualize {element_name} light flowing through your being, activating your spiritual gifts
- **Healing Work**: Use {element_name} energy for self-healing and sending healing to others
- **Wisdom Seeking**: Study the deeper meanings of {element_name} and how it relates to your spiritual journey
- **Divine Service**: Find ways to share {element_name} blessings with your community and the world

**🌟 The Magic is YOU, {user_name}:**
Through your sacred alliance with {element_name} and perfect integration with your {day_sign_name} cosmic signature, you embody the divine truth that spiritual evolution happens through conscious partnership with cosmic forces. You demonstrate that ancient wisdom lives within modern souls, that sacred alliances provide unlimited support for growth, and that when we align with our cosmic elements, we become channels for divine transformation.

The Magic is YOU, {user_name}, as you embody the sacred essence of {element_name} and show the world that spiritual awakening is possible for all who open their hearts to cosmic wisdom and divine love.
"""
        
        # If we have detailed description from database, use it
        if element_description and len(element_description) > 1000:
            # Replace placeholders in detailed description
            personalized_description = element_description.replace("{user_name}", user_name)
            personalized_description = personalized_description.replace("{day_sign}", day_sign_name)
            return personalized_description
        
        return personalized_explanation
    
    def _get_element_data(self, element_type: str, element_value: str) -> Optional[Dict[str, Any]]:
        """Get element data from appropriate database"""
        
        database = self.element_databases.get(element_type)
        if not database:
            return None
            
        # Try exact match first
        if element_value in database:
            return database[element_value]
            
        # Try case-insensitive match
        for key, value in database.items():
            if key.lower() == element_value.lower():
                return value
                
        # Try partial match
        for key, value in database.items():
            if element_value.lower() in key.lower() or key.lower() in element_value.lower():
                return value
                
        return None
    
    def _create_basic_personalized_explanation(self, element_type: str, element_value: str, user_name: str, day_sign_name: str) -> str:
        """Create basic personalized explanation when no database entry exists"""
        
        element_display_name = self.element_display_names.get(element_type, element_type)
        
        return f"""
🌟 **{element_display_name} - Your Sacred {element_value} Energy**

Dear {user_name}, your {element_display_name} of {element_value} carries profound spiritual significance for your unique cosmic journey. This sacred element is intricately connected to your {day_sign_name} Day Sign, creating a powerful spiritual alliance that enhances your natural gifts and life purpose.

**🏛️ Ancient Maya Wisdom & {element_value} Teachings:**
Throughout Maya spiritual traditions, {element_value} represents a sacred cosmic force that guides souls on their evolutionary journey. Ancient Maya wisdom keepers understood that every cosmic element carries unique vibrations and teachings that support spiritual growth and conscious evolution.

**🌌 Your {element_value} Sacred Alliance:**
Your {element_display_name} enhances your {day_sign_name} blueprint with unique spiritual qualities:
- **Cosmic Resonance**: {user_name}, you carry the vibrational frequency of {element_value} that aligns with your highest spiritual purpose
- **Divine Gift Amplification**: This element amplifies your natural {day_sign_name} abilities and spiritual gifts
- **Sacred Mission Support**: {element_value} provides energetic foundation for your life's spiritual work
- **Conscious Evolution**: This alliance supports your transformation and spiritual awakening journey

**✨ Core {element_value} Spiritual Medicine:**
- **Energetic Alignment**: You embody the sacred essence of {element_value} in your daily spiritual practices
- **Healing Transmission**: You channel {element_value} energy for personal and collective healing
- **Wisdom Integration**: You access ancient knowledge through your connection to {element_value}
- **Divine Service**: You serve others through the unique gifts that {element_value} provides

**🎯 Sacred Mission & Divine Purpose:**
Your {element_value} alliance serves your spiritual evolution by helping you embody its sacred qualities in daily life, share its wisdom with others, and integrate its teachings with your {day_sign_name} nature for maximum spiritual impact.

**🔮 Daily {element_value} Spiritual Practices:**
- Connect with {element_value} energy through meditation and prayer
- Visualize {element_value} light flowing through your being
- Use {element_value} energy for healing work and divine service
- Study the deeper meanings of {element_value} and its spiritual significance

**🌟 The Magic is YOU, {user_name}:**
Through your sacred alliance with {element_value} and perfect integration with your {day_sign_name} cosmic signature, you embody the divine truth that spiritual evolution happens through conscious partnership with cosmic forces. The Magic is YOU, {user_name}, as you embody the sacred essence of {element_value} and demonstrate that ancient wisdom lives within modern souls ready to serve divine love.
"""

# Create global instance
personalized_content_engine = PersonalizedContentEngine()

def generate_personalized_content(element_type: str, element_value: str, user_data: Dict[str, Any]) -> str:
    """Generate personalized content for any cosmic element"""
    return personalized_content_engine.generate_personalized_explanation(element_type, element_value, user_data)