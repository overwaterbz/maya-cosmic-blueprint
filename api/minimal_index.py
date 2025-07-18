#!/usr/bin/env python3
"""
Minimal Vercel handler for Maya Cosmic Blueprint Platform
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from mangum import Mangum
import os

# Create FastAPI app
app = FastAPI(title="Maya Cosmic Blueprint Platform")

# Simple homepage
@app.get("/")
async def homepage():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Maya Cosmic Blueprint Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; line-height: 1.6; }
            .btn { display: inline-block; padding: 12px 24px; background: rgba(255,255,255,0.2); border: 2px solid white; border-radius: 25px; color: white; text-decoration: none; margin: 10px; }
            .btn:hover { background: rgba(255,255,255,0.3); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Maya Cosmic Blueprint Platform</h1>
            <p>Your personalized spiritual guidance system is starting up...</p>
            <p>Experience AI-powered Maya cosmic insights, dream interpretation, and sacred ritual guidance.</p>
            <a href="/api/health" class="btn">Check Status</a>
        </div>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health():
    return JSONResponse({
        "status": "healthy", 
        "platform": "Maya Cosmic Blueprint",
        "message": "Platform is operational"
    })

# Create ASGI handler for Vercel
handler = Mangum(app, lifespan="off")