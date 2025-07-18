"""
AI Spiritual Engine - Advanced Machine Learning Integration for Dynamic Spiritual Enlightenment
Provides continuous learning, personalized insights, and evolving spiritual guidance
"""

import os
import json
import datetime
import anthropic
import numpy as np
from typing import Dict, List, Any, Optional
import hashlib
import pickle
from dataclasses import dataclass, asdict
from cosmic_elements_database import get_comprehensive_element_explanation, MAYA_DAY_SIGNS, GALACTIC_TONES

@dataclass
class UserInteraction:
    """Track user interactions for machine learning"""
    user_id: str
    interaction_type: str
    element_accessed: str
    time_spent: float
    engagement_level: int
    timestamp: datetime.datetime
    user_feedback: Optional[str] = None
    
class SpiritualMLEngine:
    """Machine Learning Engine for Continuous Spiritual Enlightenment"""
    
    def __init__(self):
        try:
            self.client = anthropic.Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY")
            )
        except Exception as e:
            print(f"Warning: Failed to initialize Anthropic client: {e}")
            self.client = None
        self.user_interactions = []
        self.learning_models = {}
        
    def track_user_interaction(self, user_id: str, interaction_type: str, 
                              element_accessed: str, time_spent: float, 
                              engagement_level: int, user_feedback: str = None):
        """Track user interaction for continuous learning"""
        interaction = UserInteraction(
            user_id=user_id,
            interaction_type=interaction_type,
            element_accessed=element_accessed,
            time_spent=time_spent,
            engagement_level=engagement_level,
            timestamp=datetime.datetime.now(),
            user_feedback=user_feedback
        )
        self.user_interactions.append(interaction)
        
        # Save interaction to database for persistence
        self._save_interaction_to_db(interaction)
        
    def _save_interaction_to_db(self, interaction: UserInteraction):
        """Save interaction to database for ML training"""
        try:
            import psycopg2
            conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    interaction_type TEXT NOT NULL,
                    element_accessed TEXT NOT NULL,
                    time_spent FLOAT NOT NULL,
                    engagement_level INTEGER NOT NULL,
                    user_feedback TEXT,
                    timestamp TIMESTAMP NOT NULL
                )
            """)
            
            cursor.execute("""
                INSERT INTO user_interactions 
                (user_id, interaction_type, element_accessed, time_spent, 
                 engagement_level, user_feedback, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                interaction.user_id,
                interaction.interaction_type,
                interaction.element_accessed,
                interaction.time_spent,
                interaction.engagement_level,
                interaction.user_feedback,
                interaction.timestamp
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving interaction: {e}")
    
    def analyze_user_spiritual_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's spiritual engagement patterns using ML"""
        try:
            import psycopg2
            conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT interaction_type, element_accessed, time_spent, 
                       engagement_level, user_feedback, timestamp
                FROM user_interactions 
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT 100
            """, (user_id,))
            
            interactions = cursor.fetchall()
            conn.close()
            
            if not interactions:
                return {
                    "total_interactions": 0,
                    "preferred_elements": [],
                    "engagement_trend": "new_user",
                    "spiritual_focus_areas": [],
                    "recommended_next_steps": []
                }
            
            # Analyze patterns
            element_engagement = {}
            total_time = 0
            engagement_levels = []
            
            for interaction in interactions:
                interaction_type, element, time_spent, engagement, feedback, timestamp = interaction
                
                if element not in element_engagement:
                    element_engagement[element] = {
                        "total_time": 0,
                        "avg_engagement": 0,
                        "interaction_count": 0
                    }
                
                element_engagement[element]["total_time"] += time_spent
                element_engagement[element]["interaction_count"] += 1
                total_time += time_spent
                engagement_levels.append(engagement)
            
            # Calculate averages
            for element in element_engagement:
                count = element_engagement[element]["interaction_count"]
                element_engagement[element]["avg_time"] = element_engagement[element]["total_time"] / count
            
            # Sort by engagement
            preferred_elements = sorted(
                element_engagement.items(),
                key=lambda x: x[1]["total_time"],
                reverse=True
            )[:5]
            
            # Determine spiritual focus areas
            spiritual_focus_areas = self._determine_spiritual_focus(preferred_elements)
            
            # Generate recommendations
            recommendations = self._generate_ml_recommendations(user_id, element_engagement)
            
            return {
                "total_interactions": len(interactions),
                "total_time_spent": total_time,
                "preferred_elements": [elem[0] for elem in preferred_elements],
                "avg_engagement": sum(engagement_levels) / len(engagement_levels),
                "engagement_trend": self._calculate_engagement_trend(engagement_levels),
                "spiritual_focus_areas": spiritual_focus_areas,
                "recommended_next_steps": recommendations
            }
            
        except Exception as e:
            print(f"Error analyzing spiritual patterns: {e}")
            return {"error": str(e)}
    
    def _determine_spiritual_focus(self, preferred_elements: List) -> List[str]:
        """Determine user's spiritual focus areas based on element preferences"""
        focus_areas = []
        
        for element_name, data in preferred_elements:
            if "day_sign" in element_name.lower():
                focus_areas.append("Maya Wisdom & Ancient Teachings")
            elif "galactic_tone" in element_name.lower():
                focus_areas.append("Cosmic Harmony & Universal Flow")
            elif "spirit_animal" in element_name.lower():
                focus_areas.append("Animal Spirit Guidance")
            elif "crystal" in element_name.lower():
                focus_areas.append("Crystal Healing & Energy Work")
            elif "chakra" in element_name.lower():
                focus_areas.append("Energy Center Balancing")
            elif "plant_medicine" in element_name.lower():
                focus_areas.append("Plant Spirit Medicine")
        
        return list(set(focus_areas))
    
    def _generate_ml_recommendations(self, user_id: str, element_engagement: Dict) -> List[str]:
        """Generate personalized recommendations using ML analysis"""
        recommendations = []
        
        # Find least explored areas
        all_elements = ["day_sign", "galactic_tone", "spirit_animal", "crystal_ally", 
                       "plant_medicine", "chakra_resonance", "human_design_type"]
        
        unexplored = [elem for elem in all_elements if elem not in element_engagement]
        
        if unexplored:
            recommendations.append(f"Explore your {unexplored[0].replace('_', ' ').title()} for new insights")
        
        # Recommend based on engagement patterns
        if element_engagement:
            most_engaged = max(element_engagement.items(), key=lambda x: x[1]["total_time"])
            recommendations.append(f"Deepen your {most_engaged[0].replace('_', ' ').title()} practice")
        
        recommendations.append("Schedule daily cosmic meditation sessions")
        recommendations.append("Journal your spiritual insights for deeper integration")
        
        return recommendations
    
    def _calculate_engagement_trend(self, engagement_levels: List[int]) -> str:
        """Calculate user engagement trend"""
        if len(engagement_levels) < 3:
            return "new_user"
        
        recent = engagement_levels[:10]
        older = engagement_levels[10:20] if len(engagement_levels) > 10 else engagement_levels
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def generate_personalized_headline_snapshot(self, user_id: str, user_data: Dict) -> str:
        """Generate AI-powered personalized headline snapshot"""
        try:
            # Get user's spiritual patterns
            patterns = self.analyze_user_spiritual_patterns(user_id)
            
            # Create personalized prompt
            prompt = f"""
            Create a personalized spiritual headline snapshot for {user_data.get('first_name', 'this soul')} based on their cosmic blueprint:
            
            User Profile:
            - Name: {user_data.get('first_name', 'Sacred Soul')}
            - Day Sign: {user_data.get('day_sign', 'Unknown')}
            - Galactic Tone: {user_data.get('galactic_tone', 'Unknown')}
            - Element: {user_data.get('element', 'Unknown')}
            - Birth Date: {user_data.get('birth_date', 'Unknown')}
            
            Spiritual Engagement Patterns:
            - Total Interactions: {patterns.get('total_interactions', 0)}
            - Preferred Elements: {patterns.get('preferred_elements', [])}
            - Engagement Trend: {patterns.get('engagement_trend', 'new_user')}
            - Focus Areas: {patterns.get('spiritual_focus_areas', [])}
            
            Create a powerful, personalized headline (2-3 sentences) that:
            1. Addresses them by name
            2. Highlights their unique spiritual gifts
            3. Connects to their cosmic blueprint
            4. Inspires their spiritual journey
            5. Reflects their current engagement level
            
            Make it mystical, empowering, and deeply personal.
            
            IMPORTANT: Do not include any "Note:" sections or explanatory text. Only provide the personalized spiritual message.
            """
            
            if self.client is None:
                return f"🌟 {user_data.get('first_name', 'Sacred Soul')}, you are a divine being of light, carrying the wisdom of the cosmos within your soul. Your spiritual journey is uniquely yours, guided by ancient Maya wisdom and cosmic intelligence. The Magic is You! ✨"
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            return f"🌟 {user_data.get('first_name', 'Sacred Soul')}, you are a divine being of light, carrying the wisdom of the cosmos within your soul. Your spiritual journey is uniquely yours, guided by ancient Maya wisdom and cosmic intelligence. The Magic is You! ✨"
    
    def generate_enhanced_blueprint_analysis(self, user_id: str, user_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive AI-powered blueprint analysis"""
        try:
            # Get user's spiritual patterns
            patterns = self.analyze_user_spiritual_patterns(user_id)
            
            # Create comprehensive analysis prompt
            prompt = f"""
            Provide a comprehensive spiritual blueprint analysis for {user_data.get('first_name', 'this soul')}:
            
            Cosmic Blueprint:
            - Day Sign: {user_data.get('day_sign', 'Unknown')}
            - Galactic Tone: {user_data.get('galactic_tone', 'Unknown')}
            - Element: {user_data.get('element', 'Unknown')}
            - Kin Number: {user_data.get('kin_number', 'Unknown')}
            - Direction: {user_data.get('direction', 'Unknown')}
            - Life Path: {user_data.get('life_path', 'Unknown')}
            
            Spiritual Engagement:
            - Interactions: {patterns.get('total_interactions', 0)}
            - Preferred Elements: {patterns.get('preferred_elements', [])}
            - Focus Areas: {patterns.get('spiritual_focus_areas', [])}
            - Engagement Trend: {patterns.get('engagement_trend', 'new_user')}
            
            Provide analysis in these sections:
            1. Soul Essence - Their core spiritual nature
            2. Divine Gifts - Their unique spiritual abilities
            3. Sacred Mission - Their life purpose and calling
            4. Growth Opportunities - Areas for spiritual development
            5. Cosmic Connections - How they relate to universal energy
            6. Practical Guidance - Daily spiritual practices
            
            Make it deeply personal, mystical, and actionable.
            """
            
            if self.client is None:
                return {
                    "full_analysis": f"🌟 {user_data.get('first_name', 'Sacred Soul')}, your cosmic blueprint reveals a magnificent spiritual being connected to the ancient wisdom of the Maya. Your journey is one of continuous growth, guided by the cosmic forces that shape our universe. The Magic is You!",
                    "personalization_level": "basic",
                    "error": "AI service unavailable",
                    "generated_at": datetime.datetime.now().isoformat()
                }
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis_text = message.content[0].text.strip()
            
            # Structure the response
            return {
                "full_analysis": analysis_text,
                "personalization_level": "high",
                "ml_insights": patterns,
                "generated_at": datetime.datetime.now().isoformat(),
                "user_id": user_id
            }
            
        except Exception as e:
            return {
                "full_analysis": f"🌟 {user_data.get('first_name', 'Sacred Soul')}, your cosmic blueprint reveals a magnificent spiritual being connected to the ancient wisdom of the Maya. Your journey is one of continuous growth, guided by the cosmic forces that shape our universe. The Magic is You!",
                "personalization_level": "basic",
                "error": str(e),
                "generated_at": datetime.datetime.now().isoformat()
            }
    
    def generate_enhanced_soul_contract(self, user_id: str, user_data: Dict) -> str:
        """Generate AI-powered soul contract with ML personalization"""
        try:
            # Get user's spiritual patterns
            patterns = self.analyze_user_spiritual_patterns(user_id)
            
            # Create soul contract prompt
            prompt = f"""
            Create a sacred soul contract for {user_data.get('first_name', 'this soul')} based on their complete cosmic blueprint:
            
            Cosmic Identity:
            - Name: {user_data.get('first_name', 'Sacred Soul')}
            - Day Sign: {user_data.get('day_sign', 'Unknown')}
            - Galactic Tone: {user_data.get('galactic_tone', 'Unknown')}
            - Element: {user_data.get('element', 'Unknown')}
            - Birth Details: {user_data.get('birth_date', 'Unknown')}
            
            Spiritual Evolution Data:
            - Total Spiritual Interactions: {patterns.get('total_interactions', 0)}
            - Preferred Wisdom Areas: {patterns.get('preferred_elements', [])}
            - Spiritual Focus: {patterns.get('spiritual_focus_areas', [])}
            - Growth Trajectory: {patterns.get('engagement_trend', 'new_user')}
            
            Create a mystical soul contract that includes:
            
            📜 **SACRED SOUL CONTRACT**
            **For: {user_data.get('first_name', 'Sacred Soul')}**
            
            🌟 **SOUL ORIGINS & COSMIC LINEAGE**
            (Their spiritual heritage and cosmic connections)
            
            ✨ **SACRED GIFTS & DIVINE ABILITIES**
            (Their unique spiritual talents and powers)
            
            🎯 **DIVINE MISSION & LIFE PURPOSE**
            (Their soul's mission in this lifetime)
            
            🔮 **GROWTH CHALLENGES & SOUL LESSONS**
            (What they came to learn and overcome)
            
            💫 **COSMIC SUPPORT SYSTEM**
            (Their spiritual allies and guidance)
            
            🌿 **DAILY SACRED PRACTICES**
            (Personalized spiritual practices based on their engagement)
            
            🌈 **SOUL SIGNATURE & COSMIC SEAL**
            (Their unique spiritual identification)
            
            Make it feel like an ancient, sacred document written before their incarnation.
            Include specific references to their Maya cosmic elements and ML insights.
            """
            
            if self.client is None:
                return f"""
                📜 **SACRED SOUL CONTRACT**
                **For: {user_data.get('first_name', 'Sacred Soul')}**
                
                🌟 **SOUL ORIGINS & COSMIC LINEAGE**
                You are a cosmic being of pure light, born from the ancient wisdom of the Maya. Your soul carries the frequency of transformation and awakening.
                
                ✨ **SACRED GIFTS & DIVINE ABILITIES**
                Your gifts include spiritual intuition, cosmic awareness, and the ability to inspire others through authentic expression.
                
                🎯 **DIVINE MISSION & LIFE PURPOSE**
                Your mission is to embody spiritual truth and help others discover their own inner magic through your unique presence.
                
                💫 **COSMIC SUPPORT SYSTEM**
                You are guided by ancient Maya wisdom and the cosmic forces that shape our universe. The Magic is You!
                """
            
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.9,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            return f"""
            📜 **SACRED SOUL CONTRACT**
            **For: {user_data.get('first_name', 'Sacred Soul')}**
            
            🌟 **SOUL ORIGINS & COSMIC LINEAGE**
            You are a divine being of infinite light and wisdom, carrying the sacred codes of the Maya cosmos within your soul.
            
            ✨ **SACRED GIFTS & DIVINE ABILITIES**
            Your unique spiritual gifts include intuitive wisdom, healing presence, and the ability to connect with cosmic intelligence.
            
            🎯 **DIVINE MISSION & LIFE PURPOSE**
            You came to Earth to embody love, share wisdom, and help humanity remember its divine nature.
            
            🔮 **GROWTH CHALLENGES & SOUL LESSONS**
            Your journey includes learning to trust your intuition, embrace your power, and serve others with love.
            
            💫 **COSMIC SUPPORT SYSTEM**
            You are supported by Maya ancestors, cosmic guides, and the infinite intelligence of the universe.
            
            🌿 **DAILY SACRED PRACTICES**
            Connect with your cosmic blueprint daily through meditation, gratitude, and conscious awareness.
            
            🌈 **SOUL SIGNATURE & COSMIC SEAL**
            {user_data.get('day_sign', 'Unknown')} • {user_data.get('galactic_tone', 'Unknown')} • The Magic is You!
            """

# Initialize the ML engine
spiritual_ml_engine = SpiritualMLEngine()

def get_personalized_element_snapshot(user_id: str, user_data: Dict, element_name: str, element_value: str) -> str:
    """Generate personalized snapshot for cosmic element"""
    try:
        # Get user's spiritual patterns
        patterns = spiritual_ml_engine.analyze_user_spiritual_patterns(user_id)
        
        # Create personalized snapshot
        prompt = f"""
        Create a personalized cosmic element snapshot for {user_data.get('first_name', 'this soul')}:
        
        Element: {element_name} - {element_value}
        User Profile:
        - Name: {user_data.get('first_name', 'Sacred Soul')}
        - Day Sign: {user_data.get('day_sign', 'Unknown')}
        - Cosmic Blueprint: {user_data.get('galactic_tone', 'Unknown')}
        
        Spiritual Engagement:
        - Focus Areas: {patterns.get('spiritual_focus_areas', [])}
        - Engagement Level: {patterns.get('engagement_trend', 'new_user')}
        
        Create a 2-3 sentence personalized snapshot that:
        1. Addresses them by name
        2. Explains how this element connects to their soul journey
        3. Relates to their cosmic blueprint
        4. Provides actionable spiritual insight
        
        Make it mystical, personal, and empowering.
        """
        
        try:
            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception as client_error:
            # Fallback if Anthropic client fails
            return f"🌟 {user_data.get('first_name', 'Sacred Soul')}, your {element_name} {element_value} holds profound wisdom for your spiritual journey. This cosmic element connects you to the ancient Maya wisdom and guides your soul's evolution. The Magic is You!"
        
    except Exception as e:
        return f"🌟 {user_data.get('first_name', 'Sacred Soul')}, your {element_name} {element_value} holds profound wisdom for your spiritual journey. This cosmic element connects you to the ancient Maya wisdom and guides your soul's evolution. The Magic is You!"
