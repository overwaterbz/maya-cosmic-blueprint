#!/usr/bin/env python3
"""
AI Personalization Engine - Phase 3 Enhancement
Advanced AI-powered content generation with user preference learning
"""

import json
import time
from openai import OpenAI
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
from collections import defaultdict, deque

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class PersonalizationDepth(Enum):
    SURFACE = "surface"
    MODERATE = "moderate"
    DEEP = "deep"
    PROFOUND = "profound"

class ContentType(Enum):
    SPIRITUAL_GUIDANCE = "spiritual_guidance"
    DAILY_INSIGHT = "daily_insight"
    COSMIC_EXPLANATION = "cosmic_explanation"
    SOUL_MESSAGE = "soul_message"
    MEDITATION_GUIDE = "meditation_guide"
    RITUAL_INSTRUCTION = "ritual_instruction"
    PROPHETIC_VISION = "prophetic_vision"

class UserEngagementPattern(Enum):
    SEEKER = "seeker"           # Questions and explores
    PRACTITIONER = "practitioner" # Takes action
    CONTEMPLATOR = "contemplator" # Reflects deeply
    TRANSFORMER = "transformer"  # Actively changing
    TEACHER = "teacher"          # Shares wisdom
    HEALER = "healer"           # Helps others

@dataclass
class UserPreference:
    user_id: str
    preference_type: str
    preference_value: str
    strength: float  # 0.0 to 1.0
    learned_from: str  # interaction_type that taught us this
    timestamp: datetime
    frequency: int = 1

@dataclass
class UserInteractionHistory:
    user_id: str
    interaction_type: str
    content_type: ContentType
    element_focused: str
    time_spent: float
    engagement_level: int  # 1-5
    feedback_rating: Optional[int] = None
    emotional_response: Optional[str] = None
    follow_up_questions: List[str] = None
    timestamp: datetime = None

