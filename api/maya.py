from fastapi import FastAPI, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from mangum import Mangum
import os
import bcrypt
import jwt
from typing import Optional
import json
from datetime import datetime, timedelta
import asyncio

app = FastAPI()
security = HTTPBearer()

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "maya-cosmic-blueprint-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 1 week

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_data: dict) -> str:
    payload = {
        'user_id': user_data.get('id'),
        'email': user_data.get('email'),
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Maya Cosmic Blueprint Platform Homepage"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Magic is You - Discover Your Sacred Maya Cosmic Blueprint</title>
    <meta name="description" content="Unlock your personalized Maya cosmic blueprint with 35+ spiritual elements, AI-powered explanations, and sacred wisdom. Create your soul contract and discover your spiritual destiny today.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        .cosmic-background {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            position: relative;
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
        
        .gradient-text {
            background: linear-gradient(135deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Mobile Optimizations */
        @media (max-width: 640px) {
            .form-container {
                padding: 1.25rem;
                margin: 0.75rem 0;
                border-radius: 1.5rem;
            }
            
            .element-bubble {
                padding: 1rem;
                border-radius: 1rem;
            }
            
            .grid-cols-2 {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }
        }
    </style>
</head>
<body class="cosmic-background min-h-screen font-sans">
    
    <div class="container mx-auto p-4 lg:p-8">
        
        <!-- Header with Animation -->
        <div class="text-center mb-16">
            <div class="mb-8">
                <h1 class="text-4xl sm:text-5xl lg:text-7xl font-bold gradient-text mb-6 pulse-glow">
                    ✨ The Magic is You ✨
                </h1>
                <div class="text-xl sm:text-2xl lg:text-3xl font-bold mb-4 drop-shadow-lg" style="color: #1e3a8a;">
                    Discover Your Sacred Maya Cosmic Blueprint
                </div>
                <div class="text-base sm:text-lg lg:text-xl font-medium drop-shadow-md" style="color: #1e3a8a;">
                    🏛️ Ancient Maya Astrology • 🔮 Shamanic Guidance • 🌟 3,000+ Years of Wisdom
                </div>
            </div>
        </div>
        
        <!-- Main Authentication Interface -->
        <div class="max-w-2xl mx-auto mb-16">
            <!-- Registration Section -->
            <div class="bg-white/95 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/30 form-container">
                <h2 class="mb-6" style="color: #1e3a8a; font-weight: 900; font-size: 2rem; text-align: center;">
                    🏛️ Begin Your Sacred Journey
                </h2>
                <p class="text-center text-blue-700 mb-8 font-medium">Unlock your personalized Maya cosmic blueprint and soul contract</p>
                
                <form id="registerForm" class="space-y-6">
                    <div>
                        <label class="block text-blue-800 font-semibold text-lg mb-3">
                            👤 Full Name <span class="text-sm text-amber-700">(for sacred numerology)</span>
                        </label>
                        <input type="text" id="registerFullName" name="fullName" 
                               placeholder="Enter your complete birth name"
                               class="form-input"
                               required>
                    </div>
                    
                    <div>
                        <label class="block text-blue-800 font-semibold text-lg mb-3">
                            📧 Email Address
                        </label>
                        <input type="email" id="registerEmail" name="email" 
                               placeholder="Enter your email address"
                               class="form-input"
                               required>
                    </div>
                    
                    <div>
                        <label class="block text-blue-800 font-semibold text-lg mb-3">
                            🔒 Password
                        </label>
                        <input type="password" id="registerPassword" name="password" 
                               placeholder="Create a secure password (min 6 characters)"
                               class="form-input"
                               required minlength="6">
                    </div>
                    
                    <div>
                        <label class="block text-blue-800 font-semibold text-lg mb-3">
                            📅 Birth Date <span class="text-sm text-amber-700">(for Maya calculations)</span>
                        </label>
                        <input type="date" id="registerBirthDate" name="birthDate" 
                               class="form-input"
                               required>
                    </div>
                    
                    <button type="submit" 
                            class="w-full cosmic-button register text-white font-bold py-4 rounded-xl text-xl">
                        🌟 Create My Cosmic Blueprint
                    </button>
                </form>
                
                <div class="text-center mt-6">
                    <p class="text-gray-600">Already have an account? 
                        <button onclick="showLoginForm()" class="text-purple-600 hover:text-purple-800 underline font-semibold">Sign In</button>
                    </p>
                </div>
            </div>
        </div>

        <!-- Login Modal -->
        <div id="loginModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-3xl p-8 max-w-md w-full">
                <h2 class="text-center text-purple-700 font-bold text-2xl mb-6">🔮 Welcome Back</h2>
                <form id="loginForm" class="space-y-6">
                    <div>
                        <label class="block text-gray-700 font-semibold mb-2">📧 Email</label>
                        <input type="email" id="loginEmail" class="form-input" required>
                    </div>
                    <div>
                        <label class="block text-gray-700 font-semibold mb-2">🔒 Password</label>
                        <input type="password" id="loginPassword" class="form-input" required>
                    </div>
                    <button type="submit" class="w-full cosmic-button text-white font-bold py-3 rounded-xl">
                        ✨ Enter My Sacred Space
                    </button>
                </form>
                <div class="text-center mt-6">
                    <button onclick="hideLoginForm()" class="text-gray-600 hover:text-gray-800">Close</button>
                </div>
            </div>
        </div>
        
        <!-- 35+ Cosmic Elements Preview Section -->
        <div class="max-w-7xl mx-auto mt-20 mb-8">
            <!-- Header -->
            <div class="text-center mb-16">
                <h2 class="text-3xl sm:text-4xl lg:text-6xl font-bold gradient-text mb-6 pulse-glow">
                    🌟 Your Cosmic Blueprint Awaits
                </h2>
                <p class="text-lg sm:text-xl lg:text-2xl font-bold max-w-4xl mx-auto drop-shadow-lg" style="color: #1e3a8a;">
                    Once you register, we'll calculate your complete personalized cosmic blueprint using authentic Maya astronomy
                </p>
            </div>
            
            <!-- Core Maya Elements -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8" style="color: #1e3a8a;">
                    🔮 Core Maya Elements
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🔸</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Day Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Your Maya glyph (e.g. Ahau Sun)</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🎵</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Galactic Tone</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Your cosmic frequency (1-13)</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🆔</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Kin Number</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Your position in 260-day cycle</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🔥</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Element</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Fire, Water, Air, or Earth</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">📱</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Life Path</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Your soul's journey purpose</p>
                    </div>
                </div>
            </div>
            
            <!-- Sacred Calendar Elements -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8" style="color: #1e3a8a;">
                    📅 Sacred Calendar Elements
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    <div class="element-bubble">
                        <div class="text-3xl mb-2">⚡</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a;">Trecena</h4>
                        <p class="text-xs" style="color: #1e3a8a;">13-day sacred cycle</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-3xl mb-2">🌙</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a;">Wavespell</h4>
                        <p class="text-xs" style="color: #1e3a8a;">13-day consciousness journey</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-3xl mb-2">🏰</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a;">Castle</h4>
                        <p class="text-xs" style="color: #1e3a8a;">52-day spiritual castle</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-3xl mb-2">🌺</div>
                        <h4 class="font-bold text-sm" style="color: #1e3a8a;">Color Family</h4>
                        <p class="text-xs" style="color: #1e3a8a;">Red, White, Blue, Yellow</p>
                    </div>
                </div>
            </div>
            
            <!-- Maya Cross & Calendar Systems -->
            <div class="mb-12">
                <h3 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-center mb-8" style="color: #1e3a8a;">
                    ✨ Maya Cross & Calendar Systems
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🧭</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Guide Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Higher guidance</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">⚖️</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Antipode Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Balancing opposite</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🔮</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Occult Sign</h4>
                        <p class="text-sm" style="color: #1e3a8a;">Hidden powers</p>
                    </div>
                    <div class="element-bubble">
                        <div class="text-4xl mb-3">🌙</div>
                        <h4 class="font-bold text-lg" style="color: #1e3a8a;">Lord of Night</h4>
                        <p class="text-sm" style="color: #1e3a8a;">9-day cycle guardian</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
        
    <!-- JavaScript -->
    <script>
        function showLoginForm() {
            document.getElementById('loginModal').classList.remove('hidden');
        }
        
        function hideLoginForm() {
            document.getElementById('loginModal').classList.add('hidden');
        }
        
        // Registration form handling
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    alert('Registration successful! Redirecting to your dashboard...');
                    window.location.href = '/dashboard';
                } else {
                    const error = await response.json();
                    alert(error.message || 'Registration failed');
                }
            } catch (error) {
                alert('Registration error. Please try again.');
            }
        });
        
        // Login form handling
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    localStorage.setItem('token', result.token);
                    window.location.href = '/dashboard';
                } else {
                    const error = await response.json();
                    alert(error.message || 'Login failed');
                }
            } catch (error) {
                alert('Login error. Please try again.');
            }
        });
    </script>
