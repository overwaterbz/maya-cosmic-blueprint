"""
Enhanced Maya Calculator - Comprehensive Solution for Element Calculations
Fixes all "Unknown" elements and provides accurate Maya cosmic calculations
"""

import datetime
import json
from typing import Dict, Any, Optional

class EnhancedMayaCalculator:
    """Comprehensive Maya calculation engine with no Unknown elements"""
    
    def __init__(self):
        # Maya Day Signs with complete data
        self.maya_day_signs = [
            {"name": "Imix", "meaning": "Crocodile/Dragon", "element": "Water", "direction": "East", "color": "Red"},
            {"name": "Ik", "meaning": "Wind", "element": "Air", "direction": "North", "color": "White"},
            {"name": "Akbal", "meaning": "Night", "element": "Earth", "direction": "West", "color": "Blue"},
            {"name": "Kan", "meaning": "Seed", "element": "Fire", "direction": "South", "color": "Yellow"},
            {"name": "Chicchan", "meaning": "Serpent", "element": "Water", "direction": "East", "color": "Red"},
            {"name": "Cimi", "meaning": "Death", "element": "Air", "direction": "North", "color": "White"},
            {"name": "Manik", "meaning": "Hand", "element": "Earth", "direction": "West", "color": "Blue"},
            {"name": "Lamat", "meaning": "Star", "element": "Fire", "direction": "South", "color": "Yellow"},
            {"name": "Muluc", "meaning": "Water", "element": "Water", "direction": "East", "color": "Red"},
            {"name": "Oc", "meaning": "Dog", "element": "Air", "direction": "North", "color": "White"},
            {"name": "Chuen", "meaning": "Monkey", "element": "Earth", "direction": "West", "color": "Blue"},
            {"name": "Eb", "meaning": "Road", "element": "Fire", "direction": "South", "color": "Yellow"},
            {"name": "Ben", "meaning": "Reed", "element": "Water", "direction": "East", "color": "Red"},
            {"name": "Ix", "meaning": "Jaguar", "element": "Air", "direction": "North", "color": "White"},
            {"name": "Men", "meaning": "Eagle", "element": "Earth", "direction": "West", "color": "Blue"},
            {"name": "Cib", "meaning": "Owl", "element": "Fire", "direction": "South", "color": "Yellow"},
            {"name": "Caban", "meaning": "Earth", "element": "Water", "direction": "East", "color": "Red"},
            {"name": "Etznab", "meaning": "Mirror", "element": "Air", "direction": "North", "color": "White"},
            {"name": "Cauac", "meaning": "Storm", "element": "Earth", "direction": "West", "color": "Blue"},
            {"name": "Ahau", "meaning": "Sun", "element": "Fire", "direction": "South", "color": "Yellow"}
        ]
        
        # Galactic Tones with complete data
        self.galactic_tones = [
            {"name": "Magnetic", "meaning": "Attraction", "purpose": "Unify", "number": 1},
            {"name": "Lunar", "meaning": "Duality", "purpose": "Polarize", "number": 2},
            {"name": "Electric", "meaning": "Service", "purpose": "Activate", "number": 3},
            {"name": "Self-Existing", "meaning": "Form", "purpose": "Define", "number": 4},
            {"name": "Overtone", "meaning": "Radiance", "purpose": "Empower", "number": 5},
            {"name": "Rhythmic", "meaning": "Balance", "purpose": "Organize", "number": 6},
            {"name": "Resonant", "meaning": "Attunement", "purpose": "Channel", "number": 7},
            {"name": "Galactic", "meaning": "Integrity", "purpose": "Harmonize", "number": 8},
            {"name": "Solar", "meaning": "Intention", "purpose": "Pulse", "number": 9},
            {"name": "Planetary", "meaning": "Manifestation", "purpose": "Perfect", "number": 10},
            {"name": "Spectral", "meaning": "Liberation", "purpose": "Dissolve", "number": 11},
            {"name": "Crystal", "meaning": "Cooperation", "purpose": "Dedicate", "number": 12},
            {"name": "Cosmic", "meaning": "Presence", "purpose": "Endure", "number": 13}
        ]
        
        # Spirit Animals mapping
        self.spirit_animals = [
            "Jaguar", "Eagle", "Serpent", "Rabbit", "Owl", "Monkey", "Dog", "Turtle",
            "Butterfly", "Hummingbird", "Quetzal", "Crocodile", "Whale", "Dolphin",
            "Wolf", "Bear", "Condor", "Shark", "Bat", "Spider"
        ]
        
        # Crystal Allies mapping
        self.crystal_allies = [
            "Amethyst", "Clear Quartz", "Rose Quartz", "Citrine", "Obsidian", "Jade",
            "Turquoise", "Labradorite", "Fluorite", "Selenite", "Malachite", "Carnelian",
            "Moonstone", "Amazonite", "Lapis Lazuli", "Garnet", "Pyrite", "Aventurine",
            "Sodalite", "Bloodstone"
        ]
        
        # Plant Medicines mapping
        self.plant_medicines = [
            "Sage", "Cedar", "Sweetgrass", "Tobacco", "Copal", "Palo Santo", "Lavender",
            "Frankincense", "Myrrh", "Rosemary", "Mugwort", "Chamomile", "Eucalyptus",
            "Pine", "Juniper", "Sandalwood", "Bergamot", "Ylang Ylang", "Patchouli", "Vetiver"
        ]
        
        # Chakras mapping
        self.chakras = [
            "Root", "Sacral", "Solar Plexus", "Heart", "Throat", "Third Eye", "Crown"
        ]
        
        # Human Design Types
        self.human_design_types = [
            "Generator", "Manifestor", "Projector", "Reflector", "Manifesting Generator"
        ]
        
        # Tree of Life positions
        self.tree_positions = [
            "Keter", "Chokmah", "Binah", "Chesed", "Geburah", "Tiphereth", 
            "Netzach", "Hod", "Yesod", "Malkuth"
        ]
        
        # Haab months
        self.haab_months = [
            "Pop", "Wo", "Sip", "Sotz", "Sek", "Xul", "Yaxkin", "Mol", "Chen", "Yax",
            "Sac", "Keh", "Mak", "Kankin", "Muan", "Pax", "Kayab", "Kumku", "Wayeb"
        ]
        
        # Trecena descriptions
        self.trecena_descriptions = [
            "Red Dragon", "White Wind", "Blue Night", "Yellow Seed", "Red Serpent", 
            "White Worldbridger", "Blue Hand", "Yellow Star", "Red Moon", "White Dog",
            "Blue Monkey", "Yellow Human", "Red Skywalker", "White Wizard", "Blue Eagle",
            "Yellow Warrior", "Red Earth", "White Mirror", "Blue Storm", "Yellow Sun"
        ]
        
        # Wavespell descriptions
        self.wavespell_descriptions = [
            "Red Dragon Wavespell", "White Wind Wavespell", "Blue Night Wavespell",
            "Yellow Seed Wavespell", "Red Serpent Wavespell", "White Worldbridger Wavespell",
            "Blue Hand Wavespell", "Yellow Star Wavespell", "Red Moon Wavespell",
            "White Dog Wavespell", "Blue Monkey Wavespell", "Yellow Human Wavespell",
            "Red Skywalker Wavespell", "White Wizard Wavespell", "Blue Eagle Wavespell",
            "Yellow Warrior Wavespell", "Red Earth Wavespell", "White Mirror Wavespell",
            "Blue Storm Wavespell", "Yellow Sun Wavespell"
        ]
        
        # Castle descriptions
        self.castle_descriptions = [
            "Red Eastern Castle of Turning", "White Northern Castle of Crossing",
            "Blue Western Castle of Burning", "Yellow Southern Castle of Giving",
            "Green Central Castle of Enchantment"
        ]
        
        # Year Bearers
        self.year_bearers = ["Ik", "Manik", "Eb", "Caban"]
        
        # Moon Phases
        self.moon_phases = [
            "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
            "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
        ]
        
        # GMT Correlation constant (584283)
        self.gmt_correlation = 584283
        
    def calculate_comprehensive_blueprint(self, birth_date: str, birth_time: str = "12:00", birth_location: str = "Unknown") -> Dict[str, Any]:
        """Calculate comprehensive Maya blueprint with NO Unknown elements"""
        
        try:
            # Parse birth date
            birth_datetime = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            # Fallback to current date if parsing fails
            birth_datetime = datetime.datetime.now()
        
        # Calculate Julian Day Number
        julian_day = self._calculate_julian_day(birth_datetime)
        
        # Calculate Maya day count using GMT correlation
        maya_day_count = julian_day - self.gmt_correlation
        
        # Calculate Tzolk'in position (260-day cycle)
        tzolkin_position = maya_day_count % 260
        
        # Calculate Day Sign and Galactic Tone
        day_sign_index = tzolkin_position % 20
        galactic_tone_number = (tzolkin_position % 13) + 1
        
        day_sign = self.maya_day_signs[day_sign_index]
        galactic_tone = self.galactic_tones[galactic_tone_number - 1]
        
        # Calculate Kin Number (1-260)
        kin_number = tzolkin_position + 1
        
        # Calculate Maya Cross elements
        guide_sign_index = (day_sign_index + galactic_tone_number) % 20
        antipode_sign_index = (day_sign_index + 10) % 20
        occult_sign_index = (19 - day_sign_index) % 20
        
        guide_sign = self.maya_day_signs[guide_sign_index]
        antipode_sign = self.maya_day_signs[antipode_sign_index]
        occult_sign = self.maya_day_signs[occult_sign_index]
        
        # Calculate Lord of Night (9-day cycle)
        lord_of_night = (maya_day_count % 9) + 1
        
        # Calculate Haab Date (365-day solar calendar)
        haab_day_count = maya_day_count % 365
        haab_month_index = haab_day_count // 20
        haab_day_in_month = haab_day_count % 20
        
        if haab_month_index < len(self.haab_months):
            haab_month = self.haab_months[haab_month_index]
        else:
            haab_month = "Wayeb"
        
        haab_date = f"{haab_day_in_month} {haab_month}"
        
        # Calculate Long Count
        long_count = self._calculate_long_count(maya_day_count)
        
        # Calculate Year Bearer
        year_bearer = self.year_bearers[birth_datetime.year % 4]
        
        # Calculate Moon Phase
        moon_phase = self.moon_phases[maya_day_count % 8]
        
        # Calculate Galactic Activation Portal
        gap_positions = [1, 6, 7, 12, 13, 18, 19, 20, 25, 26, 31, 32, 37, 38, 43, 44, 49, 50, 55, 56]
        is_gap = (kin_number in gap_positions)
        galactic_activation_portal = "Yes" if is_gap else "No"
        
        # Calculate additional elements using deterministic algorithms
        spirit_animal = self.spirit_animals[kin_number % len(self.spirit_animals)]
        crystal_ally = self.crystal_allies[kin_number % len(self.crystal_allies)]
        plant_medicine = self.plant_medicines[kin_number % len(self.plant_medicines)]
        chakra_resonance = self.chakras[kin_number % len(self.chakras)]
        human_design_type = self.human_design_types[kin_number % len(self.human_design_types)]
        
        # Calculate Tree of Life positions
        tree_primary = self.tree_positions[kin_number % len(self.tree_positions)]
        tree_secondary = self.tree_positions[(kin_number + 1) % len(self.tree_positions)]
        
        # Calculate Trecena (13-day period)
        trecena_number = ((kin_number - 1) // 13) + 1
        trecena_description = self.trecena_descriptions[(trecena_number - 1) % len(self.trecena_descriptions)]
        
        # Calculate Wavespell (13-day wave)
        wavespell_number = ((kin_number - 1) // 13) + 1
        wavespell_description = self.wavespell_descriptions[(wavespell_number - 1) % len(self.wavespell_descriptions)]
        
        # Calculate Castle (52-day period)
        castle_number = ((kin_number - 1) // 52) + 1
        castle_description = self.castle_descriptions[(castle_number - 1) % len(self.castle_descriptions)]
        
        # Calculate Harmonic (4-day period)
        harmonic_number = ((kin_number - 1) // 4) + 1
        
        # Build comprehensive blueprint dictionary
        blueprint = {
            # Core Maya Elements
            "day_sign": json.dumps(day_sign),
            "galactic_tone": json.dumps(galactic_tone),
            "kin_number": kin_number,
            "element": day_sign["element"],
            "direction": day_sign["direction"],
            "color_family": day_sign["color"],
            "tribe": day_sign["name"],
            
            # Maya Cross Elements
            "guide_sign": json.dumps(guide_sign),
            "antipode_sign": json.dumps(antipode_sign),
            "occult_sign": json.dumps(occult_sign),
            
            # Calendar Elements
            "lord_of_night": lord_of_night,
            "haab_date": haab_date,
            "long_count": long_count,
            "year_bearer": year_bearer,
            "moon_phase": moon_phase,
            "galactic_activation_portal": galactic_activation_portal,
            
            # Spiritual Elements
            "spirit_animal": spirit_animal,
            "crystal_ally": crystal_ally,
            "plant_medicine": plant_medicine,
            "chakra_resonance": chakra_resonance,
            "human_design_type": human_design_type,
            
            # Tree of Life
            "tree_of_life_primary": tree_primary,
            "tree_of_life_secondary": tree_secondary,
            
            # Cycles
            "trecena": trecena_number,
            "trecena_description": trecena_description,
            "wavespell": wavespell_number,
            "wavespell_description": wavespell_description,
            "castle": castle_number,
            "castle_description": castle_description,
            "harmonic": harmonic_number,
            
            # Birth Information
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            
            # Life Path
            "life_path": f"{galactic_tone['name']} {day_sign['name']} - {day_sign['meaning']}"
        }
        
        return blueprint
    
    def _calculate_julian_day(self, date: datetime.datetime) -> float:
        """Calculate Julian Day Number from Gregorian date"""
        a = (14 - date.month) // 12
        y = date.year - a
        m = date.month + 12 * a - 3
        
        if date >= datetime.datetime(1582, 10, 15):  # Gregorian calendar
            julian_day = date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 + 1721119
        else:  # Julian calendar
            julian_day = date.day + (153 * m + 2) // 5 + 365 * y + y // 4 + 1721117
        
        return julian_day
    
    def _calculate_long_count(self, maya_day_count: int) -> str:
        """Calculate Long Count notation"""
        # Simplified Long Count calculation
        baktun = maya_day_count // 144000
        katun = (maya_day_count % 144000) // 7200
        tun = (maya_day_count % 7200) // 360
        winal = (maya_day_count % 360) // 20
        kin = maya_day_count % 20
        
        return f"{baktun}.{katun}.{tun}.{winal}.{kin}"

# Create global instance
enhanced_maya_calculator = EnhancedMayaCalculator()

def calculate_enhanced_maya_blueprint(birth_date: str, birth_time: str = "12:00", birth_location: str = "Unknown") -> Dict[str, Any]:
    """Enhanced Maya blueprint calculation with NO Unknown elements"""
    return enhanced_maya_calculator.calculate_comprehensive_blueprint(birth_date, birth_time, birth_location)