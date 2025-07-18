#!/usr/bin/env python3
"""
Personalization Templates System - Phase 2 Scale Optimization
Efficient template-based personalization for 1000+ users
"""

import json
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import random
from datetime import datetime

class PersonalizationLevel(Enum):
    """Levels of personalization intensity"""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    PREMIUM_PLUS = "premium_plus"

@dataclass
class PersonalizationContext:
    """Context for personalization"""
    user_id: str
    first_name: str
    day_sign: str
    galactic_tone: str
    element: str
    direction: str
    spirit_animal: str
    crystal_ally: str
    plant_medicine: str
    personalization_level: PersonalizationLevel = PersonalizationLevel.STANDARD

class PersonalizationTemplateEngine:
    """Advanced template engine for scalable personalization"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.variation_patterns = self._load_variation_patterns()
        self.personalization_cache = {}
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load personalization templates for all cosmic elements"""
        return {
            "day_sign": {
                "basic": [
                    "Your {day_sign} energy brings {element} wisdom to your spiritual path.",
                    "As a {day_sign} soul, you embody the sacred essence of {element}.",
                    "The {day_sign} within you channels pure {element} transformation."
                ],
                "standard": [
                    "Dear {first_name}, your {day_sign} essence carries the transformative power of {element}, guiding you through life's sacred cycles with {galactic_tone} energy.",
                    "Your {day_sign} spirit, {first_name}, embodies the ancient wisdom of {element} from the {direction} direction, supported by your {spirit_animal} guide.",
                    "The {galactic_tone} {day_sign} within you, {first_name}, brings forth {element} mastery and spiritual leadership in the {direction} realm."
                ],
                "premium": [
                    "Sacred {first_name}, your {day_sign} incarnation represents mastery over {element} consciousness, working with {galactic_tone} frequency to manifest divine will through {direction} pathway guidance. Your {spirit_animal} spirit guide and {crystal_ally} ally support this profound transformation.",
                    "Blessed {first_name}, as a {galactic_tone} {day_sign}, you carry the cosmic responsibility of {element} stewardship, channeling ancient wisdom from the {direction} sacred direction while your {plant_medicine} medicine supports your spiritual evolution.",
                    "Divine {first_name}, your {day_sign} soul signature activates {element} mastery through {galactic_tone} vibration, creating ripples of transformation that extend from the {direction} realm into all dimensions of existence."
                ]
            },
            "galactic_tone": {
                "basic": [
                    "Your {galactic_tone} tone brings {element} balance to your journey.",
                    "The {galactic_tone} frequency activates your {day_sign} potential.",
                    "Through {galactic_tone} energy, you master {element} wisdom."
                ],
                "standard": [
                    "{first_name}, your {galactic_tone} tone creates perfect harmony between your {day_sign} essence and {element} mastery.",
                    "The {galactic_tone} frequency within you, {first_name}, amplifies your {day_sign} gifts and {element} understanding.",
                    "Your {galactic_tone} vibration, {first_name}, orchestrates the divine dance between {day_sign} wisdom and {element} transformation."
                ],
                "premium": [
                    "Sacred {first_name}, your {galactic_tone} tone serves as the cosmic tuning fork that harmonizes your {day_sign} essence with {element} mastery, creating resonance patterns that attract {spirit_animal} wisdom and {crystal_ally} support for your spiritual mission.",
                    "Beloved {first_name}, through {galactic_tone} frequency, you become a living bridge between {day_sign} ancient knowledge and {element} contemporary application, guided by {direction} wisdom and supported by {plant_medicine} healing.",
                    "Divine {first_name}, your {galactic_tone} tone activates the sacred geometry within your {day_sign} blueprint, enabling {element} mastery that transforms not only your path but creates healing ripples throughout the collective consciousness."
                ]
            },
            "spirit_animal": {
                "basic": [
                    "Your {spirit_animal} guide brings {element} protection and wisdom.",
                    "The {spirit_animal} spirit supports your {day_sign} journey.",
                    "Through {spirit_animal} energy, you access ancient {element} knowledge."
                ],
                "standard": [
                    "{first_name}, your {spirit_animal} guide embodies the perfect blend of {element} wisdom and {day_sign} strength for your spiritual path.",
                    "The {spirit_animal} spirit walks beside you, {first_name}, offering {element} guidance and {galactic_tone} support in all your endeavors.",
                    "Your {spirit_animal} ally, {first_name}, bridges the gap between {day_sign} ancient wisdom and modern {element} application."
                ],
                "premium": [
                    "Sacred {first_name}, your {spirit_animal} guide serves as the cosmic messenger between your {day_sign} soul essence and {element} mastery, carrying {galactic_tone} frequency wisdom from the {direction} realm to support your divine mission on Earth.",
                    "Blessed {first_name}, the {spirit_animal} spirit chose you for its profound connection to {element} consciousness and {day_sign} wisdom, offering protection and guidance as you navigate your {galactic_tone} frequency transformation.",
                    "Divine {first_name}, your {spirit_animal} ally embodies the living essence of {element} power channeled through {day_sign} ancient knowledge, creating a sacred partnership that amplifies your {galactic_tone} healing abilities."
                ]
            },
            "crystal_ally": {
                "basic": [
                    "Your {crystal_ally} crystal amplifies {element} energy in your life.",
                    "The {crystal_ally} supports your {day_sign} spiritual growth.",
                    "Through {crystal_ally} vibration, you enhance {element} connection."
                ],
                "standard": [
                    "{first_name}, your {crystal_ally} crystal resonates perfectly with your {day_sign} essence and {element} mastery.",
                    "The {crystal_ally} serves as your energetic anchor, {first_name}, amplifying {galactic_tone} frequency and {element} wisdom.",
                    "Your {crystal_ally} ally, {first_name}, creates a sacred bridge between {day_sign} ancient knowledge and {element} contemporary healing."
                ],
                "premium": [
                    "Sacred {first_name}, your {crystal_ally} crystal was formed in Earth's depths to specifically support your {day_sign} incarnation and {element} mastery, holding {galactic_tone} frequency patterns that align with your spiritual mission from the {direction} realm.",
                    "Beloved {first_name}, the {crystal_ally} crystal serves as your personal healing temple, amplifying {element} consciousness while grounding {day_sign} wisdom through {galactic_tone} vibration for maximum spiritual transformation.",
                    "Divine {first_name}, your {crystal_ally} ally contains the crystallized essence of {element} power merged with {day_sign} ancient knowledge, creating a sacred tool that enhances your {galactic_tone} healing abilities and spiritual leadership."
                ]
            },
            "plant_medicine": {
                "basic": [
                    "Your {plant_medicine} medicine supports {element} healing and growth.",
                    "The {plant_medicine} plant allies with your {day_sign} journey.",
                    "Through {plant_medicine} wisdom, you deepen {element} connection."
                ],
                "standard": [
                    "{first_name}, your {plant_medicine} medicine perfectly complements your {day_sign} essence and {element} mastery.",
                    "The {plant_medicine} plant spirit offers healing support, {first_name}, for your {galactic_tone} frequency and {element} transformation.",
                    "Your {plant_medicine} ally, {first_name}, provides gentle guidance for integrating {day_sign} wisdom with {element} healing."
                ],
                "premium": [
                    "Sacred {first_name}, your {plant_medicine} medicine carries the living essence of {element} healing merged with {day_sign} ancient wisdom, offering {galactic_tone} frequency support for your spiritual transformation from the {direction} sacred realm.",
                    "Blessed {first_name}, the {plant_medicine} plant spirit chose to support your {day_sign} incarnation through {element} healing, providing gentle yet powerful medicine that aligns with your {galactic_tone} frequency and spiritual mission.",
                    "Divine {first_name}, your {plant_medicine} ally serves as the botanical bridge between {element} consciousness and {day_sign} wisdom, offering sacred healing that enhances your {galactic_tone} abilities and spiritual leadership."
                ]
            }
        }
    
    def _load_variation_patterns(self) -> Dict[str, List[str]]:
        """Load variation patterns for dynamic content"""
        return {
            "greetings": [
                "Dear {first_name},", "Sacred {first_name},", "Blessed {first_name},",
                "Divine {first_name},", "Beloved {first_name},", "{first_name},"
            ],
            "transitions": [
                "Furthermore,", "Additionally,", "In this sacred light,", "Through this wisdom,",
                "As you embody this truth,", "With this understanding,", "In your spiritual journey,"
            ],
            "closings": [
                "Trust in your divine purpose.", "Remember: The Magic is You!",
                "Your spiritual journey is sacred.", "Embrace your cosmic destiny.",
                "You are a divine being of light.", "Your path is blessed."
            ],
            "power_words": [
                "sacred", "divine", "blessed", "powerful", "transformative", "magical",
                "ancient", "cosmic", "spiritual", "enlightened", "awakened", "evolved"
            ]
        }
    
    def generate_personalized_content(self, element_type: str, context: PersonalizationContext) -> str:
        """Generate personalized content using templates"""
        templates = self.templates.get(element_type, {})
        level_templates = templates.get(context.personalization_level.value, templates.get("standard", []))
        
        if not level_templates:
            return self._generate_fallback_content(element_type, context)
        
        # Select template based on user pattern or random
        template_index = hash(context.user_id + element_type) % len(level_templates)
        template = level_templates[template_index]
        
        # Apply personalization context
        personalized_content = template.format(
            first_name=context.first_name,
            day_sign=context.day_sign,
            galactic_tone=context.galactic_tone,
            element=context.element,
            direction=context.direction,
            spirit_animal=context.spirit_animal,
            crystal_ally=context.crystal_ally,
            plant_medicine=context.plant_medicine
        )
        
        # Add variations for premium content
        if context.personalization_level in [PersonalizationLevel.PREMIUM, PersonalizationLevel.PREMIUM_PLUS]:
            personalized_content = self._enhance_with_variations(personalized_content, context)
        
        return personalized_content
    
    def _enhance_with_variations(self, content: str, context: PersonalizationContext) -> str:
        """Enhance content with dynamic variations"""
        # Add greeting variation
        greeting = self._select_variation("greetings", context)
        if not content.startswith(greeting.split()[0]):
            content = f"{greeting} {content}"
        
        # Add power words
        power_words = self.variation_patterns["power_words"]
        for _ in range(2):  # Add 2 power words
            word = self._select_variation("power_words", context)
            if word not in content:
                content = content.replace(" wisdom", f" {word} wisdom")
                break
        
        # Add closing for premium plus
        if context.personalization_level == PersonalizationLevel.PREMIUM_PLUS:
            closing = self._select_variation("closings", context)
            content += f" {closing}"
        
        return content
    
    def _select_variation(self, pattern_type: str, context: PersonalizationContext) -> str:
        """Select variation based on user pattern"""
        variations = self.variation_patterns.get(pattern_type, [])
        if not variations:
            return ""
        
        # Use hash for consistent selection per user
        index = hash(context.user_id + pattern_type) % len(variations)
        return variations[index]
    
    def _generate_fallback_content(self, element_type: str, context: PersonalizationContext) -> str:
        """Generate fallback content when templates are missing"""
        return f"Your {element_type} carries the essence of {context.element} wisdom, {context.first_name}. This sacred aspect of your {context.day_sign} nature brings transformation and growth to your spiritual journey."
    
    def generate_bulk_personalization(self, element_type: str, contexts: List[PersonalizationContext]) -> Dict[str, str]:
        """Generate personalized content for multiple users efficiently"""
        results = {}
        
        # Pre-load templates for efficiency
        templates = self.templates.get(element_type, {})
        
        for context in contexts:
            try:
                content = self.generate_personalized_content(element_type, context)
                results[context.user_id] = content
            except Exception as e:
                # Fallback for any errors
                results[context.user_id] = self._generate_fallback_content(element_type, context)
        
        return results
    
    def get_personalization_stats(self) -> Dict[str, Any]:
        """Get personalization system statistics"""
        total_templates = sum(len(templates) for templates in self.templates.values())
        total_variations = sum(len(variations) for variations in self.variation_patterns.values())
        
        return {
            "total_templates": total_templates,
            "total_variations": total_variations,
            "supported_elements": list(self.templates.keys()),
            "personalization_levels": [level.value for level in PersonalizationLevel],
            "cache_size": len(self.personalization_cache)
        }

