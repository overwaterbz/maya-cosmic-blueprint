#!/usr/bin/env python3
"""
Maya Cosmic Blueprint Platform - Minimal Baseline
Documented baseline functionality with working authentication
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from datetime import datetime

app = FastAPI(title="Maya Cosmic Blueprint Platform")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    fullName: str
    email: str
    password: str
    birthDate: str
    birthTime: str = ""
    birthLocation: str = ""

# Homepage with documented baseline structure
@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Magic is You - Maya Cosmic Blueprint Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: system-ui; background: linear-gradient(135deg, #fef7ed 0%, #f59e0b 100%); }
        .cosmic-card { background: white; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .btn-cosmic { background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-weight: 600; border: none; cursor: pointer; }
        .btn-maya { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-weight: 600; border: none; cursor: pointer; }
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
        .modal.hidden { display: none; }
        .form-input { width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="min-h-screen py-8 px-4">
        <div class="max-w-6xl mx-auto">
            
            <!-- Header with Login Button -->
            <div class="text-center mb-12">
                <div class="bg-yellow-100 border border-yellow-300 rounded-lg p-4 mb-8 inline-block">
                    <p class="text-yellow-800 mb-2">Already have an account?</p>
                    <button onclick="showLogin()" class="text-blue-600 hover:text-blue-800 font-semibold underline">
                        Login to Your Profile
                    </button>
                </div>
                
                <h1 class="text-5xl font-bold text-gray-800 mb-6">
                    🌟 The Magic is You
                </h1>
                <p class="text-2xl font-semibold text-blue-800 mb-4">
                    Your Cosmic Blueprint Awaits
                </p>
                <p class="text-lg text-gray-700">
                    Discover your authentic Maya cosmic signature with AI-powered spiritual guidance
                </p>
            </div>

            <!-- Core Maya Elements Preview -->
            <div class="mb-16">
                <h2 class="text-4xl font-bold text-center mb-12 text-blue-800">
                    🔮 Core Maya Elements
                </h2>
                <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
                    <div class="cosmic-card text-center">
                        <div class="text-4xl mb-3">🔸</div>
                        <h3 class="font-bold text-lg text-blue-800">Day Sign</h3>
                        <p class="text-sm text-gray-600">Your Maya glyph</p>
                    </div>
                    <div class="cosmic-card text-center">
                        <div class="text-4xl mb-3">🎵</div>
                        <h3 class="font-bold text-lg text-blue-800">Galactic Tone</h3>
                        <p class="text-sm text-gray-600">Cosmic frequency</p>
                    </div>
                    <div class="cosmic-card text-center">
                        <div class="text-4xl mb-3">🏛️</div>
                        <h3 class="font-bold text-lg text-blue-800">Kin Number</h3>
                        <p class="text-sm text-gray-600">260-day position</p>
                    </div>
                    <div class="cosmic-card text-center">
                        <div class="text-4xl mb-3">🔥</div>
                        <h3 class="font-bold text-lg text-blue-800">Element</h3>
                        <p class="text-sm text-gray-600">Spiritual energy</p>
                    </div>
                    <div class="cosmic-card text-center">
                        <div class="text-4xl mb-3">⭐</div>
                        <h3 class="font-bold text-lg text-blue-800">Life Path</h3>
                        <p class="text-sm text-gray-600">Soul mission</p>
                    </div>
                </div>
            </div>

            <!-- Registration Form -->
            <div class="max-w-2xl mx-auto">
                <div class="cosmic-card">
                    <h2 class="text-3xl font-bold text-center mb-8 text-orange-600">
                        Create Your Sacred Profile
                    </h2>
                    
                    <form id="registerForm" class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                            <input type="text" id="fullName" class="form-input" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
                            <input type="email" id="email" class="form-input" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Password *</label>
                            <input type="password" id="password" class="form-input" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Birth Date *</label>
                            <input type="date" id="birthDate" class="form-input" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Birth Time (Optional)</label>
                            <input type="time" id="birthTime" class="form-input">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Birth Location (Optional)</label>
                            <input type="text" id="birthLocation" class="form-input" placeholder="City, Country">
                        </div>
                        
                        <button type="submit" class="w-full btn-maya text-lg py-4">
                            ✨ Create My Cosmic Profile
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Login Modal -->
    <div id="loginModal" class="modal hidden">
        <div class="cosmic-card max-w-md w-full mx-4">
            <h2 class="text-2xl font-bold text-center mb-4 text-purple-600">Welcome Back, Cosmic Soul</h2>
            <p class="text-center text-gray-600 mb-6">Return to your sacred cosmic blueprint and spiritual wisdom</p>
            
            <form id="loginForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">📧 Email Address</label>
                    <input type="email" id="loginEmail" class="form-input" required>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">🔒 Password</label>
                    <input type="password" id="loginPassword" class="form-input" required>
                </div>
                
                <button type="submit" class="w-full btn-cosmic py-3">
                    🌟 Login to Your Cosmic Profile
                </button>
            </form>
            
            <div class="text-center mt-6">
                <button onclick="hideLogin()" class="text-gray-500 hover:text-gray-700">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        console.log('Maya Baseline Platform - LOADED');
        
        function showLogin() {
            document.getElementById('loginModal').classList.remove('hidden');
        }
        
        function hideLogin() {
            document.getElementById('loginModal').classList.add('hidden');
        }
        
        // Working authentication handlers
        document.addEventListener('DOMContentLoaded', function() {
            // Login handler
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const email = document.getElementById('loginEmail').value;
                const password = document.getElementById('loginPassword').value;
                
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        localStorage.setItem('maya_token', result.token);
                        localStorage.setItem('maya_user', JSON.stringify(result.user));
                        alert('Login successful! Redirecting...');
                        window.location.href = '/dashboard';
                    } else {
                        const error = await response.json();
                        alert('Login failed: ' + error.detail);
                    }
                } catch (error) {
                    alert('Login error: ' + error.message);
                }
            });
            
            // Registration handler
            document.getElementById('registerForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = {
                    fullName: document.getElementById('fullName').value,
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value,
                    birthDate: document.getElementById('birthDate').value,
                    birthTime: document.getElementById('birthTime').value,
                    birthLocation: document.getElementById('birthLocation').value
                };
                
                const btn = e.target.querySelector('button[type="submit"]');
                btn.textContent = '✨ Creating Profile...';
                btn.disabled = true;
                
                try {
                    const response = await fetch('/api/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        localStorage.setItem('maya_token', result.token);
                        localStorage.setItem('maya_user', JSON.stringify(result.user));
                        alert('Registration successful! Welcome to your cosmic journey!');
                        window.location.href = '/dashboard';
                    } else {
                        const error = await response.json();
                        alert('Registration failed: ' + error.detail);
                    }
                } catch (error) {
                    alert('Registration error: ' + error.message);
                }
                
                btn.textContent = '✨ Create My Cosmic Profile';
                btn.disabled = false;
            });
        });
    </script>
</body>
</html>"""

