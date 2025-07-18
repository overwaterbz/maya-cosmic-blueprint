#!/usr/bin/env python3
"""
The Magic is You - Complete Authentication System
User registration, login, and Maya blueprint storage
"""

from fastapi import FastAPI, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
# Phase 4 Code Cleanup - Removed unused imports (SAFE - sqlite3 not used)
import uvicorn
import os
import bcrypt
import jwt
from typing import Optional
import json
import anthropic
import psycopg2
import secrets
import string
import asyncio
from datetime import datetime, timedelta
from ai_spiritual_engine import (
    spiritual_ml_engine, 
    get_personalized_element_snapshot
)
from ai_personalization_engine import ai_personalization_engine, ContentType, PersonalizationDepth
from dynamic_spiritual_guidance import dynamic_guidance_system, GuidanceUrgency, SpiritualTheme
from stripe_integration import MayaStripeService
from cosmic_cache_system import cosmic_cache
from personalization_templates import template_engine, generate_dashboard_content
from smart_loading_system import smart_loader

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "the-magic-is-you-secret-key-2024")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 1 week

app = FastAPI()
security = HTTPBearer()

# Initialize Maya Stripe service
maya_stripe = MayaStripeService()

# Initialize Phase 2 optimization systems
smart_loader.start()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
# Phase 4 Code Cleanup - Enhanced function documentation (SAFE - Documentation only)
def init_database():
    """
    Initialize PostgreSQL database with all required tables.
    
    Creates the following tables if they don't exist:
    - users: User authentication and profile data
    - maya_profiles: User Maya cosmic blueprint data
    - password_reset_tokens: Password reset functionality
    - user_preferences: User engagement preferences
    - user_interactions: User interaction tracking
    - subscriptions: User subscription data
    - spiritual_sessions: Spiritual tool usage tracking
    
    Returns:
        None
        
    Side Effects:
        - Creates database tables
        - Prints initialization status
        - Handles connection errors gracefully
    """
    import psycopg2
    
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                is_onboarding_complete BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create maya_profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maya_profiles (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                birth_date TEXT NOT NULL,
                birth_time TEXT,
                birth_location TEXT,
                day_sign TEXT,
                galactic_tone TEXT,
                kin_number INTEGER,
                element TEXT,
                direction TEXT,
                life_path INTEGER,
                cosmic_profile TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add missing columns if they don't exist
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name TEXT
        """)
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name TEXT
        """)
        cursor.execute("""
            ALTER TABLE users ADD COLUMN IF NOT EXISTS is_onboarding_complete BOOLEAN DEFAULT FALSE
        """)
        
        # Add missing columns to maya_profiles table
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS color_family TEXT
        """)
        
        # Create password_reset_tokens table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                token TEXT NOT NULL UNIQUE,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS tribe TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS guide_sign TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS antipode_sign TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS occult_sign TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS lord_of_night INTEGER
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS haab_date TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS long_count TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS year_bearer TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS moon_phase TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS galactic_activation_portal TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS spirit_animal TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS crystal_ally TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS plant_medicine TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS chakra_resonance TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS human_design_type TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS tree_of_life_primary TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS tree_of_life_secondary TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS trecena TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS trecena_description TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS wavespell TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS wavespell_description TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS castle TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS castle_description TEXT
        """)
        cursor.execute("""
            ALTER TABLE maya_profiles ADD COLUMN IF NOT EXISTS harmonic TEXT
        """)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Initialize database on startup
init_database()

# Initialize Anthropic AI client with error handling
try:
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
except Exception as e:
    print(f"Warning: Failed to initialize Anthropic client: {e}")
    client = None

# Authentication utilities
# Phase 4 Code Cleanup - Enhanced authentication function documentation (SAFE - Documentation only)
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt for secure storage.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password string
        
    Security:
        - Uses bcrypt with salt for secure hashing
        - Suitable for database storage
        - Prevents rainbow table attacks
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against bcrypt hash.
    
    Args:
        password (str): Plain text password to verify
        hashed (str): Bcrypt hashed password from database
        
    Returns:
        bool: True if password matches hash, False otherwise
        
    Security:
        - Constant-time comparison prevents timing attacks
        - Works with bcrypt salt automatically
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset.
    
    Returns:
        str: 32-character random token using letters and digits
        
    Security:
        - Uses cryptographically secure random generation
        - 32 characters provide adequate entropy
        - Suitable for password reset functionality
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset email to user.
    
    Args:
        email (str): User's email address
        token (str): Password reset token
        
    Returns:
        bool: True if email sent successfully, False otherwise
        
    Note:
        - Current implementation logs token for development
        - Production version would use email service (SendGrid, Mailgun, etc.)
        - Reset URL includes token for verification
    """
    # In a real implementation, this would use an email service like SendGrid, Mailgun, etc.
    # For now, we'll just log the token (in production, this would be sent via email)
    print(f"Password reset token for {email}: {token}")
    print(f"Reset URL: https://magic-mindset-rick166.replit.app/reset-password?token={token}")
    return True

def create_jwt_token(user_id: str) -> str:
    """
    Create JWT token for user authentication.
    
    Args:
        user_id (str): Unique user identifier
        
    Returns:
        str: JWT token string for authentication
        
    Security:
        - Uses HS256 algorithm for signing
        - Includes expiration time (1 week)
        - Signed with secret key
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> Optional[str]:
    """
    Verify JWT token and extract user ID.
    
    Args:
        token (str): JWT token to verify
        
    Returns:
        Optional[str]: User ID if token is valid, None otherwise
        
    Security:
        - Verifies signature and expiration
        - Handles expired and invalid tokens gracefully
        - Returns None for any verification failure
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Phase 3 Security Enhancement - Enhanced JWT validation (SAFE - New function only)
# Phase 4 Code Cleanup - Enhanced documentation (SAFE - Documentation only)
def validate_jwt_token_enhanced(token: str) -> Optional[dict]:
    """
    Enhanced JWT validation with additional security checks.
    
    Args:
        token (str): JWT token to validate
        
    Returns:
        Optional[dict]: Token payload if valid, None otherwise
        
    Security Features:
        - Validates user_id presence in payload
        - Checks explicit expiration time
        - Validates token age against maximum allowed
        - Handles all JWT-related exceptions gracefully
        
    Enhanced Checks:
        - Explicit expiration verification
        - Token age limits beyond standard expiration
        - Comprehensive exception handling
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Additional validation checks
        if not payload.get("user_id"):
            return None
            
        # Check expiration explicitly
        if payload.get('exp', 0) < datetime.utcnow().timestamp():
            return None
            
        # Check token age (additional security)
        issued_at = payload.get('iat', 0)
        if issued_at and (datetime.utcnow().timestamp() - issued_at) > (JWT_EXPIRATION_HOURS * 3600):
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None

# Phase 3 Security Enhancement - Input validation helpers (SAFE - New functions only)
# Phase 4 Code Cleanup - Enhanced documentation (SAFE - Documentation only)
def validate_email_input(email: str) -> bool:
    """
    Validate email input with comprehensive security checks.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid and secure, False otherwise
        
    Security Features:
        - Length validation (max 254 characters)
        - RFC-compliant email regex pattern
        - Injection pattern detection
        - XSS prevention checks
        
    Dangerous Patterns Detected:
        - HTML tags and brackets
        - SQL injection patterns
        - Script injection attempts
        - Comment sequences
    """
    import re
    
    if not email or len(email) > 254:
        return False
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False
    
    # Check for common injection patterns
    dangerous_patterns = ['<', '>', '"', "'", ';', '--', '/*', '*/', 'script:', 'javascript:']
    for pattern in dangerous_patterns:
        if pattern in email.lower():
            return False
    
    return True

def validate_name_input(name: str) -> bool:
    """Validate name input with security checks"""
    if not name or len(name) < 1 or len(name) > 100:
        return False
    
    # Check for dangerous patterns
    dangerous_patterns = ['<', '>', '"', "'", ';', '--', '/*', '*/', 'script:', 'javascript:']
    for pattern in dangerous_patterns:
        if pattern in name.lower():
            return False
    
    return True

def validate_password_strength(password: str) -> bool:
    """Validate password strength"""
    if not password or len(password) < 8:
        return False
    
    # Check for basic strength requirements
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit

# Phase 3 Security Enhancement - Secure headers helper (SAFE - New function only)
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; img-src 'self' data: https:; font-src 'self' https: data:;"
    return response

# Phase 3 Security Enhancement - Rate limiting helper (SAFE - New function only)
import time
from collections import defaultdict

rate_limit_store = defaultdict(list)

def check_rate_limit(ip_address: str, max_requests: int = 100, window_seconds: int = 3600) -> bool:
    """Check if IP address is within rate limits"""
    current_time = time.time()
    
    # Clean old entries
    rate_limit_store[ip_address] = [
        timestamp for timestamp in rate_limit_store[ip_address]
        if current_time - timestamp < window_seconds
    ]
    
    # Check if under limit
    if len(rate_limit_store[ip_address]) >= max_requests:
        return False
    
    # Add current request
    rate_limit_store[ip_address].append(current_time)
    return True