# Template engine instance
template_engine = PersonalizationTemplateEngine()

# Convenience functions for common use cases
def generate_user_element_content(user_id: str, first_name: str, day_sign: str, 
                                galactic_tone: str, element: str, direction: str,
                                spirit_animal: str, crystal_ally: str, plant_medicine: str,
                                element_type: str, personalization_level: str = "standard") -> str:
    """Generate personalized content for a single user element"""
    context = PersonalizationContext(
        user_id=user_id,
        first_name=first_name,
        day_sign=day_sign,
        galactic_tone=galactic_tone,
        element=element,
        direction=direction,
        spirit_animal=spirit_animal,
        crystal_ally=crystal_ally,
        plant_medicine=plant_medicine,
        personalization_level=PersonalizationLevel(personalization_level)
    )
    
    return template_engine.generate_personalized_content(element_type, context)

def generate_dashboard_content(user_profile: Dict[str, Any]) -> Dict[str, str]:
    """Generate all personalized content for user dashboard"""
    context = PersonalizationContext(
        user_id=user_profile.get('user_id', ''),
        first_name=user_profile.get('first_name', 'Sacred Soul'),
        day_sign=user_profile.get('day_sign', 'Maya'),
        galactic_tone=user_profile.get('galactic_tone', 'Cosmic'),
        element=user_profile.get('element', 'Spiritual'),
        direction=user_profile.get('direction', 'Path'),
        spirit_animal=user_profile.get('spirit_animal', 'Sacred Guide'),
        crystal_ally=user_profile.get('crystal_ally', 'Divine Crystal'),
        plant_medicine=user_profile.get('plant_medicine', 'Sacred Medicine'),
        personalization_level=PersonalizationLevel.STANDARD
    )
    
    # Generate content for all major elements
    element_types = ['day_sign', 'galactic_tone', 'spirit_animal', 'crystal_ally', 'plant_medicine']
    content = {}
    
    for element_type in element_types:
        content[element_type] = template_engine.generate_personalized_content(element_type, context)
    
    return content

if __name__ == "__main__":
    # Test personalization templates
    print("Testing Personalization Templates...")
    
    # Test single user
    test_context = PersonalizationContext(
        user_id="test_user_123",
        first_name="Maya",
        day_sign="Ahau",
        galactic_tone="Galactic",
        element="Fire",
        direction="South",
        spirit_animal="Jaguar",
        crystal_ally="Amethyst",
        plant_medicine="Sage",
        personalization_level=PersonalizationLevel.PREMIUM
    )
    
    content = template_engine.generate_personalized_content("day_sign", test_context)
    print(f"Sample personalized content: {content}")
    
    # Test system stats
    stats = template_engine.get_personalization_stats()
    print(f"Template system stats: {stats}")
    
    print("Personalization templates ready for 1000+ users!")