class UserPreferenceLearningSystem:
    """Advanced machine learning system for user preference discovery"""
    
    def __init__(self):
        self.user_preferences = defaultdict(list)
        self.interaction_history = defaultdict(deque)
        self.engagement_patterns = defaultdict(dict)
        self.preference_weights = {
            'content_depth': 0.3,
            'spiritual_focus': 0.25,
            'communication_style': 0.2,
            'timing_preference': 0.15,
            'element_affinity': 0.1
        }
        self.lock = threading.Lock()
    
    def learn_from_interaction(self, interaction: UserInteractionHistory):
        """Learn user preferences from interaction patterns"""
        with self.lock:
            user_id = interaction.user_id
            
            # Store interaction history
            self.interaction_history[user_id].append(interaction)
            if len(self.interaction_history[user_id]) > 100:
                self.interaction_history[user_id].popleft()
            
            # Analyze engagement patterns
            self._analyze_engagement_pattern(interaction)
            
            # Learn content preferences
            self._learn_content_preferences(interaction)
            
            # Learn timing preferences
            self._learn_timing_preferences(interaction)
            
            # Learn spiritual focus preferences
            self._learn_spiritual_focus(interaction)
    
    def _analyze_engagement_pattern(self, interaction: UserInteractionHistory):
        """Analyze user's engagement pattern"""
        user_id = interaction.user_id
        
        # Calculate engagement metrics
        recent_interactions = list(self.interaction_history[user_id])[-10:]
        
        avg_time_spent = sum(i.time_spent for i in recent_interactions) / len(recent_interactions)
        avg_engagement = sum(i.engagement_level for i in recent_interactions) / len(recent_interactions)
        question_ratio = sum(1 for i in recent_interactions if i.follow_up_questions) / len(recent_interactions)
        
        # Determine engagement pattern
        if question_ratio > 0.7:
            pattern = UserEngagementPattern.SEEKER
        elif avg_time_spent > 300:  # 5+ minutes
            pattern = UserEngagementPattern.CONTEMPLATOR
        elif avg_engagement > 4:
            pattern = UserEngagementPattern.PRACTITIONER
        else:
            pattern = UserEngagementPattern.TRANSFORMER
        
        self.engagement_patterns[user_id]['primary_pattern'] = pattern
        self.engagement_patterns[user_id]['last_updated'] = datetime.now()
    
    def _learn_content_preferences(self, interaction: UserInteractionHistory):
        """Learn user's content depth and style preferences"""
        user_id = interaction.user_id
        
        # Determine preferred content depth based on engagement
        if interaction.engagement_level >= 4 and interaction.time_spent > 180:
            depth = PersonalizationDepth.PROFOUND
        elif interaction.engagement_level >= 3 and interaction.time_spent > 120:
            depth = PersonalizationDepth.DEEP
        elif interaction.engagement_level >= 2:
            depth = PersonalizationDepth.MODERATE
        else:
            depth = PersonalizationDepth.SURFACE
        
        # Store preference
        preference = UserPreference(
            user_id=user_id,
            preference_type="content_depth",
            preference_value=depth.value,
            strength=interaction.engagement_level / 5.0,
            learned_from=interaction.interaction_type,
            timestamp=datetime.now()
        )
        
        self._update_preference(preference)
    
    def _learn_timing_preferences(self, interaction: UserInteractionHistory):
        """Learn user's timing preferences"""
        user_id = interaction.user_id
        hour = interaction.timestamp.hour
        
        # Categorize time periods
        if 5 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 17:
            time_period = "afternoon"
        elif 17 <= hour < 21:
            time_period = "evening"
        else:
            time_period = "night"
        
        preference = UserPreference(
            user_id=user_id,
            preference_type="timing_preference",
            preference_value=time_period,
            strength=interaction.engagement_level / 5.0,
            learned_from="timing_analysis",
            timestamp=datetime.now()
        )
        
        self._update_preference(preference)
    
    def _learn_spiritual_focus(self, interaction: UserInteractionHistory):
        """Learn user's spiritual focus preferences"""
        user_id = interaction.user_id
        
        # Map elements to spiritual focuses
        spiritual_focuses = {
            'day_sign': 'identity_exploration',
            'galactic_tone': 'frequency_alignment',
            'spirit_animal': 'nature_connection',
            'crystal_ally': 'energy_healing',
            'plant_medicine': 'consciousness_expansion',
            'chakra_resonance': 'energy_centers',
            'human_design_type': 'life_strategy'
        }
        
        focus = spiritual_focuses.get(interaction.element_focused, 'general_guidance')
        
        preference = UserPreference(
            user_id=user_id,
            preference_type="spiritual_focus",
            preference_value=focus,
            strength=interaction.engagement_level / 5.0,
            learned_from=interaction.interaction_type,
            timestamp=datetime.now()
        )
        
        self._update_preference(preference)
    
    def _update_preference(self, new_preference: UserPreference):
        """Update user preference with weighted averaging"""
        user_id = new_preference.user_id
        pref_type = new_preference.preference_type
        
        # Find existing preference
        existing = None
        for pref in self.user_preferences[user_id]:
            if pref.preference_type == pref_type and pref.preference_value == new_preference.preference_value:
                existing = pref
                break
        
        if existing:
            # Update existing preference with weighted average
            total_weight = existing.frequency + 1
            existing.strength = (existing.strength * existing.frequency + new_preference.strength) / total_weight
            existing.frequency += 1
            existing.timestamp = datetime.now()
        else:
            # Add new preference
            self.user_preferences[user_id].append(new_preference)
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user preferences"""
        with self.lock:
            preferences = {}
            
            for pref in self.user_preferences[user_id]:
                if pref.preference_type not in preferences:
                    preferences[pref.preference_type] = []
                preferences[pref.preference_type].append({
                    'value': pref.preference_value,
                    'strength': pref.strength,
                    'frequency': pref.frequency,
                    'last_updated': pref.timestamp.isoformat()
                })
            
            # Sort by strength and frequency
            for pref_type in preferences:
                preferences[pref_type].sort(key=lambda x: x['strength'] * x['frequency'], reverse=True)
            
            return preferences
    
    def get_engagement_pattern(self, user_id: str) -> Optional[UserEngagementPattern]:
        """Get user's primary engagement pattern"""
        pattern_info = self.engagement_patterns.get(user_id, {})
        return pattern_info.get('primary_pattern')