</body>
</html>"""

@app.post("/api/register")
async def register(
    fullName: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    birthDate: str = Form(...)
):
    """User registration endpoint"""
    try:
        # For now, we'll just return a success response
        # In production, you'd save to a database
        user_data = {
            'id': 1,
            'name': fullName,
            'email': email,
            'birth_date': birthDate
        }
        
        token = create_jwt_token(user_data)
        
        return JSONResponse({
            "message": "Registration successful!",
            "token": token,
            "user": {
                "name": fullName,
                "email": email,
                "birth_date": birthDate
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """User login endpoint"""
    try:
        # For now, we'll just return a success response
        # In production, you'd verify against a database
        user_data = {
            'id': 1,
            'email': email
        }
        
        token = create_jwt_token(user_data)
        
        return JSONResponse({
            "message": "Login successful!",
            "token": token
        })
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """User dashboard"""
    return """
    <html>
    <head>
        <title>Maya Cosmic Blueprint - Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gradient-to-br from-purple-100 to-amber-100 min-h-screen">
        <div class="container mx-auto p-8">
            <h1 class="text-4xl font-bold text-center text-purple-800 mb-8">
                🌟 Your Maya Cosmic Blueprint Dashboard
            </h1>
            <div class="bg-white rounded-lg p-8 shadow-xl">
                <h2 class="text-2xl font-bold text-center mb-6">Welcome to Your Sacred Space!</h2>
                <p class="text-center text-gray-600 mb-8">
                    Your personalized Maya cosmic blueprint is being prepared...
                </p>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="bg-gradient-to-br from-purple-500 to-purple-700 text-white p-6 rounded-lg">
                        <h3 class="text-xl font-bold mb-2">🔮 Cosmic Blueprint</h3>
                        <p>Your personalized Maya elements and spiritual guidance</p>
                    </div>
                    <div class="bg-gradient-to-br from-amber-500 to-amber-700 text-white p-6 rounded-lg">
                        <h3 class="text-xl font-bold mb-2">📜 Soul Contract</h3>
                        <p>Your sacred spiritual agreement and life purpose</p>
                    </div>
                    <div class="bg-gradient-to-br from-blue-500 to-blue-700 text-white p-6 rounded-lg">
                        <h3 class="text-xl font-bold mb-2">🌟 Daily Guidance</h3>
                        <p>Personalized spiritual insights for your journey</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "platform": "Maya Cosmic Blueprint", "deployed": True}

# Create the handler for Vercel
handler = Mangum(app, lifespan="off")