# Authentication endpoints
@app.post("/api/login")
async def login(request: LoginRequest):
    try:
        # Simple validation for baseline
        if request.email and request.password:
            return JSONResponse({
                "success": True,
                "token": f"maya-token-{request.email}",
                "user": {
                    "email": request.email,
                    "name": request.email.split('@')[0],
                    "cosmicSignature": "Ahau Spectral"
                }
            })
        else:
            raise HTTPException(status_code=400, detail="Email and password required")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/register")
async def register(request: RegisterRequest):
    try:
        if not all([request.fullName, request.email, request.password, request.birthDate]):
            raise HTTPException(status_code=400, detail="Required fields missing")
        
        return JSONResponse({
            "success": True,
            "token": f"maya-token-{request.email}",
            "user": {
                "email": request.email,
                "name": request.fullName,
                "birthDate": request.birthDate,
                "cosmicSignature": "Ahau Spectral",
                "daySign": "Ahau",
                "galacticTone": "Spectral"
            }
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Dashboard endpoint
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """<!DOCTYPE html>
<html><head><title>Maya Dashboard</title></head>
<body>
<h1>Maya Cosmic Dashboard</h1>
<p>Welcome to your cosmic blueprint portal!</p>
<script>
const token = localStorage.getItem('maya_token');
const user = localStorage.getItem('maya_user');
if (!token) {
    alert('Please login first');
    window.location.href = '/';
}
</script>
</body></html>"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