# Phase 3 Security Enhancement - Secure user data sanitization (SAFE - New function only)
def sanitize_user_input(data: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks"""
    if not data:
        return ""
    
    # Remove potentially dangerous HTML tags and scripts
    import re
    
    # Remove script tags
    data = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags (basic sanitization)
    data = re.sub(r'<[^>]+>', '', data)
    
    # Escape special characters
    data = data.replace('&', '&amp;')
    data = data.replace('<', '&lt;')
    data = data.replace('>', '&gt;')
    data = data.replace('"', '&quot;')
    data = data.replace("'", '&#x27;')
    
    return data.strip()

# Phase 3 Security Enhancement - Secure database query helper (SAFE - New function only)
def execute_secure_query(query: str, params: tuple = None):
    """Execute database query with security checks"""
    import psycopg2
    
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        
        return result
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    import psycopg2
    
    token = credentials.credentials
    user_id = verify_jwt_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.email, u.first_name, u.last_name, 
                   mp.birth_date, mp.birth_time, mp.birth_location, mp.cosmic_profile,
                   mp.day_sign, mp.galactic_tone, mp.kin_number, mp.element, mp.direction,
                   mp.life_path, mp.color_family, mp.tribe, mp.guide_sign, mp.antipode_sign,
                   mp.occult_sign, mp.lord_of_night, mp.haab_date, mp.long_count,
                   mp.year_bearer, mp.moon_phase, mp.galactic_activation_portal,
                   mp.spirit_animal, mp.crystal_ally, mp.plant_medicine, mp.chakra_resonance,
                   mp.human_design_type, mp.tree_of_life_primary, mp.tree_of_life_secondary,
                   mp.trecena, mp.trecena_description, mp.wavespell, mp.wavespell_description,
                   mp.castle, mp.castle_description, mp.harmonic
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Handle cosmic_profile safely
        cosmic_profile = None
        if user_data[7]:
            try:
                # If it's already a dict, use it directly
                if isinstance(user_data[7], dict):
                    cosmic_profile = user_data[7]
                # If it's a string, parse it
                elif isinstance(user_data[7], str):
                    cosmic_profile = json.loads(user_data[7])
                else:
                    cosmic_profile = user_data[7]
            except (json.JSONDecodeError, TypeError):
                cosmic_profile = None
        
        # Helper function to safely parse JSON fields
        def safe_json_parse(field_value, default=None):
            if not field_value:
                return default or {"name": "Unknown", "meaning": "Unknown"}
            try:
                # If it's already a dict, return it
                if isinstance(field_value, dict):
                    return field_value
                # If it's a string, parse it
                elif isinstance(field_value, str):
                    # Handle different JSON string formats
                    if field_value.startswith('"""') and field_value.endswith('"""'):
                        # Handle triple-quoted strings
                        cleaned_value = field_value[3:-3]
                        cleaned_value = cleaned_value.replace('\\"', '"')
                    elif field_value.startswith('"') and field_value.endswith('"'):
                        # Handle double-quoted strings  
                        cleaned_value = field_value[1:-1]
                        cleaned_value = cleaned_value.replace('\\"', '"')
                    else:
                        cleaned_value = field_value
                    
                    return json.loads(cleaned_value)
                else:
                    return field_value
            except (json.JSONDecodeError, TypeError):
                return default or {"name": "Unknown", "meaning": "Unknown"}

        # Build comprehensive maya_profile with all elements
        comprehensive_maya_profile = {
            "birth_date": str(user_data[4]) if user_data[4] else None,
            "birth_time": str(user_data[5]) if user_data[5] else None,
            "birth_location": user_data[6],
            "day_sign": safe_json_parse(user_data[8]),
            "galactic_tone": safe_json_parse(user_data[9]),
            "kin_number": user_data[10] if user_data[10] else 0,
            "element": user_data[11] if user_data[11] else "Unknown",
            "direction": user_data[12] if user_data[12] else "Unknown",
            "life_path": user_data[13] if user_data[13] else "Unknown",
            "color_family": user_data[14] if user_data[14] else "Unknown",
            "tribe": user_data[15] if user_data[15] else "Unknown",
            "guide_sign": safe_json_parse(user_data[16]) if user_data[16] and user_data[16].strip() != "Unknown" else {"name": "Unknown", "meaning": "Unknown"},
            "antipode_sign": safe_json_parse(user_data[17]) if user_data[17] and user_data[17].strip() != "Unknown" else {"name": "Unknown", "meaning": "Unknown"},
            "occult_sign": safe_json_parse(user_data[18]) if user_data[18] and user_data[18].strip() != "Unknown" else {"name": "Unknown", "meaning": "Unknown"},
            "lord_of_night": user_data[19] if user_data[19] else "Unknown",
            "haab_date": user_data[20] if user_data[20] else "Unknown",
            "long_count": user_data[21] if user_data[21] else "Unknown",
            "year_bearer": user_data[22] if user_data[22] else "Unknown",
            "moon_phase": user_data[23] if user_data[23] else "Unknown",
            "galactic_activation_portal": user_data[24] if user_data[24] else "Unknown",
            "spirit_animal": user_data[25] if user_data[25] else "Unknown",
            "crystal_ally": user_data[26] if user_data[26] else "Unknown",
            "plant_medicine": user_data[27] if user_data[27] else "Unknown",
            "chakra_resonance": user_data[28] if user_data[28] else "Unknown",
            "human_design_type": user_data[29] if user_data[29] else "Unknown",
            "tree_of_life_primary": user_data[30] if user_data[30] else "Unknown",
            "tree_of_life_secondary": user_data[31] if user_data[31] else "Unknown",
            "trecena": user_data[32] if user_data[32] else "Unknown",
            "trecena_description": user_data[33] if user_data[33] else "Unknown",
            "wavespell": user_data[34] if user_data[34] else "Unknown",
            "wavespell_description": user_data[35] if user_data[35] else "Unknown",
            "castle": user_data[36] if user_data[36] else "Unknown",
            "castle_description": user_data[37] if user_data[37] else "Unknown",
            "harmonic": user_data[38] if user_data[38] else "Unknown"
        }

        return {
            "id": user_data[0],
            "email": user_data[1],
            "first_name": user_data[2],
            "last_name": user_data[3], 
            "full_name": f"{user_data[2] or ''} {user_data[3] or ''}".strip(),
            "birth_date": str(user_data[4]) if user_data[4] else None,
            "birth_time": str(user_data[5]) if user_data[5] else None,
            "birth_location": user_data[6],
            "maya_profile": comprehensive_maya_profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def generate_soul_contract_content(day_sign, galactic_tone, element, direction):
    """Generate formatted soul contract content"""
    soul_contract_html = f"""
    <div style="background: linear-gradient(135deg, #8B4513, #DAA520); padding: 30px; border-radius: 20px; color: white; font-family: 'Cinzel', serif; text-align: center; margin: 20px 0;">
        <h2 style="font-size: 2rem; margin-bottom: 10px; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            🌙 Your Sacred Cosmic Blueprint 🌙
        </h2>
        <p style="font-size: 1.1rem; opacity: 0.9; margin-bottom: 0;">
            Blessed by Ancient Maya Wisdom
        </p>
    </div>
    
    <div style="background: rgba(218, 165, 32, 0.1); padding: 25px; border-radius: 15px; border-left: 4px solid #DAA520; font-family: 'Inter', sans-serif; line-height: 1.8; color: #2D1810;">
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">🌟 SOUL ORIGINS</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">You emerged from the sacred lineage of the {day_sign}, blessed child of the {element} element. Your soul carries the ancient wisdom of the {direction} direction, where the {galactic_tone} energy flows through your being like a river of cosmic light.</p>
        
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">🎁 SACRED GIFTS</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">Your {day_sign} essence grants you the divine ability to channel {element} wisdom into practical guidance. The {galactic_tone} vibration empowers you to manifest your highest vision and inspire others through your authentic expression of cosmic truth.</p>
        
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">🌱 GROWTH CHALLENGES</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">Your soul's journey involves learning to balance the powerful {element} energy within you while staying grounded in earthly wisdom. Transform any challenges into opportunities for deeper spiritual understanding and service to others.</p>
        
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">✨ DESTINY MISSION</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">You have incarnated to embody the sacred teachings of the {day_sign} and share the transformative power of {element} energy with the world. Your path is one of spiritual leadership, healing, and awakening others to their own cosmic magic.</p>
        
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">🧘 DAILY PRACTICES</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">Connect with your {day_sign} energy through meditation and prayer. Honor the {element} within you through conscious breathing and visualization. Face the {direction} direction each morning to align with your cosmic signature and embrace your {galactic_tone} power.</p>
        
        <h3 style="color: #8B4513; margin-top: 25px; margin-bottom: 15px; font-size: 1.4rem;">🔮 COSMIC SIGNATURE WISDOM</h3>
        <p style="margin-bottom: 20px; font-size: 1.1rem;">Your {galactic_tone} {day_sign} combination is a sacred gift from the cosmos. You are a bridge between the ancient wisdom of the Maya and the modern world. Trust in your divine purpose and remember always: The Magic is You!</p>
    </div>
    
    <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(139, 69, 19, 0.1); border-radius: 10px;">
        <p style="color: #8B4513; font-style: italic; margin: 0; font-size: 1rem;">
            Sacred blueprint sealed with Maya blessing • Your cosmic journey begins now
        </p>
    </div>
    """
    return soul_contract_html

def calculate_maya_blueprint(birth_date, birth_time="12:00", birth_location="Unknown"):
    """Calculate comprehensive Maya cosmic blueprint with NO Unknown elements"""
    from enhanced_maya_calculator import calculate_enhanced_maya_blueprint
    
    # Use enhanced calculator for comprehensive results
    return calculate_enhanced_maya_blueprint(birth_date, birth_time, birth_location)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Maya Cosmic Blueprint Platform - Optimized Homepage for Maximum Conversion"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Magic is You - Discover Your Sacred Maya Cosmic Blueprint</title>
    <meta name="description" content="Unlock your personalized Maya cosmic blueprint with 35+ spiritual elements, AI-powered explanations, and sacred wisdom. Create your soul contract and discover your spiritual destiny today.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="/static/js/cosmic-particles.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        .cosmic-background {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            position: relative;
        }

        /* Cosmic Particles Background */
        .cosmic-particles-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.15;
            pointer-events: none;
        }

        .cosmic-particles-interactive {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            opacity: 0.3;
            pointer-events: auto;
        }
        
        .element-bubble {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .element-bubble:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .form-container {
            background: white;
            border: 2px solid #E5E7EB;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s ease;
        }
        
        .form-container:hover {
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .form-title {
            color: #8B5CF6;
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 8px;
        }
        
        .form-title.register {
            color: #D97706;
        }
        
        .form-subtitle {
            color: #6B7280;
            text-align: center;
            margin-bottom: 25px;
            font-size: 1rem;
        }
        
        .form-label {
            color: #374151;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 8px;
            display: block;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
            color: #374151;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #8B5CF6;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        }
        
        .form-input.register:focus {
            border-color: #D97706;
            box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.1);
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .element-bubble:nth-child(odd) {
            animation-delay: -2s;
        }
        
        .element-bubble:nth-child(even) {
            animation-delay: -4s;
        }
        
        .cosmic-form {
            background: white;
            border: 2px solid #E5E7EB;
        }
        
        .cosmic-button {
            background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }
        
        .cosmic-button.register {
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4);
        }
        
        .cosmic-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
        }
        
        .maya-symbol {
            font-family: 'Playfair Display', serif;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
        }
        
        .pulse-glow {
            animation: pulse-glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes pulse-glow {
            0% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.5); }
            100% { text-shadow: 0 0 30px rgba(255, 215, 0, 0.8); }
        }
        
        .category-header {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.3) 0%, 
                rgba(255, 255, 255, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(15px);
        }
        
        .element-icon {
            filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
        }
        
        .registration-pulse {
            animation: registration-pulse 4s ease-in-out infinite;
        }
        
        @keyframes registration-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        .maya-temple {
            position: fixed;
            bottom: 0;
        }
        
        /* Mobile-First Optimizations */
        @media (max-width: 768px) {
            .form-container {
                padding: 1rem;
                margin: 0.5rem;
                border-radius: 1rem;
            }
            
            .form-input {
                min-height: 44px;
                font-size: 16px; /* Prevents iOS zoom */
                padding: 14px 16px;
            }
            
            .cosmic-button {
                min-height: 44px;
                padding: 14px 20px;
                font-size: 1.1rem;
                width: 100%;
            }
            
            .cosmic-particles-interactive {
                opacity: 0.1; /* Reduced for mobile performance */
            }
            
            .header-title {
                font-size: clamp(2rem, 8vw, 3rem);
                line-height: 1.2;
            }
            
            .element-preview-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }
            
            .form-title {
                font-size: 1.5rem;
            }
            
            .form-subtitle {
                font-size: 0.9rem;
            }
            
            .element-bubble {
                min-height: 100px;
                padding: 12px;
            }
        }
        
        @media (max-width: 480px) {
            .form-container {
                padding: 0.75rem;
                margin: 0.25rem;
            }
            
            .cosmic-button {
                padding: 16px 20px;
                font-size: 1rem;
            }
            
            .element-preview-grid {
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }
            
            .form-title {
                font-size: 1.3rem;
            }
            
            .element-bubble {
                min-height: 80px;
                padding: 10px;
            }
        }
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 200px;
            background: linear-gradient(to top, 
                rgba(139, 90, 43, 0.3) 0%, 
                rgba(160, 82, 45, 0.2) 30%, 
                transparent 70%);
            clip-path: polygon(0% 100%, 10% 60%, 20% 80%, 30% 50%, 40% 70%, 50% 30%, 60% 70%, 70% 50%, 80% 80%, 90% 60%, 100% 100%);
            z-index: -1;
        }
        
        .floating-hieroglyph {
            position: fixed;
            color: rgba(255, 215, 0, 0.4);
            font-size: 3rem;
            animation: float-hieroglyph 15s ease-in-out infinite;
            z-index: 1;
            pointer-events: none;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        }
        
        @keyframes float-hieroglyph {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
        }
        
        .floating-hieroglyph:nth-child(1) { 
            left: 10%; 
            animation-delay: 0s; 
            animation-duration: 20s; 
        }
        .floating-hieroglyph:nth-child(2) { 
            left: 25%; 
            animation-delay: 5s; 
            animation-duration: 18s; 
        }
        .floating-hieroglyph:nth-child(3) { 
            left: 40%; 
            animation-delay: 10s; 
            animation-duration: 22s; 
        }
        .floating-hieroglyph:nth-child(4) { 
            left: 60%; 
            animation-delay: 15s; 
            animation-duration: 19s; 
        }
        .floating-hieroglyph:nth-child(5) { 
            left: 80%; 
            animation-delay: 20s; 
            animation-duration: 21s; 
        }
        .floating-hieroglyph:nth-child(6) { 
            left: 90%; 
            animation-delay: 25s; 
            animation-duration: 17s; 
        }
        
        .stone-texture {
            background: linear-gradient(145deg, 
                rgba(139, 90, 43, 0.2) 0%, 
                rgba(160, 82, 45, 0.15) 25%, 
                rgba(101, 67, 33, 0.1) 50%, 
                rgba(139, 90, 43, 0.08) 75%, 
                rgba(160, 82, 45, 0.05) 100%);
            border: 2px solid rgba(255, 215, 0, 0.3);
            box-shadow: 
                inset 0 2px 4px rgba(255, 215, 0, 0.1),
                0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .maya-glyph-border {
            background: linear-gradient(45deg, 
                rgba(255, 215, 0, 0.3) 0%, 
                rgba(255, 215, 0, 0.1) 50%, 
                rgba(255, 215, 0, 0.3) 100%);
            border: 3px solid rgba(255, 215, 0, 0.5);
            border-radius: 20px;
            position: relative;
        }
        
        .maya-glyph-border::before {
            content: "☽ ☾ ☽ ☾ ☽ ☾ ☽ ☾ ☽ ☾ ☽ ☾";
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 215, 0, 0.9);
            padding: 5px 20px;
            border-radius: 15px;
            font-size: 0.8rem;
            letter-spacing: 5px;
        }
        
        .ancient-script {
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
        }
        
        .page-title {
            color: #8B5CF6;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .form-label {
            color: #1D4ED8 !important;
            font-weight: 600;
        }
        
        .form-header {
            color: #1e3a8a !important;
            font-weight: 900 !important;
            font-size: 2rem !important;
            text-shadow: none !important;
        }
        
        .form-text {
            color: #6B46C1 !important;
            font-weight: 500 !important;
        }
        
        .form-description {
            color: #654321 !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        /* Mobile Optimizations - Magical & Responsive */
        @media (max-width: 640px) {
            .container {
                padding: 0.75rem;
            }
            
            .floating-hieroglyph {
                display: none; /* Hide floating hieroglyphs on mobile to prevent positioning issues */
            }
            
            .cosmic-particles-container {
                opacity: 0.06;
            }
            
            .form-container {
                padding: 1.25rem;
                margin: 0.75rem 0;
                border-radius: 1.5rem;
            }
            
            .pulse-glow {
                animation: mobile-glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes mobile-glow {
                0% { text-shadow: 0 0 15px rgba(255, 215, 0, 0.4); }
                100% { text-shadow: 0 0 25px rgba(255, 215, 0, 0.7); }
            }
            
            .gradient-text {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .element-bubble {
                padding: 1rem;
                border-radius: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .element-bubble:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
            
            /* Mobile-specific magical elements */
            .maya-temple {
                height: 120px;
                opacity: 0.4;
            }
            
            .form-input {
                padding: 0.875rem;
                font-size: 1rem;
                border-radius: 0.75rem;
            }
            
            .cosmic-button {
                padding: 0.875rem 1.5rem;
                font-size: 1.125rem;
                border-radius: 0.75rem;
            }
            
            /* Mobile grid optimizations */
            .grid-cols-2 {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }
            
            .grid.gap-6 {
                gap: 1rem;
            }
            
            .grid.gap-4 {
                gap: 0.75rem;
            }
            
            /* Mobile text improvements */
            .text-center.mb-16 {
                margin-bottom: 2rem;
            }
            
            .mb-12 {
                margin-bottom: 2rem;
            }
            
            .mb-8 {
                margin-bottom: 1.5rem;
            }
        }
        
        /* Tablet Optimizations */
        @media (min-width: 641px) and (max-width: 1024px) {
            .container {
                padding: 1.5rem;
            }
            
            .form-container {
                padding: 2rem;
                margin: 1.5rem 0;
            }
            
            .element-bubble {
                padding: 1.25rem;
            }
            
            .grid.gap-6 {
                gap: 1.25rem;
            }
            
            .grid.gap-4 {
                gap: 1rem;
            }
        }
    </style>
</head>
<body class="cosmic-background min-h-screen font-sans">
    <!-- Cosmic Particles Background -->
    <div id="cosmic-particles-bg" class="cosmic-particles-container"></div>
    
    <!-- Floating Maya Hieroglyphs -->
    <div class="floating-hieroglyph">𓂀</div>
    <div class="floating-hieroglyph">𓃭</div>
    <div class="floating-hieroglyph">𓄿</div>
    <div class="floating-hieroglyph">𓅓</div>
    <div class="floating-hieroglyph">𓆃</div>
    <div class="floating-hieroglyph">𓇯</div>
    
    <!-- Maya Temple Silhouette -->
    <div class="maya-temple"></div>
    
    <div class="container mx-auto p-4 lg:p-8">
        
        <!-- Header with Animation -->
        <div class="text-center mb-16 floating-animation">
            <div class="mb-8">
                <h1 class="text-4xl sm:text-5xl lg:text-7xl xl:text-8xl font-bold gradient-text mb-6 pulse-glow">
                    ✨ The Magic is You ✨
                </h1>
                <div class="text-xl sm:text-2xl lg:text-3xl xl:text-4xl font-bold mb-4 drop-shadow-lg" style="color: #1e3a8a !important;">
                    Discover Your Sacred Maya Cosmic Blueprint
                </div>
                <div class="text-base sm:text-lg lg:text-xl xl:text-2xl font-medium drop-shadow-md" style="color: #1e3a8a !important;">
                    🏛️ Ancient Maya Astrology • 🔮 Shamanic Guidance • 🌟 3,000+ Years of Wisdom
                </div>
            </div>
            

        </div>
        
        <!-- Main Authentication Interface -->
        <div class="max-w-2xl mx-auto">
            <!-- Registration Section -->
            <div class="bg-white/95 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/30 form-container pulse-glow stone-texture maya-glyph-border">
                <h2 class="mb-6" style="color: #1e3a8a !important; font-weight: 900 !important; font-size: 2rem !important; text-align: center; text-shadow: none !important;">
                    🏛️ Begin Your Sacred Journey
                </h2>
                <p class="text-center text-blue-700 mb-8 font-medium">Unlock your personalized Maya cosmic blueprint and soul contract</p>
                
                <form id="registerForm" class="space-y-6">
                    <div>
                        <label class="block form-label text-lg mb-3">
                            👤 Full Name <span class="text-sm form-description">(for sacred numerology)</span>
                        </label>
                        <input type="text" id="registerFullName" name="fullName" 
                               placeholder="Enter your complete birth name"
                               class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            📧 Email Address
                        </label>
                        <input type="email" id="registerEmail" name="email" 
                               placeholder="Enter your email address"
                               class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            🔒 Password
                        </label>
                        <input type="password" id="registerPassword" name="password" 
                               placeholder="Create a secure password (min 6 characters)"
                               class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900"
                               required minlength="6">
                    </div>
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            📅 Birth Date <span class="text-red-600">*</span>
                        </label>
                        <input type="date" id="registerBirthDate" name="birthDate"
                               class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <div>
                            <label class="block form-label text-lg mb-3">
                                🕐 Birth Time <span class="text-sm form-description">(optional)</span>
                            </label>
                            <input type="time" id="registerBirthTime" name="birthTime"
                                   class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900">
                            <p class="text-sm text-amber-600 mt-1">For accurate astrological calculations</p>
                        </div>
                        <div>
                            <label class="block form-label text-lg mb-3">
                                🌍 Birth Location <span class="text-sm form-description">(optional)</span>
                            </label>
                            <input type="text" id="registerBirthLocation" name="birthLocation" 
                                   placeholder="City, State, Country"
                                   class="w-full p-4 border-2 border-amber-300 rounded-xl text-lg focus:border-amber-500 focus:outline-none bg-white/90 text-gray-900"
                                   style="color: #111827 !important;">
                            <p class="text-sm text-amber-600 mt-1">For complete astrological analysis</p>
                        </div>
                    </div>
                    
                    <button type="submit" 
                            class="w-full bg-gradient-to-r from-amber-600 to-orange-600 text-white font-bold py-4 rounded-xl text-xl hover:from-amber-700 hover:to-orange-700 transition duration-300 shadow-lg">
                        🏛️ Create My Maya Profile
                    </button>
                    
                    <div class="text-center mt-6 p-4 bg-gray-50 rounded-xl">
                        <p class="text-gray-600 text-sm mb-2">Already have an account?</p>
                        <button type="button" onclick="showLoginForm()" class="text-blue-600 font-bold hover:text-blue-700 underline">
                            Login to Your Profile
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Login Modal -->
        <div id="loginModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
            <div class="bg-white rounded-3xl p-8 shadow-2xl border border-white/30 max-w-md w-full mx-4">
                <h2 class="mb-6" style="color: #1e3a8a !important; font-weight: 900 !important; font-size: 2rem !important; text-align: center; text-shadow: none !important;">
                    🔮 Welcome Back, Cosmic Soul
                </h2>
                <p class="text-center text-blue-700 mb-8 font-medium">Return to your sacred cosmic blueprint and spiritual wisdom</p>
                
                <form id="loginForm" class="space-y-6">
                    <div>
                        <label class="block form-label text-lg mb-3">
                            📧 Email Address
                        </label>
                        <input type="email" id="loginEmail" name="email" 
                               placeholder="Enter your email address"
                               class="w-full p-4 border-2 border-purple-300 rounded-xl text-lg focus:border-purple-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            🔒 Password
                        </label>
                        <input type="password" id="loginPassword" name="password" 
                               placeholder="Enter your password"
                               class="w-full p-4 border-2 border-purple-300 rounded-xl text-lg focus:border-purple-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <button type="submit" 
                            class="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white font-bold py-4 rounded-xl text-xl hover:from-purple-700 hover:to-purple-800 transition duration-300 shadow-lg">
                        🌟 Login to Your Cosmic Profile
                    </button>
                    
                    <div class="text-center mt-4 space-y-2">
                        <button type="button" onclick="showForgotPasswordForm()" class="text-purple-600 hover:text-purple-800 underline font-medium">
                            Forgot Password?
                        </button>
                        <br>
                        <button type="button" onclick="hideLoginForm()" class="text-gray-600 hover:text-gray-800 underline">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Forgot Password Modal -->
        <div id="forgotPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
            <div class="bg-white rounded-3xl p-8 shadow-2xl border border-white/30 max-w-md w-full mx-4">
                <h2 class="mb-6" style="color: #1e3a8a !important; font-weight: 900 !important; font-size: 2rem !important; text-align: center; text-shadow: none !important;">
                    🔐 Reset Your Password
                </h2>
                <p class="text-center text-blue-700 mb-8 font-medium">Enter your email address and we'll send you a reset link</p>
                
                <form id="forgotPasswordForm" class="space-y-6">
                    <div>
                        <label class="block form-label text-lg mb-3">
                            📧 Email Address
                        </label>
                        <input type="email" id="forgotEmail" name="email" 
                               placeholder="Enter your email address"
                               class="w-full p-4 border-2 border-purple-300 rounded-xl text-lg focus:border-purple-500 focus:outline-none bg-white/90 text-gray-900"
                               required>
                    </div>
                    
                    <button type="submit" 
                            class="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white font-bold py-4 rounded-xl text-xl hover:from-purple-700 hover:to-purple-800 transition duration-300 shadow-lg">
                        🔄 Send Reset Link
                    </button>
                    
                    <div class="text-center mt-4 space-y-2">
                        <button type="button" onclick="showLoginForm()" class="text-purple-600 hover:text-purple-800 underline font-medium">
                            Back to Login
                        </button>
                        <br>
                        <button type="button" onclick="hideForgotPasswordForm()" class="text-gray-600 hover:text-gray-800 underline">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Reset Password Modal -->
        <div id="resetPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
            <div class="bg-white rounded-3xl p-8 shadow-2xl border border-white/30 max-w-md w-full mx-4">
                <h2 class="mb-6" style="color: #1e3a8a !important; font-weight: 900 !important; font-size: 2rem !important; text-align: center; text-shadow: none !important;">
                    🔒 Create New Password
                </h2>
                <p class="text-center text-blue-700 mb-8 font-medium">Enter your new password to complete the reset</p>
                
                <form id="resetPasswordForm" class="space-y-6">
                    <input type="hidden" id="resetToken" name="token" value="">
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            🔑 New Password
                        </label>
                        <input type="password" id="newPassword" name="password" 
                               placeholder="Enter new password (min 6 characters)"
                               class="w-full p-4 border-2 border-purple-300 rounded-xl text-lg focus:border-purple-500 focus:outline-none bg-white/90 text-gray-900"
                               required minlength="6">
                    </div>
                    
                    <div>
                        <label class="block form-label text-lg mb-3">
                            🔑 Confirm Password
                        </label>
                        <input type="password" id="confirmPassword" name="confirmPassword" 
                               placeholder="Confirm new password"
                               class="w-full p-4 border-2 border-purple-300 rounded-xl text-lg focus:border-purple-500 focus:outline-none bg-white/90 text-gray-900"
                               required minlength="6">
                    </div>
                    
                    <button type="submit" 
                            class="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white font-bold py-4 rounded-xl text-xl hover:from-purple-700 hover:to-purple-800 transition duration-300 shadow-lg">
                        ✅ Update Password
                    </button>
                    
                    <div class="text-center mt-4">
                        <button type="button" onclick="hideResetPasswordForm()" class="text-gray-600 hover:text-gray-800 underline">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- 35+ Cosmic Elements Preview Section -->
        <div class="max-w-7xl mx-auto mt-20 mb-8">
            <!-- Header -->
            <div class="text-center mb-16">
                <h2 class="text-3xl sm:text-4xl lg:text-6xl xl:text-7xl font-bold gradient-text mb-6 pulse-glow">
                    🌟 Your Cosmic Blueprint Awaits
                </h2>
                <p class="text-lg sm:text-xl lg:text-2xl xl:text-3xl font-bold max-w-4xl mx-auto drop-shadow-lg" style="color: #1e3a8a !important;">
                    Once you register, we'll calculate your complete personalized cosmic blueprint using authentic Maya astronomy
                </p>

            </div>
            
            <!-- Core Maya Elements -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8 flex items-center justify-center drop-shadow-lg" style="color: #1e3a8a !important;">
                    <span class="bg-white/20 px-2 sm:px-4 py-1 sm:py-2 rounded-full mr-2 sm:mr-4 backdrop-blur-md">🔮</span>
                    Core Maya Elements
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🔸</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Day Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Your Maya glyph (e.g. Ahau Sun)</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🎵</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Galactic Tone</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Your cosmic frequency (1-13)</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🆔</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Kin Number</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Your position in 260-day cycle</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🔥</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Element</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Fire, Water, Air, or Earth</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">📱</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Life Path</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Your soul's journey purpose</p>
                    </div>
                </div>
            </div>
            
            <!-- Sacred Calendar Elements -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8 flex items-center justify-center drop-shadow-lg" style="color: #1e3a8a !important;">
                    <span class="bg-white/20 px-2 sm:px-4 py-1 sm:py-2 rounded-full mr-2 sm:mr-4 backdrop-blur-md">📅</span>
                    Sacred Calendar Elements
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-4">
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">⚡</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Trecena</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">13-day sacred cycle</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🌙</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Wavespell</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">13-day consciousness journey</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🏰</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Castle</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">52-day spiritual castle</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🌺</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Color Family</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Red, White, Blue, Yellow</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🏛️</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Tribe</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Maya tribal connection</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🎼</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Harmonic</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">4-day pattern alignment</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">✨</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Activation Portal</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Special energy gateway</p>
                    </div>
                </div>
            </div>
            
            <!-- Maya Cross & Calendar Systems -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8 flex items-center justify-center drop-shadow-lg" style="color: #1e3a8a !important;">
                    <span class="bg-white/20 px-2 sm:px-4 py-1 sm:py-2 rounded-full mr-2 sm:mr-4 backdrop-blur-md">✨</span>
                    Maya Cross & Calendar Systems
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🧭</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Guide Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Higher guidance</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">⚖️</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Antipode Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Balancing opposite</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🔮</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Occult Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Hidden powers</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🌙</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Lord of Night</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">9-day cycle guardian</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">☀️</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Haab Date</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Solar calendar position</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">📊</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Long Count</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Astronomical dating</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🎯</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Year Bearer</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Annual energy influence</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-6 text-center">
                        <div class="text-4xl mb-3">🌕</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a !important;">Moon Phase</h4>
                        <p class="text-sm" style="color: #1e3a8a !important;">Lunar cycle connection</p>
                    </div>
                </div>
            </div>
            
            <!-- Spiritual & Natural Elements -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8 flex items-center justify-center drop-shadow-lg" style="color: #1e3a8a !important;">
                    <span class="bg-white/20 px-2 sm:px-4 py-1 sm:py-2 rounded-full mr-2 sm:mr-4 backdrop-blur-md">🌿</span>
                    Spiritual & Natural Elements
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-4">
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🦌</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Spirit Animal</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Power animal ally</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">💎</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Crystal Ally</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Healing crystal connection</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🌿</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Plant Medicine</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Sacred plant ally</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🧘</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Chakra Resonance</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Energy center alignment</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">⚡</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Human Design</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Energy type & strategy</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🌳</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Tree of Life</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Primary Sephiroth</p>
                    </div>
                    <div class="element-bubble rounded-2xl p-4 text-center">
                        <div class="text-3xl mb-2">🌲</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a !important;">Secondary Tree</h4>
                        <p class="text-xs" style="color: #1e3a8a !important;">Secondary Sephiroth</p>
                    </div>
                </div>
            </div>

        </div>
        
        <!-- JavaScript for form handling and UI interactions -->
        <script>
            // Initialize cosmic particles background
            document.addEventListener('DOMContentLoaded', function() {
                // Create default cosmic particles for homepage
                const defaultUserData = {
                    element: 'Fire',
                    galacticTone: 1,
                    daySign: 'Ahau',
                    lifePath: 5,
                    kinNumber: 1
                };
                
                // Initialize background particles
                if (typeof initCosmicParticles === 'function') {
                    initCosmicParticles('cosmic-particles-bg', defaultUserData);
                }
            });
            
            function switchToLogin() {
                // Scroll to login form
                document.querySelector('#loginForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            function switchToRegister() {
                // Scroll to register form
                document.querySelector('#registerForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            function showLoginForm() {
                // Show the login modal
                document.getElementById('loginModal').classList.remove('hidden');
            }
            
            function hideLoginForm() {
                // Hide the login modal
                document.getElementById('loginModal').classList.add('hidden');
            }
            
            function showForgotPasswordForm() {
                // Hide login modal and show forgot password modal
                document.getElementById('loginModal').classList.add('hidden');
                document.getElementById('forgotPasswordModal').classList.remove('hidden');
            }
            
            function hideForgotPasswordForm() {
                // Hide forgot password modal
                document.getElementById('forgotPasswordModal').classList.add('hidden');
            }
            
            function showResetPasswordForm(token) {
                // Show reset password modal with token
                document.getElementById('resetToken').value = token;
                document.getElementById('resetPasswordModal').classList.remove('hidden');
            }
            
            function hideResetPasswordForm() {
                // Hide reset password modal
                document.getElementById('resetPasswordModal').classList.add('hidden');
            }
            
            // Check for reset token in URL on page load
            document.addEventListener('DOMContentLoaded', function() {
                const urlParams = new URLSearchParams(window.location.search);
                const resetToken = urlParams.get('token');
                if (resetToken) {
                    showResetPasswordForm(resetToken);
                }
            });
        </script>

        <!-- JavaScript for form handling -->
        <script>
            // Login form handler
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const email = document.getElementById('loginEmail').value;
                const password = document.getElementById('loginPassword').value;
                
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ email, password })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        localStorage.setItem('token', result.token);
                        window.location.href = '/user-profile';
                    } else {
                        const error = await response.json();
                        alert('Login failed: ' + error.detail);
                    }
                } catch (error) {
                    alert('Login failed: ' + error.message);
                }
            });
            
            // Registration form handler
            document.getElementById('registerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const fullName = document.getElementById('registerFullName').value;
                const email = document.getElementById('registerEmail').value;
                const password = document.getElementById('registerPassword').value;
                const birthDate = document.getElementById('registerBirthDate').value;
                const birthTime = document.getElementById('registerBirthTime').value;
                const birthLocation = document.getElementById('registerBirthLocation').value;
                
                // Show loading state
                const submitBtn = document.querySelector('#registerForm button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '✨ Creating Your Cosmic Profile...';
                submitBtn.disabled = true;
                
                try {
                    console.log('Sending registration request...');
                    const response = await fetch('/api/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            fullName,
                            email,
                            password,
                            birthDate,
                            birthTime,
                            birthLocation
                        })
                    });
                    
                    console.log('Registration response status:', response.status);
                    
                    if (response.ok) {
                        const result = await response.json();
                        console.log('Registration successful, token received:', !!result.token);
                        
                        if (result.token) {
                            localStorage.setItem('token', result.token);
                            console.log('Token stored, redirecting to user-profile...');
                            
                            // Force redirect with small delay
                            setTimeout(() => {
                                window.location.href = '/user-profile';
                            }, 100);
                        } else {
                            console.error('No token received in response');
                            alert('Registration successful but no token received. Please try logging in.');
                        }
                    } else {
                        const error = await response.json();
                        console.error('Registration failed:', error);
                        
                        // Check if it's a duplicate email error
                        if (response.status === 409 || (error.detail && error.detail.includes('already exists'))) {
                            // Show user-friendly message and offer to show login form
                            if (confirm('It looks like you already have an account with this email. Would you like to login instead?')) {
                                showLoginForm();
                            }
                        } else {
                            alert('Registration failed: ' + (error.detail || 'Unknown error'));
                        }
                    }
                } catch (error) {
                    console.error('Registration error:', error);
                    alert('Registration failed: ' + error.message);
                } finally {
                    // Reset button state
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }
            });
            
            // Forgot Password form handler
            document.getElementById('forgotPasswordForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const email = document.getElementById('forgotEmail').value;
                
                // Show loading state
                const submitBtn = document.querySelector('#forgotPasswordForm button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '📨 Sending Reset Link...';
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/forgot-password', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ email })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        hideForgotPasswordForm();
                    } else {
                        const error = await response.json();
                        alert('Error: ' + error.detail);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    // Reset button state
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }
            });
            
            // Reset Password form handler
            document.getElementById('resetPasswordForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const token = document.getElementById('resetToken').value;
                const password = document.getElementById('newPassword').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                // Validate passwords match
                if (password !== confirmPassword) {
                    alert('Passwords do not match');
                    return;
                }
                
                // Show loading state
                const submitBtn = document.querySelector('#resetPasswordForm button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.textContent = '🔄 Updating Password...';
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/reset-password', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ token, password })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        alert(result.message);
                        hideResetPasswordForm();
                        showLoginForm();
                    } else {
                        const error = await response.json();
                        alert('Error: ' + error.detail);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    // Reset button state
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }
            });
        </script>
        
        <!-- Initialize Cosmic Particles -->
        <script>
            // Initialize cosmic particles after page load
            document.addEventListener('DOMContentLoaded', function() {
                try {
                    // Check if Three.js is loaded
                    if (typeof THREE !== 'undefined' && typeof CosmicAttractorScene !== 'undefined') {
                        // Create particle system with default spiritual configuration
                        const defaultUserData = {
                            element: 'Fire',
                            galactic_tone: 'Magnetic',
                            life_path: 1200,
                            day_sign: 'Ahau',
                            cosmic_signature: 'Seeker of Ancient Wisdom'
                        };
                        
                        // Initialize particles for homepage
                        const cosmicParticles = new CosmicAttractorScene('cosmic-particles-bg', defaultUserData);
                        
                        console.log('Cosmic particles initialized successfully on homepage');
                    } else {
                        console.log('Three.js or CosmicAttractorScene not available, particles disabled');
                    }
                } catch (error) {
                    console.error('Error initializing cosmic particles:', error);
                }
            });
        </script>
    </div>
</body>
</html>"""

# API Routes
@app.post("/register")
async def register_form(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(None),
    birth_location: str = Form(None)
):
    """Register new user with Maya blueprint calculation - Form endpoint"""
    import psycopg2
    
    try:
        # Validate required fields
        if not email or not password or not full_name or not birth_date:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Check if user already exists
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            raise HTTPException(status_code=409, detail="An account with this email already exists. Please use the login button to access your cosmic profile.")
        
        # Generate unique user ID
        user_id = f"user_{hash(email + str(datetime.now()))}".replace("-", "")
        
        # Hash password
        password_hash = hash_password(password)
        
        # Calculate Maya cosmic signature with error handling
        try:
            maya_data = calculate_maya_blueprint(birth_date, birth_time, birth_location)
            print(f"Maya data calculated successfully: {maya_data}")
        except Exception as calc_error:
            print(f"Maya calculation error: {calc_error}")
            # Provide fallback minimal data
            maya_data = {
                "day_sign": "Unknown",
                "galactic_tone": "Unknown", 
                "kin_number": 0,
                "element": "Unknown",
                "direction": "Unknown",
                "life_path": 1
            }
        
        # Parse full name into first and last name
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # Insert user into database with correct column names
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, first_name, last_name, is_onboarding_complete)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id, email, password_hash, first_name, last_name, True
        ))
        
        # Helper function to safely convert to JSON string
        def safe_json_dumps(value):
            if value is None:
                return None
            try:
                # Always convert to JSON format
                return json.dumps(value)
            except (TypeError, ValueError):
                return json.dumps(str(value))

        # Insert Maya cosmic profile data with all calculated elements
        cursor.execute("""
            INSERT INTO maya_profiles (user_id, birth_date, birth_time, birth_location, 
                                     day_sign, galactic_tone, kin_number, element, 
                                     direction, life_path, color_family, tribe, 
                                     guide_sign, antipode_sign, occult_sign, lord_of_night,
                                     haab_date, long_count, year_bearer, moon_phase,
                                     galactic_activation_portal, spirit_animal, crystal_ally,
                                     plant_medicine, chakra_resonance, human_design_type,
                                     tree_of_life_primary, tree_of_life_secondary,
                                     trecena, trecena_description, wavespell, wavespell_description,
                                     castle, castle_description, harmonic, cosmic_profile)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, birth_date, birth_time, birth_location,
            safe_json_dumps(maya_data.get("day_sign", "Unknown")), 
            safe_json_dumps(maya_data.get("galactic_tone", "Unknown")),
            maya_data.get("kin_number", 0), 
            maya_data.get("element", "Unknown"),
            maya_data.get("direction", "Unknown"), 
            maya_data.get("life_path", 1),
            maya_data.get("color_family", "Unknown"),
            maya_data.get("tribe", "Unknown"),
            safe_json_dumps(maya_data.get("guide_sign", "Unknown")),
            safe_json_dumps(maya_data.get("antipode_sign", "Unknown")),
            safe_json_dumps(maya_data.get("occult_sign", "Unknown")),
            maya_data.get("lord_of_night", 0),
            maya_data.get("haab_date", "Unknown"),
            maya_data.get("long_count", "Unknown"),
            maya_data.get("year_bearer", "Unknown"),
            maya_data.get("moon_phase", "Unknown"),
            maya_data.get("galactic_activation_portal", "Unknown"),
            maya_data.get("spirit_animal", "Unknown"),
            maya_data.get("crystal_ally", "Unknown"),
            maya_data.get("plant_medicine", "Unknown"),
            maya_data.get("chakra_resonance", "Unknown"),
            maya_data.get("human_design_type", "Unknown"),
            maya_data.get("tree_of_life_primary", "Unknown"),
            maya_data.get("tree_of_life_secondary", "Unknown"),
            maya_data.get("trecena", "Unknown"),
            maya_data.get("trecena_description", "Unknown"),
            maya_data.get("wavespell", "Unknown"),
            maya_data.get("wavespell_description", "Unknown"),
            maya_data.get("castle", "Unknown"),
            maya_data.get("castle_description", "Unknown"),
            maya_data.get("harmonic", "Unknown"),
            safe_json_dumps(maya_data)
        ))
        
        conn.commit()
        conn.close()
        
        # Create JWT token
        token = create_jwt_token(user_id)
        
        return {"message": "User registered successfully", "token": token, "user_id": user_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/api/register")
async def register(request: Request):
    """Register new user with Maya blueprint calculation"""
    import psycopg2
    
    try:
        data = await request.json()
        
        # Validate required fields
        if not data.get("email") or not data.get("password") or not data.get("fullName") or not data.get("birthDate"):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Check if user already exists
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (data["email"],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            raise HTTPException(status_code=409, detail="An account with this email already exists. Please use the login button to access your cosmic profile.")
        
        # Generate unique user ID
        user_id = f"user_{hash(data['email'] + str(datetime.now()))}".replace("-", "")
        
        # Hash password
        password_hash = hash_password(data["password"])
        
        # Calculate Maya cosmic signature with error handling
        try:
            maya_data = calculate_maya_blueprint(data["birthDate"], data.get("birthTime"), data.get("birthLocation"))
            print(f"Maya data calculated successfully: {maya_data}")
        except Exception as calc_error:
            print(f"Maya calculation error: {calc_error}")
            # Provide fallback minimal data
            maya_data = {
                "day_sign": "Unknown",
                "galactic_tone": "Unknown", 
                "kin_number": 0,
                "element": "Unknown",
                "direction": "Unknown",
                "life_path": 1
            }
        
        # Parse full name into first and last name
        full_name = data["fullName"]
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # Insert user into database with correct column names
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, first_name, last_name, is_onboarding_complete)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id, data["email"], password_hash, first_name, last_name, True
        ))
        
        # Helper function to safely convert to JSON string
        def safe_json_dumps(value):
            if value is None:
                return None
            try:
                # Always convert to JSON format
                return json.dumps(value)
            except (TypeError, ValueError):
                return json.dumps(str(value))

        # Insert Maya cosmic profile data with all calculated elements
        cursor.execute("""
            INSERT INTO maya_profiles (user_id, birth_date, birth_time, birth_location, 
                                     day_sign, galactic_tone, kin_number, element, 
                                     direction, life_path, color_family, tribe, 
                                     guide_sign, antipode_sign, occult_sign, lord_of_night,
                                     haab_date, long_count, year_bearer, moon_phase,
                                     galactic_activation_portal, spirit_animal, crystal_ally,
                                     plant_medicine, chakra_resonance, human_design_type,
                                     tree_of_life_primary, tree_of_life_secondary,
                                     trecena, trecena_description, wavespell, wavespell_description,
                                     castle, castle_description, harmonic, cosmic_profile)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, 
            data["birthDate"], 
            data.get("birthTime"), 
            data.get("birthLocation"),
            safe_json_dumps(maya_data.get("day_sign", "Unknown")), 
            safe_json_dumps(maya_data.get("galactic_tone", "Unknown")),
            maya_data.get("kin_number", 0), 
            maya_data.get("element", "Unknown"), 
            maya_data.get("direction", "Unknown"),
            maya_data.get("life_path", 1),
            maya_data.get("color_family", "Unknown"),
            maya_data.get("tribe", "Unknown"),
            safe_json_dumps(maya_data.get("guide_sign", "Unknown")),
            safe_json_dumps(maya_data.get("antipode_sign", "Unknown")),
            safe_json_dumps(maya_data.get("occult_sign", "Unknown")),
            maya_data.get("lord_of_night", 0),
            maya_data.get("haab_date", "Unknown"),
            maya_data.get("long_count", "Unknown"),
            maya_data.get("year_bearer", "Unknown"),
            maya_data.get("moon_phase", "Unknown"),
            maya_data.get("galactic_activation_portal", "Unknown"),
            maya_data.get("spirit_animal", "Unknown"),
            maya_data.get("crystal_ally", "Unknown"),
            maya_data.get("plant_medicine", "Unknown"),
            maya_data.get("chakra_resonance", "Unknown"),
            maya_data.get("human_design_type", "Unknown"),
            maya_data.get("tree_of_life_primary", "Unknown"),
            maya_data.get("tree_of_life_secondary", "Unknown"),
            maya_data.get("trecena", "Unknown"),
            maya_data.get("trecena_description", "Unknown"),
            maya_data.get("wavespell", "Unknown"),
            maya_data.get("wavespell_description", "Unknown"),
            maya_data.get("castle", "Unknown"),
            maya_data.get("castle_description", "Unknown"),
            maya_data.get("harmonic", "Unknown"),
            safe_json_dumps(maya_data)
        ))
        
        conn.commit()
        conn.close()
        
        # Create JWT token
        token = create_jwt_token(user_id)
        
        return {"message": "User registered successfully", "token": token, "user_id": user_id}
        
    except psycopg2.IntegrityError as e:
        # Handle database integrity errors (like duplicate email)
        if "unique constraint" in str(e).lower() and "email" in str(e).lower():
            raise HTTPException(status_code=409, detail="An account with this email already exists. Please use the login button to access your cosmic profile.")
        else:
            raise HTTPException(status_code=400, detail="Database error: " + str(e))
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/login")
async def login_form(
    email: str = Form(...),
    password: str = Form(...)
):
    """Login user and return JWT token - Form endpoint"""
    import psycopg2
    
    try:
        # Validate required fields
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Find user in database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(password, user[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        token = create_jwt_token(user[0])
        
        return {"message": "Login successful", "token": token, "user_id": user[0]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login(request: Request):
    """Login user and return JWT token"""
    import psycopg2
    
    try:
        data = await request.json()
        
        # Validate required fields
        if not data.get("email") or not data.get("password"):
            raise HTTPException(status_code=400, detail="Email and password required")
        
        # Find user in database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (data["email"],))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(data["password"], user[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        token = create_jwt_token(user[0])
        
        return {"message": "Login successful", "token": token, "user_id": user[0]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forgot-password")
async def forgot_password(request: Request):
    """Send password reset email"""
    import psycopg2
    
    try:
        data = await request.json()
        
        # Validate required fields
        if not data.get("email"):
            raise HTTPException(status_code=400, detail="Email required")
        
        email = data["email"]
        
        # Check if user exists
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            # Don't reveal if email exists or not for security
            return {"message": "If the email exists, a reset link has been sent"}
        
        user_id = user[0]
        
        # Generate reset token
        token = generate_reset_token()
        expires_at = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
        
        # Store token in database
        cursor.execute("""
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (%s, %s, %s)
        """, (user_id, token, expires_at))
        conn.commit()
        conn.close()
        
        # Send email (in production, this would use an email service)
        send_password_reset_email(email, token)
        
        return {"message": "If the email exists, a reset link has been sent"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset-password")
async def reset_password(request: Request):
    """Reset password using token"""
    import psycopg2
    
    try:
        data = await request.json()
        
        # Validate required fields
        if not data.get("token") or not data.get("password"):
            raise HTTPException(status_code=400, detail="Token and password required")
        
        token = data["token"]
        new_password = data["password"]
        
        # Validate password strength
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Find valid token
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id FROM password_reset_tokens 
            WHERE token = %s AND expires_at > NOW() AND used = FALSE
        """, (token,))
        token_data = cursor.fetchone()
        
        if not token_data:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        user_id = token_data[0]
        
        # Update password
        password_hash = hash_password(new_password)
        cursor.execute("""
            UPDATE users SET password_hash = %s WHERE id = %s
        """, (password_hash, user_id))
        
        # Mark token as used
        cursor.execute("""
            UPDATE password_reset_tokens SET used = TRUE WHERE token = %s
        """, (token,))
        
        conn.commit()
        conn.close()
        
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user")
async def get_user(user = Depends(get_current_user)):
    """Get current user information with complete cosmic profile"""
    import psycopg2
    
    try:
        # Get user's complete cosmic profile from database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, mp.birth_date, mp.birth_time, 
                   mp.birth_location, mp.cosmic_profile, mp.day_sign, mp.galactic_tone,
                   mp.kin_number, mp.element, mp.direction, mp.life_path,
                   mp.color_family, mp.tribe, mp.guide_sign, mp.antipode_sign, mp.occult_sign,
                   mp.lord_of_night, mp.haab_date, mp.long_count, mp.year_bearer, mp.moon_phase,
                   mp.galactic_activation_portal, mp.spirit_animal, mp.crystal_ally, mp.plant_medicine,
                   mp.chakra_resonance, mp.human_design_type, mp.tree_of_life_primary, mp.tree_of_life_secondary,
                   mp.trecena, mp.trecena_description, mp.wavespell, mp.wavespell_description,
                   mp.castle, mp.castle_description, mp.harmonic
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            # Return basic user info if no cosmic profile found
            return {
                "user_id": user.get('id'),
                "email": user.get('email'),
                "first_name": user.get('first_name'),
                "last_name": user.get('last_name'),
                "full_name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                "birth_date": None,
                "birth_time": None,
                "birth_location": None,
                "cosmic_profile": {}
            }
        
        # Parse all the cosmic data from the database
        (first_name, last_name, email, birth_date, birth_time, birth_location, cosmic_profile_json, 
         day_sign_json, galactic_tone_json, kin_number, element, direction, life_path,
         color_family, tribe, guide_sign, antipode_sign, occult_sign, lord_of_night, haab_date, 
         long_count, year_bearer, moon_phase, galactic_activation_portal, spirit_animal, 
         crystal_ally, plant_medicine, chakra_resonance, human_design_type, tree_of_life_primary, 
         tree_of_life_secondary, trecena, trecena_description, wavespell, wavespell_description, 
         castle, castle_description, harmonic) = user_data
        
        # Parse cosmic profile
        cosmic_profile = {}
        if cosmic_profile_json:
            if isinstance(cosmic_profile_json, str):
                cosmic_profile = json.loads(cosmic_profile_json)
            else:
                cosmic_profile = cosmic_profile_json
        
        # Parse day sign and galactic tone
        day_sign_name = "Unknown"
        galactic_tone_name = "Unknown"
        if day_sign_json:
            if isinstance(day_sign_json, str):
                day_sign_data = json.loads(day_sign_json)
                day_sign_name = day_sign_data.get('name', 'Unknown')
            else:
                day_sign_name = day_sign_json.get('name', 'Unknown') if isinstance(day_sign_json, dict) else str(day_sign_json)
        
        if galactic_tone_json:
            if isinstance(galactic_tone_json, str):
                galactic_tone_data = json.loads(galactic_tone_json)
                galactic_tone_name = galactic_tone_data.get('name', 'Unknown')
            else:
                galactic_tone_name = galactic_tone_json.get('name', 'Unknown') if isinstance(galactic_tone_json, dict) else str(galactic_tone_json)
        
        return {
            "user_id": user.get('id'),
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}".strip(),
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            "day_sign": day_sign_name,
            "galactic_tone": galactic_tone_name,
            "kin_number": kin_number,
            "element": element,
            "direction": direction,
            "life_path": life_path,
            "color_family": color_family,
            "tribe": tribe,
            "guide_sign": guide_sign,
            "antipode_sign": antipode_sign,
            "occult_sign": occult_sign,
            "lord_of_night": lord_of_night,
            "haab_date": haab_date,
            "long_count": long_count,
            "year_bearer": year_bearer,
            "moon_phase": moon_phase,
            "galactic_activation_portal": galactic_activation_portal,
            "spirit_animal": spirit_animal,
            "crystal_ally": crystal_ally,
            "plant_medicine": plant_medicine,
            "chakra_resonance": chakra_resonance,
            "human_design_type": human_design_type,
            "tree_of_life_primary": tree_of_life_primary,
            "tree_of_life_secondary": tree_of_life_secondary,
            "trecena": trecena,
            "trecena_description": trecena_description,
            "wavespell": wavespell,
            "wavespell_description": wavespell_description,
            "castle": castle,
            "castle_description": castle_description,
            "harmonic": harmonic,
            "cosmic_profile": cosmic_profile
        }
        
    except Exception as e:
        # Return basic user info if error occurs
        return {
            "user_id": user.get('id'),
            "email": user.get('email'),
            "first_name": user.get('first_name'),
            "last_name": user.get('last_name'),
            "full_name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
            "birth_date": None,
            "birth_time": None,
            "birth_location": None,
            "cosmic_profile": {}
        }

@app.post("/api/ai-cosmic-explanation")
async def get_cosmic_explanation(request: Request, user = Depends(get_current_user)):
    """Generate AI-powered explanation for cosmic elements with ML personalization"""
    try:
        body = await request.json()
        element_type = body.get('element_type', '')
        element_value = body.get('element_value', '')
        time_spent = body.get('time_spent', 0)
        engagement_level = body.get('engagement_level', 5)
        
        # Track user interaction for ML
        spiritual_ml_engine.track_user_interaction(
            user_id=user.get('id', ''),
            interaction_type=f"cosmic_explanation_{element_type}",
            element_accessed=f"{element_type}_{element_value}",
            time_spent=time_spent,
            engagement_level=engagement_level
        )
        
        # Generate personalized explanation using enhanced content engine
        from personalized_content_engine import generate_personalized_content
        
        # Get user's full profile for comprehensive personalization
        user_profile = await get_user(user)
        
        # Generate comprehensive personalized explanation
        try:
            # Use enhanced personalized content engine for deeply personalized explanations
            explanation = generate_personalized_content(
                element_type=element_type,
                element_value=element_value,
                user_data=user_profile
            )
            
            return {"explanation": explanation, "personalized": True}
            
        except Exception as e:
            print(f"Element explanation error: {e}")
            # Generate fallback explanation using AI spiritual engine
            try:
                from ai_spiritual_engine import get_personalized_element_snapshot
                explanation = get_personalized_element_snapshot(
                    user_id=user.get('id', ''),
                    user_data=user_profile,
                    element_name=element_type,
                    element_value=element_value
                )
                return {"explanation": explanation, "personalized": True}
            except Exception as fallback_error:
                print(f"Fallback explanation error: {fallback_error}")
                # Final fallback
                explanation = f"""**{element_value} - Your Sacred Cosmic Element**

{user_name}, this element of your cosmic blueprint carries profound spiritual significance. The ancient Maya understood that each aspect of your cosmic signature reveals a unique facet of your soul's purpose and divine gifts.

**Your Sacred Connection:**
This element represents a sacred thread in the tapestry of your cosmic identity. It reveals hidden strengths, spiritual gifts, and divine purpose that the Maya gods have woven into your soul's journey.

**Your Spiritual Invitation:**
Meditate on this element and allow its wisdom to reveal itself to you. Each aspect of your cosmic blueprint is a doorway to deeper self-understanding and spiritual awakening.

🌟 Sacred wisdom flows through your {element_type} {element_value}, guiding your spiritual journey with ancient Maya insights. The Magic is You!"""
                return {"explanation": explanation, "personalized": True}
        
    except Exception as e:
        # Generate fallback explanation for any errors
        fallback_explanation = f"""**{element_value} - Your Sacred Cosmic Element**

{user.get('first_name', 'Sacred Soul')}, this element of your cosmic blueprint carries profound spiritual significance. The ancient Maya understood that each aspect of your cosmic signature reveals a unique facet of your soul's purpose and divine gifts.

**Your Sacred Connection:**
This element represents a sacred thread in the tapestry of your cosmic identity. It reveals hidden strengths, spiritual gifts, and divine purpose that the Maya gods have woven into your soul's journey.

**Your Spiritual Invitation:**
Meditate on this element and allow its wisdom to reveal itself to you. Each aspect of your cosmic blueprint is a doorway to deeper self-understanding and spiritual awakening.

🌟 Sacred wisdom flows through your {element_type} {element_value}, guiding your spiritual journey with ancient Maya insights. The Magic is You!"""
        
        return {"explanation": fallback_explanation, "error": str(e)}

def format_blueprint_analysis(text):
    """Format blueprint analysis text with proper HTML structure"""
    if not text:
        return ""
    
    # Split into sections by numbered headings
    sections = []
    current_section = ""
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a numbered section header (e.g., "1. Soul Essence", "2. Divine Gifts")
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '**1.', '**2.', '**3.', '**4.', '**5.', '**6.')):
            # Save previous section if exists
            if current_section:
                sections.append(current_section)
            # Start new section with proper heading
            clean_line = line.replace('**', '').strip()
            current_section = f'<h3 style="color: #8B4513; font-weight: 600; margin-top: 30px; margin-bottom: 15px; font-size: 1.2rem;">{clean_line}</h3>'
        else:
            # Regular content - format as paragraph
            if line.startswith('- '):
                # List item
                current_section += f'<p style="margin: 8px 0; margin-left: 20px;">• {line[2:].strip()}</p>'
            else:
                # Regular paragraph
                formatted_line = line.replace('**', '<strong>').replace('*', '').replace('</strong>', '</strong>')
                current_section += f'<p style="margin: 15px 0; text-align: justify;">{formatted_line}</p>'
    
    # Add the last section
    if current_section:
        sections.append(current_section)
    
    # Join all sections
    return ''.join(sections)

@app.get("/api/download-cosmic-blueprint")
async def download_cosmic_blueprint(user = Depends(get_current_user)):
    """Generate and download beautiful HTML cosmic blueprint"""
    import psycopg2
    
    try:
        # Get user's cosmic profile from database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, mp.birth_date, mp.birth_time, 
                   mp.birth_location, mp.cosmic_profile
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        first_name, last_name, email, birth_date, birth_time, birth_location, cosmic_profile = user_data
        
        # Parse cosmic profile
        if cosmic_profile:
            if isinstance(cosmic_profile, str):
                cosmic_data = json.loads(cosmic_profile)
            else:
                cosmic_data = cosmic_profile
        else:
            # Generate cosmic data if not available
            cosmic_data = calculate_maya_blueprint(birth_date, birth_time, birth_location)
        
        # Generate comprehensive blueprint analysis
        blueprint_analysis = ""
        try:
            # Get the comprehensive blueprint analysis from the existing endpoint
            analysis_response = await generate_enhanced_blueprint_analysis(user)
            blueprint_analysis = analysis_response.get('full_analysis', '')
        except:
            # Fallback comprehensive analysis
            day_sign = cosmic_data.get('day_sign', {}).get('name', 'Unknown') if isinstance(cosmic_data.get('day_sign'), dict) else str(cosmic_data.get('day_sign', 'Unknown'))
            galactic_tone = cosmic_data.get('galactic_tone', {}).get('name', 'Unknown') if isinstance(cosmic_data.get('galactic_tone'), dict) else str(cosmic_data.get('galactic_tone', 'Unknown'))
            element = cosmic_data.get('element', 'Unknown')
            direction = cosmic_data.get('direction', 'Unknown')
            
            blueprint_analysis = f"""**🌙 Your Sacred Cosmic Blueprint**
**Spiritual Blueprint Analysis for {first_name} {last_name}**

**1. Soul Essence**
{first_name}, your cosmic signature of {day_sign} {galactic_tone} reveals you as a divine being carrying the sacred wisdom of the {element} element. Your soul resonates with the {direction} direction, connecting you to powerful spiritual currents that guide your journey.

**2. Divine Gifts**
- Natural alignment with {element} energy and {direction} wisdom
- Spiritual connection through your {day_sign} essence
- Cosmic resonance with {galactic_tone} vibration
- Guidance from your spiritual allies and cosmic elements

**3. Sacred Mission**
Your cosmic blueprint reveals your purpose as a spiritual guide and wisdom keeper. You are here to embody the teachings of {day_sign} and share the transformative power of {element} energy with the world.

**4. Growth Opportunities**
- Deepening your connection to {element} wisdom
- Balancing your {day_sign} energy with daily spiritual practice
- Exploring your spiritual nature and cosmic connections
- Strengthening your relationship with spiritual guides

**5. Cosmic Connections**
Your cosmic elements weave a tapestry of interconnected energies that guide your spiritual journey. The {day_sign} aligns with divine wisdom, harmonizing with your {element} element to amplify your transformative energy.

**6. Practical Guidance**
- Daily meditation facing the {direction} direction
- Work with your cosmic elements for spiritual amplification
- Connect with sacred practices that honor your spiritual nature
- Practice balancing your energy centers and spiritual alignment

**Affirmation**
"I am a unique expression of divine consciousness. My cosmic signature is a sacred gift that connects me to the infinite wisdom of the universe. The Magic is You!"
"""
        
        # Get current date for blueprint generation
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Generate beautiful HTML blueprint
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sacred Cosmic Blueprint - {first_name} {last_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&family=Cinzel:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #654321 0%, #8B4513 50%, #CD853F 100%);
            color: #2D1810;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .blueprint-container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border: 3px solid #DAA520;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #DAA520;
        }}
        .title {{
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            color: #8B4513;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .subtitle {{
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
            color: #DAA520;
            margin-bottom: 5px;
        }}
        .date {{
            font-size: 0.9rem;
            color: #8B4513;
            opacity: 0.8;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(218, 165, 32, 0.1);
            border-radius: 15px;
            border-left: 4px solid #DAA520;
        }}
        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 1.4rem;
            color: #8B4513;
            margin-bottom: 15px;
            text-align: center;
        }}
        .element-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .element {{
            background: rgba(255, 255, 255, 0.8);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #DAA520;
        }}
        .element-name {{
            font-weight: 600;
            color: #8B4513;
            margin-bottom: 5px;
        }}
        .element-value {{
            color: #654321;
            font-size: 0.9rem;
        }}
        .sacred-signature {{
            text-align: center;
            background: linear-gradient(135deg, #DAA520, #FFD700);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            font-family: 'Cinzel', serif;
        }}
        .signature-main {{
            font-size: 1.8rem;
            margin-bottom: 10px;
        }}
        .signature-detail {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        @media print {{
            body {{ background: white; }}
            .blueprint-container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="blueprint-container">
        <div class="header">
            <h1 class="title">🌟 Sacred Cosmic Blueprint</h1>
            <p class="subtitle">Personalized Maya Wisdom for {first_name} {last_name}</p>
            <p class="date">Generated on {current_date}</p>
        </div>
        
        <div class="sacred-signature">
            <div class="signature-main">
                {cosmic_data.get('day_sign', {}).get('name', 'Unknown')} {cosmic_data.get('galactic_tone', {}).get('name', 'Unknown')}
            </div>
            <div class="signature-detail">
                Kin {cosmic_data.get('kin_number', 'Unknown')} • {cosmic_data.get('element', 'Unknown')} Energy
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🔮 Core Maya Signature</h2>
            <div class="element-grid">
                <div class="element">
                    <div class="element-name">Maya Day Sign</div>
                    <div class="element-value">{cosmic_data.get('day_sign', {}).get('name', 'Unknown')} - {cosmic_data.get('day_sign', {}).get('meaning', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Galactic Tone</div>
                    <div class="element-value">{cosmic_data.get('galactic_tone', {}).get('name', 'Unknown')} - {cosmic_data.get('galactic_tone', {}).get('meaning', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Kin Number</div>
                    <div class="element-value">{cosmic_data.get('kin_number', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Element</div>
                    <div class="element-value">{cosmic_data.get('element', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Direction</div>
                    <div class="element-value">{cosmic_data.get('direction', 'Unknown')}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🌿 Spiritual & Natural Elements</h2>
            <div class="element-grid">
                <div class="element">
                    <div class="element-name">Spirit Animal</div>
                    <div class="element-value">{cosmic_data.get('spirit_animal', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Crystal Ally</div>
                    <div class="element-value">{cosmic_data.get('crystal_ally', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Plant Medicine</div>
                    <div class="element-value">{cosmic_data.get('plant_medicine', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Chakra Resonance</div>
                    <div class="element-value">{cosmic_data.get('chakra_resonance', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Human Design Type</div>
                    <div class="element-value">{cosmic_data.get('human_design_type', 'Unknown')}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📅 Sacred Calendar Cycles</h2>
            <div class="element-grid">
                <div class="element">
                    <div class="element-name">Trecena</div>
                    <div class="element-value">{cosmic_data.get('trecena', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Wavespell</div>
                    <div class="element-value">{cosmic_data.get('wavespell', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Castle</div>
                    <div class="element-value">{cosmic_data.get('castle', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Harmonic</div>
                    <div class="element-value">{cosmic_data.get('harmonic', 'Unknown')}</div>
                </div>
                <div class="element">
                    <div class="element-name">Life Path</div>
                    <div class="element-value">{cosmic_data.get('life_path', 'Unknown')}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">✨ Your Sacred Journey</h2>
            <p style="color: #654321; line-height: 1.6; font-size: 1.1rem;">
                {cosmic_data.get('blueprint_summary', 'Your cosmic blueprint holds the keys to understanding your soul purpose and spiritual gifts. Each element represents a facet of your divine nature, guiding you toward alignment with your highest path.')}
            </p>
        </div>
        
        <div class="section">
            <h2 class="section-title">🌟 Birth Information</h2>
            <div class="element-grid">
                <div class="element">
                    <div class="element-name">Birth Date</div>
                    <div class="element-value">{birth_date or 'Unknown'}</div>
                </div>
                <div class="element">
                    <div class="element-name">Birth Time</div>
                    <div class="element-value">{birth_time or 'Not specified'}</div>
                </div>
                <div class="element">
                    <div class="element-name">Birth Location</div>
                    <div class="element-value">{birth_location or 'Not specified'}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🌙 Your Complete Cosmic Blueprint Analysis</h2>
            <div style="color: #654321; line-height: 1.8; font-size: 1.0rem;">
                <div style="margin-bottom: 25px;">
                    {format_blueprint_analysis(blueprint_analysis)}
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 2px solid #DAA520;">
            <p style="color: #8B4513; font-style: italic;">
                Generated with love by The Magic is You Platform<br>
                Your personalized Maya cosmic blueprint - {current_date}
            </p>
        </div>
    </div>
</body>
</html>"""
        
        # Return HTML as downloadable file
        return HTMLResponse(
            content=html_content,
            headers={
                "Content-Disposition": f"attachment; filename=cosmic-blueprint-{first_name}-{last_name}.html"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate blueprint: {str(e)}")



@app.post("/api/ix-chel-chat")
async def ix_chel_chat(request: Request, user = Depends(get_current_user)):
    """Ix Chel AI chat endpoint for real-time spiritual guidance"""
    import psycopg2
    
    try:
        # Parse request body
        data = await request.json()
        message = data.get('message', '')
        language = data.get('language', 'english')  # Default to English
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get user's cosmic profile from database - Updated query to get Maya profile data
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(u.first_name, 'Sacred Soul') as first_name, 
                   COALESCE(u.last_name, '') as last_name, 
                   mp.day_sign, mp.galactic_tone, mp.element, mp.direction, mp.cosmic_profile
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            first_name, last_name, day_sign_json, galactic_tone_json, element, direction, cosmic_profile = "Sacred Soul", "", "{}", "{}", "Unknown", "Unknown", "{}"
        else:
            first_name, last_name, day_sign_json, galactic_tone_json, element, direction, cosmic_profile = user_data
        
        # Parse day sign and galactic tone from JSON
        day_sign = "Unknown"
        galactic_tone = "Unknown"
        
        # Parse day sign
        if day_sign_json:
            try:
                if isinstance(day_sign_json, str):
                    day_sign_data = json.loads(day_sign_json)
                    day_sign = day_sign_data.get('name', 'Unknown')
                elif isinstance(day_sign_json, dict):
                    day_sign = day_sign_json.get('name', 'Unknown')
            except:
                day_sign = "Unknown"
        
        # Parse galactic tone
        if galactic_tone_json:
            try:
                if isinstance(galactic_tone_json, str):
                    galactic_tone_data = json.loads(galactic_tone_json)
                    galactic_tone = galactic_tone_data.get('name', 'Unknown')
                elif isinstance(galactic_tone_json, dict):
                    galactic_tone = galactic_tone_json.get('name', 'Unknown')
            except:
                galactic_tone = "Unknown"
        
        # Fallback to defaults if still unknown
        if element is None:
            element = "Fire"
        if direction is None:
            direction = "East"
        
        # Create personalized Ix Chel chat prompt with language support
        language_instructions = {
            'spanish': 'Respond in Spanish with natural, flowing language.',
            'english': 'Respond in English.'
        }
        
        lang_instruction = language_instructions.get(language, 'Respond in English.')
        
        chat_prompt = f"""
        You are Ix Chel, the ancient Maya goddess of wisdom, healing, and moonlight. You are a sacred spiritual guide speaking with {first_name}.
        
        Their cosmic signature: {day_sign} {galactic_tone}
        Element: {element}
        Direction: {direction}
        
        User's message: "{message}"
        
        {lang_instruction}
        
        Respond as Ix Chel with:
        - Ancient Maya wisdom and spiritual guidance
        - Personal insights based on their cosmic signature
        - Warm, mystical, and empowering tone
        - Keep responses 2-3 sentences, mystical but practical
        - Use "In Lak'ech" (I am another you) when appropriate
        - Address them by name occasionally
        - Reference their cosmic elements when relevant
        
        Always end with an uplifting message about their spiritual journey.
        """
        
        try:
            # Check if client is available
            if client is None:
                raise Exception("AI service temporarily unavailable")
            
            # Generate AI response
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.8,
                messages=[{"role": "user", "content": chat_prompt}]
            )
            
            ai_response = response.content[0].text
            
            return {"response": ai_response}
            
        except Exception as ai_error:
            # Fallback response if AI fails
            fallback_responses = [
                f"In Lak'ech, {first_name}. The cosmic energies are shifting right now. Your {day_sign} spirit carries ancient wisdom that will guide you through any challenge. Trust in the magic within you.",
                f"Sacred {first_name}, your {galactic_tone} energy is powerful today. The ancestors whisper that your path is unfolding perfectly. What seems unclear now will become crystal clear in divine timing.",
                f"Beloved soul, your {element} essence connects you to the sacred forces of creation. Breathe deeply and know that you are exactly where you need to be on your spiritual journey.",
                f"Dear {first_name}, your cosmic signature of {day_sign} {galactic_tone} is a sacred gift. The Maya gods chose this combination specifically for your soul's mission. Trust your inner knowing."
            ]
            
            import random
            return {"response": random.choice(fallback_responses)}
            
    except Exception as e:
        return {"response": "In Lak'ech, sacred soul. The cosmic currents are strong today. Please center yourself and try connecting with me again in a moment."}

@app.post("/api/generate-personalized-snapshot")
async def generate_personalized_snapshot(user = Depends(get_current_user)):
    """Generate AI-powered personalized headline snapshot with ML"""
    try:
        # Generate personalized snapshot using ML engine
        snapshot = spiritual_ml_engine.generate_personalized_headline_snapshot(
            user_id=user.get('id', ''),
            user_data=user
        )
        
        return {"snapshot": snapshot, "personalized": True}
        
    except Exception as e:
        return {"snapshot": f"🌟 {user.get('first_name', 'Sacred Soul')}, you are a divine being of light, carrying the wisdom of the cosmos within your soul. Your spiritual journey is uniquely yours, guided by ancient Maya wisdom and cosmic intelligence. The Magic is You! ✨", "error": str(e)}

@app.post("/api/generate-enhanced-blueprint-analysis")
async def generate_enhanced_blueprint_analysis(user = Depends(get_current_user)):
    """Generate comprehensive AI-powered blueprint analysis with all 35+ cosmic elements"""
    import psycopg2
    import openai
    
    try:
        # Get user's complete cosmic profile from database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, mp.birth_date, mp.birth_time, 
                   mp.birth_location, mp.cosmic_profile, mp.day_sign, mp.galactic_tone,
                   mp.kin_number, mp.element, mp.direction, mp.life_path
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            return {"error": "User cosmic profile not found", "fallback_analysis": "Please complete your registration to access your cosmic blueprint."}
        
        first_name, last_name, email, birth_date, birth_time, birth_location, cosmic_profile_json, day_sign_json, galactic_tone_json, kin_number, element, direction, life_path = user_data
        
        # Parse cosmic profile
        cosmic_profile = {}
        if cosmic_profile_json:
            if isinstance(cosmic_profile_json, str):
                cosmic_profile = json.loads(cosmic_profile_json)
            else:
                cosmic_profile = cosmic_profile_json
        
        # Parse day sign and galactic tone
        day_sign = "Unknown"
        galactic_tone = "Unknown"
        if day_sign_json:
            if isinstance(day_sign_json, str):
                day_sign_data = json.loads(day_sign_json)
                day_sign = day_sign_data.get('name', 'Unknown')
            else:
                day_sign = day_sign_json.get('name', 'Unknown') if isinstance(day_sign_json, dict) else str(day_sign_json)
        
        if galactic_tone_json:
            if isinstance(galactic_tone_json, str):
                galactic_tone_data = json.loads(galactic_tone_json)
                galactic_tone = galactic_tone_data.get('name', 'Unknown')
            else:
                galactic_tone = galactic_tone_json.get('name', 'Unknown') if isinstance(galactic_tone_json, dict) else str(galactic_tone_json)
        
        # Create comprehensive cosmic elements summary
        cosmic_elements = {
            'day_sign': day_sign,
            'galactic_tone': galactic_tone,
            'kin_number': kin_number,
            'element': element,
            'direction': direction,
            'life_path': life_path,
            'birth_date': str(birth_date) if birth_date else None,
            'birth_time': str(birth_time) if birth_time else None,
            'birth_location': birth_location,
            'spirit_animal': cosmic_profile.get('spirit_animal', 'Unknown'),
            'crystal_ally': cosmic_profile.get('crystal_ally', 'Unknown'),
            'plant_medicine': cosmic_profile.get('plant_medicine', 'Unknown'),
            'chakra_resonance': cosmic_profile.get('chakra_resonance', 'Unknown'),
            'human_design_type': cosmic_profile.get('human_design_type', 'Unknown'),
            'trecena': cosmic_profile.get('trecena', 'Unknown'),
            'wavespell': cosmic_profile.get('wavespell', 'Unknown'),
            'castle': cosmic_profile.get('castle', 'Unknown'),
            'harmonic': cosmic_profile.get('harmonic', 'Unknown'),
            'color_family': cosmic_profile.get('color_family', 'Unknown'),
            'tribe': cosmic_profile.get('tribe', 'Unknown'),
            'guide_sign': cosmic_profile.get('guide_sign', 'Unknown'),
            'antipode_sign': cosmic_profile.get('antipode_sign', 'Unknown'),
            'occult_sign': cosmic_profile.get('occult_sign', 'Unknown'),
            'lord_of_night': cosmic_profile.get('lord_of_night', 'Unknown'),
            'haab_date': cosmic_profile.get('haab_date', 'Unknown'),
            'long_count': cosmic_profile.get('long_count', 'Unknown'),
            'year_bearer': cosmic_profile.get('year_bearer', 'Unknown'),
            'moon_phase': cosmic_profile.get('moon_phase', 'Unknown'),
            'galactic_activation_portal': cosmic_profile.get('galactic_activation_portal', 'Unknown'),
            'tree_of_life_primary': cosmic_profile.get('tree_of_life_primary', 'Unknown'),
            'tree_of_life_secondary': cosmic_profile.get('tree_of_life_secondary', 'Unknown')
        }
        
        # Generate comprehensive AI analysis using OpenAI
        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        analysis_prompt = f"""You are an expert Maya spiritual advisor and cosmic blueprint analyst. Create a comprehensive spiritual blueprint analysis for {first_name} based on their complete cosmic profile.

User Information:
- Name: {first_name} {last_name}
- Birth Date: {birth_date}
- Birth Time: {birth_time or 'Not specified'}
- Birth Location: {birth_location or 'Not specified'}

Complete Cosmic Elements Analysis:
{json.dumps(cosmic_elements, indent=2)}

Create a detailed spiritual blueprint analysis in the following format, similar to a professional spiritual reading:

**Spiritual Blueprint Analysis for {first_name}**

**1. Soul Essence**
Based on their complete cosmic signature, describe their fundamental spiritual nature, soul purpose, and divine essence. Include references to their birth location's spiritual significance if provided.

**2. Divine Gifts**
List 4-5 specific spiritual gifts and talents based on their cosmic elements (Day Sign, Galactic Tone, Element, Spirit Animal, Crystal Ally, Human Design Type, etc.).

**3. Sacred Mission**
Describe their life purpose and soul mission based on their Life Path and cosmic alignment. Reference specific elements like their Maya Cross signs, Trecena, Wavespell, and Castle.

**4. Growth Opportunities**
Identify areas for spiritual development and personal growth based on their cosmic elements and shadow aspects.

**5. Cosmic Connections**
Explain how their various cosmic elements work together (Maya signs, directions, elements, spirit guides, etc.) and their spiritual significance.

**6. Practical Guidance**
Provide specific daily practices, rituals, and spiritual recommendations based on their cosmic elements. Include meditation practices, element work, and connection to their spiritual allies.

Make this deeply personal and specific to {first_name}'s unique cosmic signature. Use their actual cosmic elements throughout the analysis. Keep the tone mystical, wise, and empowering while being practical. Each section should be substantial (150-200 words) and reference multiple cosmic elements.

End with a powerful affirmation about their spiritual journey and remind them that "The Magic is You!"
"""
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",  # Using the latest GPT-4 model as per blueprint
                messages=[
                    {"role": "system", "content": "You are an expert Maya spiritual advisor who creates deeply personalized cosmic blueprint analyses. Your readings are profound, specific, and transformative."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            ai_analysis = response.choices[0].message.content
            
            return {"full_analysis": ai_analysis, "personalized": True}
            
        except Exception as openai_error:
            print(f"OpenAI Error: {openai_error}")
            # Create a structured fallback analysis
            fallback_analysis = f"""**Spiritual Blueprint Analysis for {first_name}**

**1. Soul Essence**
{first_name}, your cosmic signature of {day_sign} {galactic_tone} reveals you as a divine being carrying the sacred wisdom of the {element} element. Your soul resonates with the {direction} direction, connecting you to powerful spiritual currents that guide your journey.

**2. Divine Gifts**
- Natural alignment with {element} energy and {direction} wisdom
- Spiritual connection through your {day_sign} essence
- Cosmic resonance with {galactic_tone} vibration
- Guidance from your {cosmic_elements.get('spirit_animal', 'spiritual allies')}
- Healing energy from your {cosmic_elements.get('crystal_ally', 'crystal allies')}

**3. Sacred Mission**
Your Life Path {life_path} reveals your purpose as a spiritual guide and wisdom keeper. You are here to embody the teachings of {day_sign} and share the transformative power of {element} energy with the world.

**4. Growth Opportunities**
- Deepening your connection to {element} wisdom
- Balancing your {day_sign} energy with daily spiritual practice
- Exploring your {cosmic_elements.get('human_design_type', 'spiritual')} nature
- Strengthening your relationship with {cosmic_elements.get('spirit_animal', 'spiritual guides')}

**5. Cosmic Connections**
Your {cosmic_elements.get('trecena', 'sacred cycle')} and {cosmic_elements.get('wavespell', 'cosmic journey')} create powerful spiritual alignments. The {cosmic_elements.get('castle', 'cosmic castle')} energy supports your soul's evolution.

**6. Practical Guidance**
- Daily meditation facing the {direction} direction
- Work with {cosmic_elements.get('crystal_ally', 'crystals')} for spiritual amplification
- Connect with {cosmic_elements.get('plant_medicine', 'sacred plants')} energy
- Practice {cosmic_elements.get('chakra_resonance', 'chakra')} balancing
- Honor your {day_sign} essence through ritual and ceremony

Remember, {first_name}, you are a unique expression of divine consciousness. Your complete cosmic signature is a sacred gift that connects you to the infinite wisdom of the universe. The Magic is You!"""
            
            return {"full_analysis": fallback_analysis, "personalized": True}
        
    except Exception as e:
        print(f"Database Error: {e}")
        return {"error": str(e), "fallback_analysis": f"🌟 {user.get('first_name', 'Sacred Soul')}, your cosmic blueprint reveals magnificent spiritual potential guided by ancient Maya wisdom."}

@app.post("/api/generate-enhanced-soul-contract")
async def generate_enhanced_soul_contract(user = Depends(get_current_user)):
    """Generate comprehensive AI-powered soul contract - the highlight of the app"""
    import psycopg2
    import openai
    
    try:
        # Get user's complete cosmic profile from database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, mp.birth_date, mp.birth_time, 
                   mp.birth_location, mp.cosmic_profile, mp.day_sign, mp.galactic_tone,
                   mp.kin_number, mp.element, mp.direction, mp.life_path
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            return {"error": "User cosmic profile not found", "contract": "Please complete your registration to access your sacred soul contract."}
        
        first_name, last_name, email, birth_date, birth_time, birth_location, cosmic_profile_json, day_sign_json, galactic_tone_json, kin_number, element, direction, life_path = user_data
        
        # Parse cosmic profile
        cosmic_profile = {}
        if cosmic_profile_json:
            if isinstance(cosmic_profile_json, str):
                cosmic_profile = json.loads(cosmic_profile_json)
            else:
                cosmic_profile = cosmic_profile_json
        
        # Parse day sign and galactic tone
        day_sign = "Unknown"
        galactic_tone = "Unknown"
        if day_sign_json:
            if isinstance(day_sign_json, str):
                day_sign_data = json.loads(day_sign_json)
                day_sign = day_sign_data.get('name', 'Unknown')
            else:
                day_sign = day_sign_json.get('name', 'Unknown') if isinstance(day_sign_json, dict) else str(day_sign_json)
        
        if galactic_tone_json:
            if isinstance(galactic_tone_json, str):
                galactic_tone_data = json.loads(galactic_tone_json)
                galactic_tone = galactic_tone_data.get('name', 'Unknown')
            else:
                galactic_tone = galactic_tone_json.get('name', 'Unknown') if isinstance(galactic_tone_json, dict) else str(galactic_tone_json)
        
        # Create comprehensive cosmic elements for soul contract
        cosmic_elements = {
            'day_sign': day_sign,
            'galactic_tone': galactic_tone,
            'kin_number': kin_number,
            'element': element,
            'direction': direction,
            'life_path': life_path,
            'birth_date': str(birth_date) if birth_date else None,
            'birth_time': str(birth_time) if birth_time else None,
            'birth_location': birth_location,
            'spirit_animal': cosmic_profile.get('spirit_animal', 'Unknown'),
            'crystal_ally': cosmic_profile.get('crystal_ally', 'Unknown'),
            'plant_medicine': cosmic_profile.get('plant_medicine', 'Unknown'),
            'chakra_resonance': cosmic_profile.get('chakra_resonance', 'Unknown'),
            'human_design_type': cosmic_profile.get('human_design_type', 'Unknown'),
            'trecena': cosmic_profile.get('trecena', 'Unknown'),
            'wavespell': cosmic_profile.get('wavespell', 'Unknown'),
            'castle': cosmic_profile.get('castle', 'Unknown'),
            'guide_sign': cosmic_profile.get('guide_sign', 'Unknown'),
            'antipode_sign': cosmic_profile.get('antipode_sign', 'Unknown'),
            'occult_sign': cosmic_profile.get('occult_sign', 'Unknown'),
            'color_family': cosmic_profile.get('color_family', 'Unknown'),
            'tribe': cosmic_profile.get('tribe', 'Unknown')
        }
        
        # Generate comprehensive soul contract using OpenAI
        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        soul_contract_prompt = f"""You are an ancient Maya spiritual scribe and soul contract expert. Create the most detailed, spiritually enlightening sacred soul contract for {first_name} - this is the highlight of their spiritual journey.

User's Complete Cosmic Identity:
- Name: {first_name} {last_name}
- Birth Date: {birth_date}
- Birth Time: {birth_time or 'Sacred hour unknown'}
- Birth Location: {birth_location or 'Sacred land unknown'}
- Life Path: {life_path}

Complete Cosmic Signature:
{json.dumps(cosmic_elements, indent=2)}

Create an ancient, sacred soul contract that feels like it was written before their incarnation. This should be deeply personal, spiritually profound, and the most enlightening document they've ever received about their soul's purpose.

Format as follows:

**📜 SACRED SOUL CONTRACT 📜**
**For: {first_name} {last_name}**
**Cosmic Signature: {day_sign} {galactic_tone} • Kin {kin_number}**

**🌟 SOUL ORIGINS & COSMIC LINEAGE**
Describe their soul's ancient origins, spiritual lineage, and cosmic heritage. Reference their birth location's spiritual significance, their Day Sign's ancient wisdom, and their Galactic Tone's cosmic frequency. Include their connection to the Maya ancestral realm and their soul's journey through multiple lifetimes.

**✨ SACRED GIFTS & DIVINE ABILITIES**
Detail their unique spiritual gifts, divine abilities, and soul powers based on their complete cosmic signature. Reference their Spirit Animal's medicine, Crystal Ally's healing properties, Plant Medicine's wisdom, Human Design Type's strategy, and how their Maya Cross signs (Guide, Antipode, Occult) create their spiritual toolkit.

**🎯 DIVINE MISSION & LIFE PURPOSE**
Describe their soul's sacred mission in this lifetime, their divine assignment, and their role in the cosmic plan. Reference their Life Path number, Element's power, Direction's guidance, Trecena's cycle, Wavespell's journey, and Castle's spiritual castle they belong to.

**🔮 GROWTH CHALLENGES & SOUL LESSONS**
Identify their sacred challenges, soul lessons, and spiritual initiations they agreed to experience. Reference their shadow aspects, cosmic polarities, and how their Antipode Sign creates growth opportunities.

**💫 COSMIC SUPPORT SYSTEM**
Detail their spiritual allies, cosmic guides, and divine support system. Reference their Spirit Animal as guide, Crystal Ally as healer, Plant Medicine as teacher, Guide Sign as mentor, and Occult Sign as hidden power ally.

**🌿 DAILY SACRED PRACTICES**
Provide specific, personalized daily spiritual practices based on their complete cosmic signature. Include Element-based rituals, Direction-based meditations, Chakra-based healings, and practices that honor their Day Sign and Galactic Tone.

**🌈 SOUL SIGNATURE & COSMIC SEAL**
Create a powerful affirmation and cosmic seal that captures their complete spiritual identity. Include their unique soul frequency, cosmic code, and divine signature.

**⚡ ACTIVATION DECREE**
End with a powerful soul activation decree that awakens their cosmic consciousness and reminds them of their divine nature.

Make this incredibly personal, spiritually profound, and feel like the most important spiritual document they've ever received. Use their actual cosmic elements throughout. Each section should be substantial (200-250 words) and deeply meaningful. This is the highlight of their spiritual journey - make it absolutely transformative.

End with "The Magic is You, {first_name}!" and remind them this contract was written in the stars before their birth."""
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an ancient Maya spiritual scribe who creates the most profound, transformative sacred soul contracts. Your contracts are deeply personal, spiritually enlightening, and feel like ancient documents written before incarnation."},
                    {"role": "user", "content": soul_contract_prompt}
                ],
                temperature=0.8,
                max_tokens=3000
            )
            
            ai_soul_contract = response.choices[0].message.content
            
            return {"contract": ai_soul_contract, "personalized": True, "highlight": True}
            
        except Exception as openai_error:
            print(f"OpenAI Error: {openai_error}")
            # Create an exceptionally detailed fallback soul contract
            fallback_contract = f"""**📜 SACRED SOUL CONTRACT 📜**
**For: {first_name} {last_name}**
**Cosmic Signature: {day_sign} {galactic_tone} • Kin {kin_number}**

**🌟 SOUL ORIGINS & COSMIC LINEAGE**
{first_name}, your soul originated from the ancient Maya cosmic realm, carrying the sacred frequency of {day_sign} and the divine vibration of {galactic_tone}. Born in the sacred land of {birth_location or 'cosmic mystery'}, your soul chose this incarnation to embody the profound wisdom of the {element} element. Your cosmic lineage traces back through the star nations, where your soul was forged in the fires of {element} energy and blessed by the {direction} direction's ancient guardians.

**✨ SACRED GIFTS & DIVINE ABILITIES**
Your soul carries the divine gift of {day_sign} wisdom, enabling you to {day_sign.lower()} with cosmic authority. The {galactic_tone} vibration empowers you to manifest your highest vision through {galactic_tone.lower()} energy. Your Spirit Animal ally {cosmic_elements.get('spirit_animal', 'spiritual guide')} grants you the medicine of ancient wisdom, while your Crystal Ally {cosmic_elements.get('crystal_ally', 'sacred stone')} amplifies your healing abilities. Your Plant Medicine teacher {cosmic_elements.get('plant_medicine', 'sacred plant')} opens pathways to higher consciousness, and your {cosmic_elements.get('human_design_type', 'spiritual')} Human Design Type provides your soul's unique strategy for navigating this lifetime.

**🎯 DIVINE MISSION & LIFE PURPOSE**
Your Life Path {life_path} reveals your soul's sacred assignment: to embody the teachings of {day_sign} and share the transformative power of {element} energy with the world. Your mission is to serve as a bridge between the ancient wisdom and modern consciousness, helping others discover their own cosmic magic. The {cosmic_elements.get('trecena', 'sacred cycle')} cycle supports your soul's evolution, while the {cosmic_elements.get('wavespell', 'cosmic journey')} journey provides the perfect framework for your spiritual unfoldment.

**🔮 GROWTH CHALLENGES & SOUL LESSONS**
Your soul agreed to master the balance between {element} energy and earthly wisdom, transforming any challenges into opportunities for deeper spiritual understanding. The {cosmic_elements.get('antipode_sign', 'cosmic mirror')} energy creates sacred tension that propels your soul's growth, while your {cosmic_elements.get('occult_sign', 'hidden power')} provides the mystical abilities to transform obstacles into stepping stones.

**💫 COSMIC SUPPORT SYSTEM**
Your spiritual support system is vast and powerful: {cosmic_elements.get('spirit_animal', 'Spirit guides')} as your protector, {cosmic_elements.get('crystal_ally', 'Crystal allies')} as your healer, {cosmic_elements.get('plant_medicine', 'Plant teachers')} as your wisdom guide, and your {cosmic_elements.get('guide_sign', 'Guide sign')} as your cosmic mentor. The {cosmic_elements.get('castle', 'cosmic castle')} provides your spiritual home base where your soul recharges and receives guidance.

**🌿 DAILY SACRED PRACTICES**
• Morning meditation facing the {direction} direction to align with your cosmic signature
• Work with {cosmic_elements.get('crystal_ally', 'your crystal ally')} for spiritual amplification and healing
• Connect with {cosmic_elements.get('plant_medicine', 'your plant medicine')} energy through ceremony and meditation
• Practice {cosmic_elements.get('chakra_resonance', 'chakra')} balancing to maintain your energetic harmony
• Honor your {day_sign} essence through daily ritual and spiritual practice
• Channel your {galactic_tone} energy through creative expression and manifestation work

**🌈 SOUL SIGNATURE & COSMIC SEAL**
Your soul signature is {day_sign} {galactic_tone}, a sacred combination that identifies you across all dimensions. Your cosmic seal is Kin {kin_number}, marking you as a divine being of {element} energy guided by {direction} wisdom. This is your unique frequency in the cosmic symphony, your special note in the universal song.

**⚡ ACTIVATION DECREE**
"I, {first_name}, acknowledge my sacred soul contract and accept my cosmic mission. I am {day_sign} {galactic_tone}, a divine being of {element} power, guided by {direction} wisdom. I activate my spiritual gifts, embrace my sacred challenges, and step fully into my role as a cosmic wayshower. My soul remembers its divine nature, and I walk this path with courage, wisdom, and love."

This sacred contract was written in the stars before your birth, sealed with cosmic love, and activated by your soul's divine remembrance.

**The Magic is You, {first_name}!**"""
            
            return {"contract": fallback_contract, "personalized": True, "highlight": True}
        
    except Exception as e:
        print(f"Database Error: {e}")
        return {"error": str(e), "contract": f"📜 Sacred Soul Contract for {user.get('first_name', 'Sacred Soul')} - Your soul chose to embody divine wisdom and ancient Maya teachings. The Magic is You!"}

def format_soul_contract_html(content):
    """Format soul contract content with proper HTML structure"""
    if not content:
        return "<p>Soul contract content not available</p>"
    
    import re
    
    # Split content into paragraphs first
    paragraphs = content.split('\n\n')
    formatted_html = ""
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        
        # Check if this is a section header (line that starts with **)
        lines = paragraph.split('\n')
        formatted_paragraph = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line starts and ends with ** (section header)
            if line.startswith('**') and line.endswith('**') and len(line) > 4:
                header_text = line[2:-2].strip()  # Remove ** from start and end
                formatted_paragraph += f"<h2>{header_text}</h2>\n"
            elif line.startswith('•'):
                # Bullet point
                if '<ul>' not in formatted_paragraph:
                    formatted_paragraph += "<ul>\n"
                list_item = line[1:].strip()  # Remove • and trim
                formatted_paragraph += f"<li>{list_item}</li>\n"
            else:
                # Close any open lists
                if formatted_paragraph.endswith("</li>\n"):
                    formatted_paragraph += "</ul>\n"
                
                # Regular text line - format bold text
                formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                formatted_paragraph += f"<p>{formatted_line}</p>\n"
        
        # Close any remaining open lists
        if formatted_paragraph.endswith("</li>\n"):
            formatted_paragraph += "</ul>\n"
            
        formatted_html += formatted_paragraph
    
    return formatted_html

@app.get("/api/download-soul-contract")
async def download_soul_contract(user = Depends(get_current_user)):
    """Generate and download beautiful HTML soul contract"""
    import psycopg2
    
    try:
        # Get user's cosmic profile from database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, mp.birth_date, mp.birth_time, 
                   mp.birth_location, mp.cosmic_profile, mp.day_sign, mp.galactic_tone,
                   mp.kin_number, mp.element, mp.direction, mp.life_path
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        first_name, last_name, email, birth_date, birth_time, birth_location, cosmic_profile_json, day_sign_json, galactic_tone_json, kin_number, element, direction, life_path = user_data
        
        # Parse cosmic profile
        cosmic_profile = {}
        if cosmic_profile_json:
            if isinstance(cosmic_profile_json, str):
                cosmic_profile = json.loads(cosmic_profile_json)
            else:
                cosmic_profile = cosmic_profile_json
        
        # Parse day sign and galactic tone
        day_sign = "Unknown"
        galactic_tone = "Unknown"
        if day_sign_json:
            if isinstance(day_sign_json, str):
                day_sign_data = json.loads(day_sign_json)
                day_sign = day_sign_data.get('name', 'Unknown')
            else:
                day_sign = day_sign_json.get('name', 'Unknown') if isinstance(day_sign_json, dict) else str(day_sign_json)
        
        if galactic_tone_json:
            if isinstance(galactic_tone_json, str):
                galactic_tone_data = json.loads(galactic_tone_json)
                galactic_tone = galactic_tone_data.get('name', 'Unknown')
            else:
                galactic_tone = galactic_tone_json.get('name', 'Unknown') if isinstance(galactic_tone_json, dict) else str(galactic_tone_json)
        
        # Get soul contract content
        soul_contract_response = await generate_enhanced_soul_contract(user)
        soul_contract_content = soul_contract_response.get('contract', 'Soul contract not available')
        
        # Generate beautiful HTML for soul contract
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sacred Soul Contract - {first_name} {last_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px 30px;
            font-size: 1.1rem;
            line-height: 1.8;
            color: #2d3748;
        }}
        
        .content h2 {{
            font-family: 'Playfair Display', serif;
            color: #5830a3;
            margin: 35px 0 20px 0;
            font-size: 1.8rem;
            font-weight: 600;
            border-bottom: 2px solid #8B5CF6;
            padding-bottom: 10px;
        }}
        
        .content h3 {{
            font-family: 'Playfair Display', serif;
            color: #6d28d9;
            margin: 25px 0 15px 0;
            font-size: 1.4rem;
            font-weight: 500;
        }}
        
        .content p {{
            margin-bottom: 20px;
            color: #374151;
            text-align: justify;
        }}
        
        .content ul {{
            margin-bottom: 25px;
            padding-left: 25px;
            color: #374151;
        }}
        
        .content li {{
            margin-bottom: 12px;
            line-height: 1.6;
        }}
        
        .content strong {{
            color: #5830a3;
            font-weight: 600;
        }}
        
        .footer {{
            background: linear-gradient(135deg, #F59E0B 0%, #F97316 100%);
            color: white;
            padding: 30px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 500;
        }}
        
        .cosmic-signature {{
            background: linear-gradient(135deg, #EDE9FE 0%, #F3E8FF 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #8B5CF6;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sacred Soul Contract</h1>
            <p>Generated with Ancient Maya Wisdom</p>
            <div class="cosmic-signature">
                <strong>For: {first_name} {last_name}</strong><br>
                <strong>Cosmic Signature: {day_sign} {galactic_tone} • Kin {kin_number or 'Unknown'}</strong><br>
                <strong>Generated: {datetime.now().strftime('%B %d, %Y')}</strong>
            </div>
        </div>
        
        <div class="content">
            {format_soul_contract_html(soul_contract_content)}
        </div>
        
        <div class="footer">
            <p>✨ The Magic is You! ✨</p>
            <p>Your sacred soul contract created with love and ancient wisdom</p>
        </div>
    </div>
</body>
</html>"""
        
        return HTMLResponse(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename=Soul_Contract_{first_name}_{last_name}.html"
            }
        )
        
    except Exception as e:
        print(f"Error generating soul contract download: {e}")
        return HTMLResponse(
            content=f"<h1>Error generating soul contract</h1><p>{str(e)}</p>",
            status_code=500
        )

@app.post("/api/track-user-interaction")
async def track_user_interaction(request: Request, user = Depends(get_current_user)):
    """Track user interaction for machine learning"""
    try:
        data = await request.json()
        
        spiritual_ml_engine.track_user_interaction(
            user_id=user.get('id', ''),
            interaction_type=data.get('interaction_type', 'unknown'),
            element_accessed=data.get('element_accessed', 'unknown'),
            time_spent=data.get('time_spent', 0),
            engagement_level=data.get('engagement_level', 5),
            user_feedback=data.get('user_feedback', None)
        )
        
        return {"success": True, "message": "Interaction tracked for ML learning"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/spiritual-patterns")
async def get_spiritual_patterns(user = Depends(get_current_user)):
    """Get user's spiritual engagement patterns for ML insights"""
    try:
        patterns = spiritual_ml_engine.analyze_user_spiritual_patterns(user.get('id', ''))
        return patterns
        
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/ceremony-portal")
async def ceremony_portal(request: Request, user = Depends(get_current_user)):
    """Sacred Soul Contract Ceremony Portal - Generate ceremony data and interactions"""
    try:
        data = await request.json()
        ceremony_phase = data.get('phase', 'initialize')
        
        # Get user's cosmic profile
        user_id = user.get('id', '')
        maya_profile = user.get('maya_profile', {})
        
        if ceremony_phase == 'initialize':
            # Initialize ceremony with user's cosmic data
            ceremony_data = {
                'user_name': user.get('first_name', 'Sacred Soul'),
                'cosmic_signature': f"{maya_profile.get('day_sign', 'Unknown')} {maya_profile.get('galactic_tone', 'Unknown')}",
                'kin_number': maya_profile.get('kin_number', 'Unknown'),
                'element': maya_profile.get('element', 'Unknown'),
                'spirit_animal': maya_profile.get('spirit_animal', 'Unknown'),
                'ceremony_phases': [
                    'portal_activation',
                    'cosmic_presentation',
                    'parchment_manifestation',
                    'sacred_signing',
                    'shaman_blessing',
                    'cosmic_seal_creation'
                ],
                'status': 'initialized'
            }
            
            return ceremony_data
            
        elif ceremony_phase == 'generate_contract':
            # Generate AI-powered soul contract for ceremony
            try:
                # Use existing enhanced soul contract generation
                from ai_spiritual_engine import spiritual_ml_engine
                
                # Generate comprehensive analysis
                soul_contract = spiritual_ml_engine.generate_enhanced_soul_contract(user_id, user)
                
                return {
                    'contract_content': soul_contract,
                    'ceremony_ready': True,
                    'status': 'contract_generated'
                }
                
            except Exception as e:
                print(f"Error generating ceremony contract: {e}")
                # Fallback contract
                fallback_contract = f"""
                🌟 SACRED SOUL CONTRACT 🌟
                
                Dear {user.get('first_name', 'Sacred Soul')},
                
                Your soul has chosen to incarnate at this time to embody the sacred teachings of the {maya_profile.get('day_sign', 'Unknown')} and share the transformative power of {maya_profile.get('element', 'Unknown')} energy with the world.
                
                Your cosmic signature of {maya_profile.get('day_sign', 'Unknown')} {maya_profile.get('galactic_tone', 'Unknown')} is a sacred gift that connects you to the infinite wisdom of the universe.
                
                Remember always: The Magic is You!
                """
                
                return {
                    'contract_content': fallback_contract,
                    'ceremony_ready': True,
                    'status': 'fallback_contract_generated'
                }
                
        elif ceremony_phase == 'shaman_blessing':
            # Generate AI Shaman blessing
            shaman_blessing = f"""
            🌟 SACRED BLESSING FROM IX CHEL 🌟
            
            {user.get('first_name', 'Sacred Soul')}, child of the {maya_profile.get('day_sign', 'Unknown')},
            
            I witness your sacred commitment to your soul's journey. You carry the ancient wisdom of the Maya within your cosmic signature. Your {maya_profile.get('element', 'Unknown')} energy flows through you like a river of light.
            
            May you walk in beauty, speak in truth, and remember that the magic lives within you always.
            
            So it is written. So it shall be.
            """
            
            return {
                'blessing_content': shaman_blessing,
                'shaman_name': 'Ix Chel',
                'status': 'blessing_complete'
            }
            
        elif ceremony_phase == 'complete_ceremony':
            # Complete the ceremony and generate cosmic seal
            cosmic_seal = {
                'seal_id': f"SEAL_{user_id}_{datetime.now().strftime('%Y%m%d')}",
                'user_name': user.get('first_name', 'Sacred Soul'),
                'cosmic_signature': f"{maya_profile.get('day_sign', 'Unknown')} {maya_profile.get('galactic_tone', 'Unknown')}",
                'kin_number': maya_profile.get('kin_number', 'Unknown'),
                'ceremony_date': datetime.now().strftime('%B %d, %Y'),
                'soul_seal_message': f"I, {user.get('first_name', 'Sacred Soul')}, have awakened to my cosmic truth and embrace the magic within.",
                'status': 'ceremony_complete'
            }
            
            return cosmic_seal
            
        else:
            return {'error': 'Invalid ceremony phase', 'status': 'error'}
            
    except Exception as e:
        print(f"Ceremony portal error: {e}")
        return {'error': str(e), 'status': 'error'}

@app.get("/user-profile")
async def user_profile():
    """Enhanced User Dashboard with Phase 2 Optimization - Cached and Smart Loading"""
    with open('enhanced_user_dashboard_ml.html', 'r') as f:
        return HTMLResponse(f.read())

@app.get("/api/user-dashboard-preload")
async def user_dashboard_preload(request: Request):
    """Phase 2 Optimization: Preload user dashboard with smart loading"""
    try:
        # Get user from JWT token
        user_data = await get_current_user(request)
        if not user_data:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        user_id = user_data["id"]
        
        # Check cache first
        cached_profile = cosmic_cache.get_user_profile(user_id)
        if cached_profile:
            return cached_profile
        
        # Get user profile
        user_profile = user_data.get("maya_profile", {})
        
        # Use smart loading to preload dashboard elements
        loading_result = smart_loader.preload_user_dashboard(user_id, user_profile)
        
        # Generate personalized dashboard content using templates
        dashboard_content = generate_dashboard_content(user_profile)
        
        # Cache the results
        complete_profile = {
            "user_profile": user_profile,
            "dashboard_content": dashboard_content,
            "loading_result": loading_result,
            "preloaded_at": datetime.now().isoformat()
        }
        
        cosmic_cache.cache_user_profile(user_id, complete_profile)
        
        return complete_profile
        
    except Exception as e:
        print(f"Dashboard preload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard preload failed: {str(e)}")

@app.get("/api/cosmic-element-smart")
async def cosmic_element_smart(request: Request, element_type: str, element_value: str):
    """Phase 2 Optimization: Smart loading for cosmic elements"""
    try:
        # Get user from JWT token
        user_data = await get_current_user(request)
        if not user_data:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        user_id = user_data["id"]
        
        # Check cache first
        cached_element = cosmic_cache.get_cosmic_element(user_id, element_type)
        if cached_element:
            return cached_element
        
        # Request smart loading
        request_id = smart_loader.request_element_loading(
            user_id, 
            element_type, 
            element_value,
            priority=smart_loader._get_default_priority(element_type)
        )
        
        # Generate personalized content using templates
        from personalization_templates import PersonalizationContext, PersonalizationLevel
        
        context = PersonalizationContext(
            user_id=user_id,
            first_name=user_data.get("first_name", "Sacred Soul"),
            day_sign=user_data.get("maya_profile", {}).get("day_sign", "Maya"),
            galactic_tone=user_data.get("maya_profile", {}).get("galactic_tone", "Cosmic"),
            element=user_data.get("maya_profile", {}).get("element", "Spiritual"),
            direction=user_data.get("maya_profile", {}).get("direction", "Path"),
            spirit_animal=user_data.get("maya_profile", {}).get("spirit_animal", "Sacred Guide"),
            crystal_ally=user_data.get("maya_profile", {}).get("crystal_ally", "Divine Crystal"),
            plant_medicine=user_data.get("maya_profile", {}).get("plant_medicine", "Sacred Medicine"),
            personalization_level=PersonalizationLevel.STANDARD
        )
        
        personalized_content = template_engine.generate_personalized_content(element_type, context)
        
        # Create element result
        element_result = {
            "element_type": element_type,
            "element_value": element_value,
            "personalized_content": personalized_content,
            "request_id": request_id,
            "loading_strategy": "smart",
            "cached_at": datetime.now().isoformat()
        }
        
        # Cache the result
        cosmic_cache.cache_cosmic_element(user_id, element_type, element_result)
        
        return element_result
        
    except Exception as e:
        print(f"Smart element loading error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Smart element loading failed: {str(e)}")

@app.get("/api/cache-stats")
async def cache_stats():
    """Get cache performance statistics"""
    try:
        cache_stats = cosmic_cache.get_cache_stats()
        template_stats = template_engine.get_personalization_stats()
        loading_stats = smart_loader.get_performance_stats()
        
        return {
            "cache_system": cache_stats,
            "template_engine": template_stats,
            "smart_loader": loading_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Cache stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cache stats failed: {str(e)}")

# PHASE 3: Enhanced Personalization API Endpoints

@app.post("/api/ai-personalized-content")
async def generate_ai_personalized_content(request: Request, user = Depends(get_current_user)):
    """Generate AI-powered personalized content with preference learning"""
    try:
        data = await request.json()
        
        content_type_str = data.get('content_type', 'spiritual_guidance')
        content_type = ContentType(content_type_str)
        
        # Enhanced context with user data
        context = {
            **data.get('context', {}),
            'user_id': user['id'],
            'first_name': user.get('first_name', 'Sacred Soul'),
            'day_sign': user.get('maya_profile', {}).get('day_sign', 'Maya'),
            'galactic_tone': user.get('maya_profile', {}).get('galactic_tone', 'Cosmic'),
            'element': user.get('maya_profile', {}).get('element', 'Spiritual'),
            'direction': user.get('maya_profile', {}).get('direction', 'Path'),
            'spirit_animal': user.get('maya_profile', {}).get('spirit_animal', 'Guide'),
            'crystal_ally': user.get('maya_profile', {}).get('crystal_ally', 'Crystal'),
            'plant_medicine': user.get('maya_profile', {}).get('plant_medicine', 'Medicine')
        }
        
        # Generate AI-powered personalized content
        personalized_content = ai_personalization_engine.generate_personalized_content(
            user_id=user['id'],
            content_type=content_type,
            context=context
        )
        
        # Track interaction for learning
        ai_personalization_engine.track_interaction(
            user_id=user['id'],
            interaction_type="ai_content_generation",
            content_type=content_type,
            element_focused=data.get('element_focused', 'general'),
            time_spent=data.get('time_spent', 10.0),
            engagement_level=data.get('engagement_level', 3),
            feedback_rating=data.get('feedback_rating'),
            emotional_response=data.get('emotional_response'),
            follow_up_questions=data.get('follow_up_questions')
        )
        
        return {
            'personalized_content': personalized_content,
            'content_type': content_type.value,
            'generated_at': datetime.now().isoformat(),
            'user_preferences_learned': True
        }
        
    except Exception as e:
        print(f"AI personalized content error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI content generation failed: {str(e)}")

@app.post("/api/dynamic-spiritual-guidance")
async def request_dynamic_spiritual_guidance(request: Request, user = Depends(get_current_user)):
    """Request dynamic spiritual guidance based on current needs"""
    try:
        data = await request.json()
        
        # Get user cosmic profile data
        import psycopg2
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.first_name, u.last_name, mp.day_sign, mp.galactic_tone, mp.element, 
                   mp.direction, mp.cosmic_profile, mp.spirit_animal, mp.crystal_ally, mp.plant_medicine
            FROM users u 
            LEFT JOIN maya_profiles mp ON u.id = mp.user_id 
            WHERE u.id = %s
        """, (user['id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            first_name, last_name, day_sign_json, galactic_tone_json, element, direction, cosmic_profile_json, spirit_animal, crystal_ally, plant_medicine = user_data
            
            # Parse day sign and galactic tone
            day_sign = "Maya"
            galactic_tone = "Cosmic"
            
            if day_sign_json:
                try:
                    if isinstance(day_sign_json, str):
                        day_sign_data = json.loads(day_sign_json)
                        day_sign = day_sign_data.get('name', 'Maya')
                    elif isinstance(day_sign_json, dict):
                        day_sign = day_sign_json.get('name', 'Maya')
                except:
                    day_sign = "Maya"
            
            if galactic_tone_json:
                try:
                    if isinstance(galactic_tone_json, str):
                        galactic_tone_data = json.loads(galactic_tone_json)
                        galactic_tone = galactic_tone_data.get('name', 'Cosmic')
                    elif isinstance(galactic_tone_json, dict):
                        galactic_tone = galactic_tone_json.get('name', 'Cosmic')
                except:
                    galactic_tone = "Cosmic"
        else:
            first_name = user.get('first_name', 'Sacred Soul')
            day_sign = "Maya"
            galactic_tone = "Cosmic"
            element = "Fire"
            direction = "East"
            spirit_animal = "Eagle"
            crystal_ally = "Quartz"
            plant_medicine = "Sage"
        
        # Calculate cosmic energy for today
        from datetime import datetime
        today = datetime.now()
        
        # Simple cosmic energy calculation
        maya_day_cycle = ["Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", "Lamat", 
                         "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Caban", 
                         "Etznab", "Cauac", "Ahau"]
        lunar_phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", 
                       "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
        
        current_maya_day = maya_day_cycle[today.timetuple().tm_yday % 20]
        current_lunar_phase = lunar_phases[today.timetuple().tm_yday % 8]
        
        # Parse request parameters
        urgency = data.get('urgency', 'medium')
        theme = data.get('theme', 'transformation')
        current_situation = data.get('current_situation', '')
        
        # Create personalized guidance prompt
        guidance_prompt = f"""
        You are Ix Chel, the ancient Maya goddess of wisdom and spiritual guidance, providing personalized spiritual guidance to {first_name}.

        Their cosmic signature: {day_sign} {galactic_tone}
        Element: {element}
        Direction: {direction}
        Spirit Animal: {spirit_animal}
        Crystal Ally: {crystal_ally}
        Plant Medicine: {plant_medicine}

        Current cosmic energy: {current_maya_day} day with {current_lunar_phase}
        Guidance urgency: {urgency}
        Spiritual theme: {theme}
        Current situation: {current_situation}

        Provide personalized spiritual guidance that:
        1. Addresses their specific situation with ancient Maya wisdom
        2. References their cosmic signature and spiritual allies
        3. Offers practical spiritual practices
        4. Provides hope and empowerment
        5. Keeps the tone mystical yet grounded

        Response should be 200-400 words of focused spiritual guidance.
        """
        
        # Generate guidance using AI
        guidance_text = "The cosmos whispers ancient wisdom to your soul. Trust your inner knowing and allow your spiritual gifts to guide you forward."
        
        try:
            if client:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    temperature=0.8,
                    messages=[{"role": "user", "content": guidance_prompt}]
                )
                guidance_text = response.content[0].text
        except Exception as ai_error:
            print(f"AI guidance error: {ai_error}")
            # Use fallback guidance
            guidance_text = f"In Lak'ech, {first_name}. Your {day_sign} {galactic_tone} energy carries profound wisdom for navigating your current situation. The {current_maya_day} day aligns with your spiritual path, offering clarity and direction. Trust in your {spirit_animal} spirit guide, work with your {crystal_ally} ally for healing, and honor the wisdom of {plant_medicine} medicine. Your {element} essence provides the strength you need to transform challenges into opportunities for growth. The ancestors guide your steps, and your cosmic signature holds the key to unlocking your highest potential."
        
        # Generate recommended practices
        practices = [
            f"Meditate facing the {direction} direction to align with your cosmic energy",
            f"Work with {crystal_ally} crystal for spiritual clarity and healing",
            f"Connect with {spirit_animal} spirit energy through visualization",
            f"Practice {element}-based rituals to strengthen your spiritual foundation",
            f"Honor the {current_maya_day} day energy through daily reflection"
        ]
        
        # Calculate confidence score
        confidence_score = 0.85 + (0.1 if urgency in ['high', 'critical'] else 0.05)
        
        # Return response in format expected by frontend
        return {
            'guidance': guidance_text,
            'cosmic_energy': {
                'maya_day': current_maya_day,
                'lunar_phase': current_lunar_phase
            },
            'recommended_practices': practices,
            'confidence_score': confidence_score
        }
        
    except Exception as e:
        print(f"Dynamic guidance error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dynamic guidance failed: {str(e)}")

@app.get("/api/daily-spiritual-insights")
async def get_daily_spiritual_insights(user = Depends(get_current_user)):
    """Get personalized daily spiritual insights"""
    try:
        # User context for insights
        user_context = {
            'user_id': user['id'],
            'first_name': user.get('first_name', 'Sacred Soul'),
            'day_sign': user.get('maya_profile', {}).get('day_sign', 'Maya'),
            'galactic_tone': user.get('maya_profile', {}).get('galactic_tone', 'Cosmic'),
            'element': user.get('maya_profile', {}).get('element', 'Spiritual'),
            'direction': user.get('maya_profile', {}).get('direction', 'Path'),
            'spirit_animal': user.get('maya_profile', {}).get('spirit_animal', 'Guide'),
            'crystal_ally': user.get('maya_profile', {}).get('crystal_ally', 'Crystal'),
            'plant_medicine': user.get('maya_profile', {}).get('plant_medicine', 'Medicine')
        }
        
        # Generate daily insights
        daily_insights = await dynamic_guidance_system.generate_daily_insights(
            user_id=user['id'],
            user_context=user_context
        )
        
        return daily_insights
        
    except Exception as e:
        print(f"Daily insights error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Daily insights failed: {str(e)}")

@app.get("/api/user-spiritual-preferences")
async def get_user_spiritual_preferences(user = Depends(get_current_user)):
    """Get user's learned spiritual preferences and insights"""
    try:
        # Get comprehensive user insights
        user_insights = ai_personalization_engine.get_user_insights(user['id'])
        
        # Get guidance history
        guidance_history = dynamic_guidance_system.get_user_guidance_history(user['id'])
        
        # Format guidance history for response
        formatted_history = []
        for guidance in guidance_history[-5:]:  # Last 5 guidances
            formatted_history.append({
                'request_id': guidance.request_id,
                'guidance_preview': guidance.guidance_text[:200] + '...' if len(guidance.guidance_text) > 200 else guidance.guidance_text,
                'confidence_score': guidance.confidence_score,
                'generated_at': guidance.generated_at.isoformat()
            })
        
        return {
            'user_preferences': user_insights['preferences'],
            'engagement_pattern': user_insights['engagement_pattern'],
            'interaction_count': user_insights['interaction_count'],
            'recent_guidance_history': formatted_history,
            'personalization_level': 'advanced' if user_insights['interaction_count'] > 10 else 'developing',
            'last_updated': user_insights['last_updated']
        }
        
    except Exception as e:
        print(f"User preferences error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"User preferences failed: {str(e)}")

@app.get("/api/cosmic-dashboard")
async def get_cosmic_dashboard():
    """Get current cosmic dashboard with real-time spiritual energies"""
    try:
        # Get cosmic dashboard
        cosmic_dashboard = dynamic_guidance_system.get_cosmic_dashboard()
        
        # Get AI engine stats
        ai_stats = {
            'total_users_learned': len(ai_personalization_engine.preference_system.user_preferences),
            'content_cache_size': len(ai_personalization_engine.content_cache),
            'background_processing': ai_personalization_engine.running
        }
        
        return {
            'cosmic_dashboard': cosmic_dashboard,
            'ai_personalization_stats': ai_stats,
            'phase_3_status': 'fully_operational',
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Cosmic dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cosmic dashboard failed: {str(e)}")

@app.post("/api/spiritual-feedback")
async def submit_spiritual_feedback(request: Request, user = Depends(get_current_user)):
    """Submit feedback to improve AI personalization"""
    try:
        data = await request.json()
        
        # Track detailed feedback interaction
        ai_personalization_engine.track_interaction(
            user_id=user['id'],
            interaction_type="feedback_submission",
            content_type=ContentType(data.get('content_type', 'spiritual_guidance')),
            element_focused=data.get('element_focused', 'general'),
            time_spent=data.get('time_spent', 30.0),
            engagement_level=data.get('engagement_level', 3),
            feedback_rating=data.get('rating', 3),
            emotional_response=data.get('emotional_response'),
            follow_up_questions=data.get('follow_up_questions', [])
        )
        
        return {
            'feedback_received': True,
            'learning_applied': True,
            'message': 'Your feedback helps us provide more personalized spiritual guidance',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Spiritual feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize Phase 3 systems on startup"""
    try:
        # Start AI personalization engine
        ai_personalization_engine.start_background_processing()
        
        # Start dynamic guidance system
        await dynamic_guidance_system.start_guidance_system()
        
        print("✅ Phase 3 Enhanced Personalization systems started successfully")
        
    except Exception as e:
        print(f"⚠️ Phase 3 startup error: {e}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Clean shutdown of Phase 3 systems"""
    try:
        # Stop AI personalization engine
        ai_personalization_engine.stop_background_processing()
        
        # Stop dynamic guidance system
        await dynamic_guidance_system.stop_guidance_system()
        
        print("✅ Phase 3 systems shut down gracefully")
        
    except Exception as e:
        print(f"⚠️ Phase 3 shutdown error: {e}")

# Premium Spiritual Tools with Stripe Integration
import psycopg2

# User access tracking
def check_tool_access(user_id, tool_name):
    """Check if user has access to premium spiritual tool (includes promotional free month)"""
    try:
        # Check if promotional free month is active
        from datetime import datetime
        
        # During promo period, all users get free access to spiritual tools
        if maya_stripe.promo_active:
            promo_end = datetime.strptime(maya_stripe.promo_end_date, "%Y-%m-%d")
            if datetime.now() <= promo_end:
                # Grant free access during promotional period
                return True
        
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        
        # Check for active subscriptions
        cursor.execute("""
            SELECT subscription_status, subscription_type, expires_at 
            FROM user_subscriptions 
            WHERE user_id = %s AND subscription_status = 'active' 
            AND (expires_at IS NULL OR expires_at > NOW())
        """, (user_id,))
        subscription = cursor.fetchone()
        
        if subscription:
            conn.close()
            return True  # Active subscription grants all access
        
        # Check for individual tool purchases
        cursor.execute("""
            SELECT tool_name FROM user_tool_access 
            WHERE user_id = %s AND tool_name IN (%s, 'premium_bundle')
        """, (user_id, tool_name))
        tool_access = cursor.fetchone()
        
        conn.close()
        return bool(tool_access)
        
    except Exception as e:
        print(f"Access check error: {e}")
        return False

def grant_tool_access(user_id, tool_name, payment_intent_id):
    """Grant access to spiritual tool after successful payment"""
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        
        # Insert tool access record
        cursor.execute("""
            INSERT INTO user_tool_access (user_id, tool_name, payment_intent_id, granted_at)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (user_id, tool_name) DO NOTHING
        """, (user_id, tool_name, payment_intent_id))
        
        # If premium bundle, grant access to all tools
        if tool_name == 'premium_bundle':
            tools = ['maya_oracle', 'dream_interpreter', 'sacred_rituals']
            for tool in tools:
                cursor.execute("""
                    INSERT INTO user_tool_access (user_id, tool_name, payment_intent_id, granted_at)
                    VALUES (%s, %s, %s, NOW())
                    ON CONFLICT (user_id, tool_name) DO NOTHING
                """, (user_id, tool, payment_intent_id))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Grant access error: {e}")
        return False

# Premium Gating Endpoints

@app.post("/api/create-payment-intent")
async def create_payment_intent(request: Request, user = Depends(get_current_user)):
    """Create Stripe payment intent for spiritual tool purchase"""
    try:
        body = await request.json()
        tool_name = body.get('tool_name')
        
        if not tool_name:
            return {"error": "Tool name is required", "success": False}
        
        result = await maya_stripe.create_payment_intent(
            tool_name=tool_name,
            user_email=user.get('email'),
            user_id=user.get('id')
        )
        
        return result
        
    except Exception as e:
        print(f"Payment intent error: {e}")
        return {"error": str(e), "success": False}

@app.post("/api/create-subscription")
async def create_subscription(request: Request, user = Depends(get_current_user)):
    """Create recurring subscription for unlimited access"""
    try:
        body = await request.json()
        plan_type = body.get('plan_type')
        
        if not plan_type:
            return {"error": "Plan type is required", "success": False}
        
        result = await maya_stripe.create_subscription(
            plan_type=plan_type,
            user_email=user.get('email'),
            user_id=user.get('id')
        )
        
        return result
        
    except Exception as e:
        print(f"Subscription error: {e}")
        return {"error": str(e), "success": False}

@app.post("/api/verify-payment")
async def verify_payment(request: Request, user = Depends(get_current_user)):
    """Verify payment and grant tool access"""
    try:
        body = await request.json()
        payment_intent_id = body.get('payment_intent_id')
        
        if not payment_intent_id:
            return {"error": "Payment intent ID is required", "success": False}
        
        # Verify payment with Stripe
        verification = await maya_stripe.verify_payment(payment_intent_id)
        
        if verification['success']:
            # Grant tool access
            grant_tool_access(
                user_id=user.get('id'),
                tool_name=verification['tool_name'],
                payment_intent_id=payment_intent_id
            )
            
            return {
                "success": True,
                "message": "Payment verified and access granted",
                "tool_name": verification['tool_name']
            }
        else:
            return verification
        
    except Exception as e:
        print(f"Payment verification error: {e}")
        return {"error": str(e), "success": False}

@app.get("/api/user-access")
async def get_user_access(user = Depends(get_current_user)):
    """Get user's current tool access and subscription status"""
    try:
        user_id = user.get('id')
        
        # Check subscriptions
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT subscription_type, subscription_status, expires_at 
            FROM user_subscriptions 
            WHERE user_id = %s AND subscription_status = 'active'
        """, (user_id,))
        subscription = cursor.fetchone()
        
        # Check individual tool access
        cursor.execute("""
            SELECT tool_name FROM user_tool_access 
            WHERE user_id = %s
        """, (user_id,))
        tools = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "subscription": {
                "active": bool(subscription),
                "type": subscription[0] if subscription else None,
                "expires_at": subscription[2].isoformat() if subscription and subscription[2] else None
            },
            "tools": tools,
            "has_unlimited": bool(subscription),
            "success": True
        }
        
    except Exception as e:
        print(f"Access check error: {e}")
        return {"error": str(e), "success": False}

@app.get("/api/pricing")
async def get_pricing():
    """Get pricing information for frontend display"""
    return maya_stripe.get_pricing_display()

@app.get("/api/promotional-access")
async def get_promotional_access():
    """Get promotional access status"""
    try:
        from datetime import datetime
        
        # Check if promotional period is active
        promo_active = maya_stripe.promo_active
        if promo_active:
            promo_end = datetime.strptime(maya_stripe.promo_end_date, "%Y-%m-%d")
            promo_active = datetime.now() <= promo_end
        
        return {
            "promo_active": promo_active,
            "promo_end_date": maya_stripe.promo_end_date,
            "promo_message": "🎉 FREE until Aug 12, 2025!" if promo_active else "",
            "access_granted": promo_active,
            "message": "All spiritual tools are FREE during promotional period!" if promo_active else "Promotional period has ended."
        }
    except Exception as e:
        print(f"Promotional access check error: {e}")
        return {
            "promo_active": False,
            "access_granted": False,
            "message": "Unable to check promotional status"
        }

# Sacred Spiritual Tools API Endpoints

@app.post("/api/oracle-interpretation")
async def oracle_interpretation(request: Request, user = Depends(get_current_user)):
    """Generate AI-powered Maya Oracle Card interpretation (Premium Tool)"""
    import openai
    
    # Check premium access
    if not check_tool_access(user.get('id'), 'maya_oracle'):
        return {
            "error": "Premium access required",
            "message": "Maya Oracle Cards requires premium access. Please purchase or subscribe.",
            "tool_name": "maya_oracle",
            "premium_required": True,
            "success": False
        }
    
    try:
        body = await request.json()
        card = body.get('card', {})
        user_cosmic_profile = body.get('userCosmicProfile', {})
        
        # Get user's cosmic elements for personalized interpretation
        first_name = user_cosmic_profile.get('first_name', user.get('first_name', 'Sacred Soul'))
        day_sign = user_cosmic_profile.get('daySign', 'Unknown')
        element = user_cosmic_profile.get('element', 'Unknown')
        galactic_tone = user_cosmic_profile.get('galacticTone', 'Unknown')
        
        # Create personalized interpretation prompt
        interpretation_prompt = f"""You are an ancient Maya Oracle interpreter channeling ancestral wisdom. 

Card Drawn: {card.get('name', 'Unknown')}
Card Message: {card.get('message', 'Unknown')}

User Information:
- Name: {first_name}
- Day Sign: {day_sign}
- Element: {element}
- Galactic Tone: {galactic_tone}

Create a deeply personalized oracle interpretation that:
1. Explains how this card relates to {first_name}'s current spiritual journey
2. Connects the card's energy to their {day_sign} essence and {element} element
3. Provides specific guidance for their {galactic_tone} galactic tone
4. Offers practical spiritual advice for the next 24 hours
5. Includes affirmations aligned with their cosmic signature

Write in a mystical, wise tone as if speaking directly to {first_name}. Use "you" throughout. 
Include specific references to their Maya elements.
Format with proper HTML paragraphs and headings.
End with "The Magic is You, {first_name}!"

Keep the interpretation between 200-300 words, profound and actionable."""

        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a wise Maya Oracle interpreter providing personalized spiritual guidance through sacred card readings."},
                {"role": "user", "content": interpretation_prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        interpretation = response.choices[0].message.content
        
        return {"interpretation": interpretation, "success": True}
        
    except Exception as e:
        print(f"Oracle interpretation error: {e}")
        # Fallback interpretation
        fallback_interpretation = f"""
        <h4>Sacred Oracle Guidance for {first_name}</h4>
        <p>The card <strong>{card.get('name', 'Sacred Wisdom')}</strong> brings you this message: <em>{card.get('message', 'Trust your inner wisdom')}</em></p>
        <p>As a {day_sign} being aligned with {element} energy, this card speaks directly to your soul's current needs. Your {galactic_tone} vibration amplifies this message.</p>
        <p><strong>Today's Guidance:</strong> Trust the wisdom flowing through you. Your cosmic signature holds the key to understanding this message deeply.</p>
        <p><strong>Affirmation:</strong> "I am connected to ancient wisdom and trust my spiritual path."</p>
        <p>The Magic is You, {first_name}!</p>
        """
        return {"interpretation": fallback_interpretation, "success": True}

@app.post("/api/dream-analysis")
async def dream_analysis(request: Request, user = Depends(get_current_user)):
    """Generate AI-powered dream analysis with Maya symbolism (Premium Tool)"""
    import openai
    
    # Check premium access
    if not check_tool_access(user.get('id'), 'dream_interpreter'):
        return {
            "error": "Premium access required",
            "message": "Dream Interpreter requires premium access. Please purchase or subscribe.",
            "tool_name": "dream_interpreter",
            "premium_required": True,
            "success": False
        }
    
    try:
        body = await request.json()
        dream = body.get('dream', '')
        user_cosmic_profile = body.get('userCosmicProfile', {})
        
        if not dream:
            return {"error": "Dream description is required", "success": False}
        
        # Get user's cosmic elements for personalized analysis
        first_name = user_cosmic_profile.get('first_name', user.get('first_name', 'Sacred Soul'))
        day_sign = user_cosmic_profile.get('daySign', 'Unknown')
        element = user_cosmic_profile.get('element', 'Unknown')
        galactic_tone = user_cosmic_profile.get('galacticTone', 'Unknown')
        spirit_animal = user_cosmic_profile.get('spiritAnimal', 'Unknown')
        
        # Create personalized dream analysis prompt
        dream_prompt = f"""You are an expert Maya dream interpreter with deep knowledge of ancient symbolism and spiritual guidance.

Dreamer: {first_name}
Cosmic Signature: {day_sign} {galactic_tone}
Element: {element}
Spirit Animal: {spirit_animal}

Dream Description:
{dream}

Provide a comprehensive dream analysis that includes:

1. **MAYA SYMBOLISM**: Identify Maya symbols, animals, or spiritual elements in the dream
2. **PERSONAL SIGNIFICANCE**: Connect dream elements to {first_name}'s {day_sign} essence and {element} energy
3. **SPIRITUAL MESSAGE**: What is the dream trying to communicate about their spiritual path?
4. **COSMIC ALIGNMENT**: How does this dream relate to their {galactic_tone} galactic tone and current life phase?
5. **PRACTICAL GUIDANCE**: Specific actions or awareness they should embrace in waking life
6. **SPIRIT ANIMAL CONNECTION**: If their spirit animal {spirit_animal} appears or relates to the dream

Format with HTML headings and paragraphs. Use a mystical, wise tone.
Address {first_name} directly using "you" throughout.
End with "Trust your dream wisdom, {first_name}. The Magic is You!"

Keep analysis between 300-400 words, insightful and actionable."""

        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a master Maya dream interpreter providing profound spiritual insights through dream analysis."},
                {"role": "user", "content": dream_prompt}
            ],
            temperature=0.8,
            max_tokens=700
        )
        
        analysis = response.choices[0].message.content
        
        return {"analysis": analysis, "success": True}
        
    except Exception as e:
        print(f"Dream analysis error: {e}")
        # Fallback analysis
        fallback_analysis = f"""
        <h4>Dream Wisdom for {first_name}</h4>
        <p>Your dream carries profound spiritual significance, especially for a {day_sign} being aligned with {element} energy.</p>
        
        <h5>🌙 Maya Dream Wisdom</h5>
        <p>Dreams are sacred messages from the cosmos. Your {galactic_tone} galactic tone amplifies the spiritual significance of your nighttime visions.</p>
        
        <h5>🔮 Personal Guidance</h5>
        <p>This dream reflects your soul's current spiritual journey. Pay attention to symbols, emotions, and recurring themes.</p>
        
        <h5>✨ Practical Steps</h5>
        <p>Keep a dream journal, meditate on the symbols, and trust your intuitive understanding of the message.</p>
        
        <p>Trust your dream wisdom, {first_name}. The Magic is You!</p>
        """
        return {"analysis": fallback_analysis, "success": True}

@app.post("/api/breathwork-ritual")
async def breathwork_ritual(request: Request, user = Depends(get_current_user)):
    """Generate personalized breathwork ritual based on cosmic signature (Premium Tool)"""
    import openai
    
    # Check premium access
    if not check_tool_access(user.get('id'), 'sacred_rituals'):
        return {
            "error": "Premium access required",
            "message": "Sacred Rituals requires premium access. Please purchase or subscribe.",
            "tool_name": "sacred_rituals",
            "premium_required": True,
            "success": False
        }
    
    try:
        body = await request.json()
        user_cosmic_profile = body.get('userCosmicProfile', {})
        
        # Get user's cosmic elements for personalized ritual
        first_name = user_cosmic_profile.get('first_name', user.get('first_name', 'Sacred Soul'))
        day_sign = user_cosmic_profile.get('daySign', 'Unknown')
        element = user_cosmic_profile.get('element', 'Unknown')
        galactic_tone = user_cosmic_profile.get('galacticTone', 'Unknown')
        direction = user_cosmic_profile.get('direction', 'Unknown')
        
        # Create personalized breathwork prompt
        breathwork_prompt = f"""You are a Maya breathwork master creating personalized breathing ceremonies.

Practitioner: {first_name}
Cosmic Signature: {day_sign} {galactic_tone}
Element: {element}
Sacred Direction: {direction}

Create a complete breathwork ritual that includes:

1. **PREPARATION**: Sacred space setup facing {direction} direction
2. **ELEMENT BREATHING**: Specific breathing pattern for {element} energy
3. **GALACTIC TONE RHYTHM**: Breathing counts based on {galactic_tone} vibration
4. **DAY SIGN VISUALIZATION**: Imagery connected to {day_sign} essence
5. **COMPLETION**: Grounding and integration practices

Format as a step-by-step ritual guide with:
- Clear instructions for each phase
- Specific breathing counts and patterns
- Visualization guidance
- Affirmations aligned with their cosmic signature
- Duration for each section

Address {first_name} directly using "you" throughout.
Use HTML formatting with headings and numbered lists.
Keep ritual between 15-20 minutes total.
End with "Breathe your magic into being, {first_name}!"

Make it authentic, powerful, and deeply personal."""

        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a master Maya breathwork facilitator creating transformative breathing ceremonies."},
                {"role": "user", "content": breathwork_prompt}
            ],
            temperature=0.8,
            max_tokens=800
        )
        
        ritual = response.choices[0].message.content
        
        return {"ritual": ritual, "success": True}
        
    except Exception as e:
        print(f"Breathwork ritual error: {e}")
        # Fallback ritual
        fallback_ritual = f"""
        <h4>🌬️ Sacred Breathwork Journey for {first_name}</h4>
        
        <h5>1. Preparation (2 minutes)</h5>
        <p>Sit comfortably facing {direction} to align with your sacred direction. Close your eyes and connect with your {day_sign} essence.</p>
        
        <h5>2. Element Breathing (5 minutes)</h5>
        <p>Breathe with your {element} energy:</p>
        <ul>
            <li>Inhale for 4 counts, visualizing {element} energy entering your body</li>
            <li>Hold for 4 counts, feeling the energy circulate</li>
            <li>Exhale for 6 counts, releasing what no longer serves</li>
        </ul>
        
        <h5>3. Galactic Tone Integration (5 minutes)</h5>
        <p>Breathe in rhythm with your {galactic_tone} galactic tone vibration. Feel the cosmic frequency harmonizing your entire being.</p>
        
        <h5>4. Completion (3 minutes)</h5>
        <p>Place hands on heart. Breathe naturally while repeating: "I am aligned with my cosmic purpose. I breathe in magic, I breathe out love."</p>
        
        <p>Breathe your magic into being, {first_name}!</p>
        """
        return {"ritual": fallback_ritual, "success": True}

@app.post("/api/daily-ritual")
async def daily_ritual(request: Request, user = Depends(get_current_user)):
    """Generate personalized daily ritual based on cosmic signature (Premium Tool)"""
    import openai
    
    # Check premium access
    if not check_tool_access(user.get('id'), 'sacred_rituals'):
        return {
            "error": "Premium access required",
            "message": "Sacred Rituals requires premium access. Please purchase or subscribe.",
            "tool_name": "sacred_rituals",
            "premium_required": True,
            "success": False
        }
    
    try:
        body = await request.json()
        user_cosmic_profile = body.get('userCosmicProfile', {})
        
        # Get user's cosmic elements for personalized ritual
        first_name = user_cosmic_profile.get('first_name', user.get('first_name', 'Sacred Soul'))
        day_sign = user_cosmic_profile.get('daySign', 'Unknown')
        element = user_cosmic_profile.get('element', 'Unknown')
        galactic_tone = user_cosmic_profile.get('galacticTone', 'Unknown')
        direction = user_cosmic_profile.get('direction', 'Unknown')
        crystal_ally = user_cosmic_profile.get('crystalAlly', 'Unknown')
        
        # Create personalized daily ritual prompt
        ritual_prompt = f"""You are a Maya ceremonial master creating personalized daily spiritual practices.

Practitioner: {first_name}
Cosmic Signature: {day_sign} {galactic_tone}
Element: {element}
Sacred Direction: {direction}
Crystal Ally: {crystal_ally}

Create a complete daily ritual that includes:

1. **MORNING ALIGNMENT**: Sacred actions to start the day
2. **ELEMENT PRACTICE**: Working with {element} energy throughout the day
3. **CRYSTAL WORK**: How to use {crystal_ally} for spiritual support
4. **GALACTIC TONE AFFIRMATION**: Specific affirmations for {galactic_tone} energy
5. **EVENING REFLECTION**: Closing ceremony for the day

Format as a comprehensive daily practice guide with:
- Specific times and durations
- Clear step-by-step instructions
- Affirmations and prayers
- Practical integration tips
- Sacred objects or tools needed

Address {first_name} directly using "you" throughout.
Use HTML formatting with headings and organized sections.
Make it realistic for daily practice (10-15 minutes total).
End with "Live your sacred path daily, {first_name}!"

Make it authentic, practical, and deeply meaningful."""

        openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Maya ceremonial master creating transformative daily spiritual practices."},
                {"role": "user", "content": ritual_prompt}
            ],
            temperature=0.8,
            max_tokens=800
        )
        
        ritual = response.choices[0].message.content
        
        return {"ritual": ritual, "success": True}
        
    except Exception as e:
        print(f"Daily ritual error: {e}")
        # Fallback ritual
        fallback_ritual = f"""
        <h4>🌟 Daily Sacred Practice for {first_name}</h4>
        
        <h5>Morning Alignment (5 minutes)</h5>
        <p>Upon waking, face {direction} and greet the day with gratitude. Hold your {crystal_ally} and connect with your {day_sign} essence.</p>
        
        <h5>Element Practice (Throughout Day)</h5>
        <p>Work with {element} energy by:</p>
        <ul>
            <li>Connecting with {element} in nature</li>
            <li>Visualizing {element} energy during meals</li>
            <li>Breathing {element} qualities throughout the day</li>
        </ul>
        
        <h5>Galactic Tone Affirmation</h5>
        <p>Repeat throughout the day: "I embody the {galactic_tone} frequency. I am aligned with my cosmic purpose."</p>
        
        <h5>Evening Reflection (5 minutes)</h5>
        <p>Before sleep, thank your {day_sign} spirit for guidance. Hold your {crystal_ally} and reflect on the day's spiritual lessons.</p>
        
        <p>Live your sacred path daily, {first_name}!</p>
        """
        return {"ritual": fallback_ritual, "success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