class AIPersonalizationEngine:
    """Advanced AI-powered personalization engine"""
    
    def __init__(self):
        self.preference_system = UserPreferenceLearningSystem()
        self.content_cache = {}
        self.generation_queue = queue.Queue()
        self.worker_thread = None
        self.running = False
        
        # AI model configuration
        self.model_config = {
            'model': 'gpt-4o',  # Latest OpenAI model
            'temperature': 0.7,
            'max_tokens': 1500,
            'top_p': 0.9
        }
    
    def start_background_processing(self):
        """Start background content generation"""
        self.running = True
        self.worker_thread = threading.Thread(target=self._background_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def stop_background_processing(self):
        """Stop background content generation"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
    
    def _background_worker(self):
        """Background worker for content generation"""
        while self.running:
            try:
                task = self.generation_queue.get(timeout=1)
                self._process_generation_task(task)
            except queue.Empty:
                continue
    
    def _process_generation_task(self, task):
        """Process a content generation task"""
        try:
            user_id = task['user_id']
            content_type = task['content_type']
            context = task['context']
            
            # Generate content
            content = self._generate_ai_content(user_id, content_type, context)
            
            # Cache result
            cache_key = f"{user_id}:{content_type.value}:{hash(str(context))}"
            self.content_cache[cache_key] = {
                'content': content,
                'generated_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(hours=24)
            }
            
        except Exception as e:
            print(f"Background generation error: {e}")
    
    def generate_personalized_content(self, user_id: str, content_type: ContentType, 
                                    context: Dict[str, Any]) -> str:
        """Generate AI-powered personalized content"""
        
        # Check cache first
        cache_key = f"{user_id}:{content_type.value}:{hash(str(context))}"
        cached = self.content_cache.get(cache_key)
        
        if cached and cached['expires_at'] > datetime.now():
            return cached['content']
        
        # Generate new content
        content = self._generate_ai_content(user_id, content_type, context)
        
        # Cache result
        self.content_cache[cache_key] = {
            'content': content,
            'generated_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=24)
        }
        
        return content
    
    def _generate_ai_content(self, user_id: str, content_type: ContentType, 
                           context: Dict[str, Any]) -> str:
        """Generate AI content using OpenAI"""
        
        # Get user preferences
        preferences = self.preference_system.get_user_preferences(user_id)
        engagement_pattern = self.preference_system.get_engagement_pattern(user_id)
        
        # Build personalized prompt
        prompt = self._build_personalized_prompt(content_type, context, preferences, engagement_pattern)
        
        try:
            response = openai_client.chat.completions.create(
                model=self.model_config['model'],
                messages=[
                    {"role": "system", "content": self._get_system_prompt(content_type, engagement_pattern)},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.model_config['temperature'],
                max_tokens=self.model_config['max_tokens'],
                top_p=self.model_config['top_p']
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._get_fallback_content(content_type, context)
    
    def _build_personalized_prompt(self, content_type: ContentType, context: Dict[str, Any],
                                 preferences: Dict[str, Any], engagement_pattern: Optional[UserEngagementPattern]) -> str:
        """Build personalized prompt based on user preferences"""
        
        # Base context
        first_name = context.get('first_name', 'Sacred Soul')
        day_sign = context.get('day_sign', 'Maya')
        galactic_tone = context.get('galactic_tone', 'Cosmic')
        element = context.get('element', 'Spiritual')
        
        # Determine content depth
        depth_prefs = preferences.get('content_depth', [])
        depth = PersonalizationDepth.MODERATE
        if depth_prefs:
            depth = PersonalizationDepth(depth_prefs[0]['value'])
        
        # Determine spiritual focus
        focus_prefs = preferences.get('spiritual_focus', [])
        spiritual_focus = 'general_guidance'
        if focus_prefs:
            spiritual_focus = focus_prefs[0]['value']
        
        # Build prompt based on content type
        if content_type == ContentType.SPIRITUAL_GUIDANCE:
            prompt = f"""
            Create deeply personalized spiritual guidance for {first_name}, whose cosmic signature is {day_sign} {galactic_tone} with {element} element.
            
            Content depth: {depth.value}
            Spiritual focus: {spiritual_focus}
            Engagement pattern: {engagement_pattern.value if engagement_pattern else 'balanced'}
            
            Current spiritual question or area of focus: {context.get('focus_area', 'life path guidance')}
            
            Generate guidance that speaks directly to their soul's journey, incorporating their cosmic elements naturally.
            """
        
        elif content_type == ContentType.DAILY_INSIGHT:
            prompt = f"""
            Generate a daily spiritual insight for {first_name} ({day_sign} {galactic_tone}) that connects to their current life circumstances.
            
            Today's energy focus: {context.get('daily_energy', 'transformation')}
            Depth level: {depth.value}
            Spiritual focus: {spiritual_focus}
            
            Create insight that feels personally relevant and actionable for their spiritual growth.
            """
        
        elif content_type == ContentType.COSMIC_EXPLANATION:
            element_type = context.get('element_type', 'cosmic element')
            element_value = context.get('element_value', 'unknown')
            
            prompt = f"""
            Explain the cosmic element "{element_value}" ({element_type}) for {first_name}, whose signature is {day_sign} {galactic_tone}.
            
            Personalization level: {depth.value}
            Spiritual focus: {spiritual_focus}
            Connection to their cosmic signature: Include how this element specifically relates to their {day_sign} nature
            
            Make this explanation feel like it was written specifically for their spiritual journey.
            """
        
        else:
            # General prompt
            prompt = f"""
            Create personalized spiritual content for {first_name} ({day_sign} {galactic_tone}) with {element} energy.
            
            Content type: {content_type.value}
            Depth: {depth.value}
            Focus: {spiritual_focus}
            
            Context: {context}
            
            Generate content that resonates with their unique cosmic signature and spiritual path.
            """
        
        return prompt
    
    def _get_system_prompt(self, content_type: ContentType, engagement_pattern: Optional[UserEngagementPattern]) -> str:
        """Get system prompt based on content type and engagement pattern"""
        
        base_prompt = """You are an advanced AI spiritual guide with deep knowledge of Maya cosmology, chakra systems, human design, and universal spiritual principles. You create deeply personalized spiritual guidance that feels like it was written by someone who truly understands the individual's soul journey."""
        
        if engagement_pattern == UserEngagementPattern.SEEKER:
            return base_prompt + " Focus on answering deep questions and encouraging further exploration."
        elif engagement_pattern == UserEngagementPattern.PRACTITIONER:
            return base_prompt + " Provide practical, actionable spiritual guidance and specific practices."
        elif engagement_pattern == UserEngagementPattern.CONTEMPLATOR:
            return base_prompt + " Offer profound insights and encourage deep reflection."
        elif engagement_pattern == UserEngagementPattern.TRANSFORMER:
            return base_prompt + " Support active transformation and change processes."
        elif engagement_pattern == UserEngagementPattern.TEACHER:
            return base_prompt + " Provide wisdom that can be shared and taught to others."
        elif engagement_pattern == UserEngagementPattern.HEALER:
            return base_prompt + " Focus on healing wisdom and guidance for helping others."
        else:
            return base_prompt + " Provide balanced, comprehensive spiritual guidance."
    
    def _get_fallback_content(self, content_type: ContentType, context: Dict[str, Any]) -> str:
        """Fallback content when AI generation fails"""
        first_name = context.get('first_name', 'Sacred Soul')
        day_sign = context.get('day_sign', 'Maya')
        
        fallback_templates = {
            ContentType.SPIRITUAL_GUIDANCE: f"Dear {first_name}, your {day_sign} essence carries ancient wisdom that guides you toward your highest path. Trust the journey unfolding before you.",
            ContentType.DAILY_INSIGHT: f"{first_name}, today your {day_sign} energy invites you to embrace transformation and growth. Listen to your inner guidance.",
            ContentType.COSMIC_EXPLANATION: f"Your cosmic signature as {day_sign} {first_name} holds profound meaning for your spiritual journey and life purpose."
        }
        
        return fallback_templates.get(content_type, f"Sacred guidance flows to you, {first_name}, through your {day_sign} essence.")
    
    def track_interaction(self, user_id: str, interaction_type: str, content_type: ContentType,
                         element_focused: str, time_spent: float, engagement_level: int,
                         feedback_rating: Optional[int] = None, emotional_response: Optional[str] = None,
                         follow_up_questions: Optional[List[str]] = None):
        """Track user interaction for preference learning"""
        
        interaction = UserInteractionHistory(
            user_id=user_id,
            interaction_type=interaction_type,
            content_type=content_type,
            element_focused=element_focused,
            time_spent=time_spent,
            engagement_level=engagement_level,
            feedback_rating=feedback_rating,
            emotional_response=emotional_response,
            follow_up_questions=follow_up_questions or [],
            timestamp=datetime.now()
        )
        
        self.preference_system.learn_from_interaction(interaction)
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user insights and preferences"""
        preferences = self.preference_system.get_user_preferences(user_id)
        engagement_pattern = self.preference_system.get_engagement_pattern(user_id)
        
        return {
            'preferences': preferences,
            'engagement_pattern': engagement_pattern.value if engagement_pattern else None,
            'interaction_count': len(self.preference_system.interaction_history[user_id]),
            'cache_size': len(self.content_cache),
            'last_updated': datetime.now().isoformat()
        }
    
    def pregenerate_content(self, user_id: str, content_types: List[ContentType], 
                          context: Dict[str, Any]):
        """Queue content for background generation"""
        for content_type in content_types:
            task = {
                'user_id': user_id,
                'content_type': content_type,
                'context': context
            }
            self.generation_queue.put(task)

# Global instance
ai_personalization_engine = AIPersonalizationEngine()