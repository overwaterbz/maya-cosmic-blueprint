#!/usr/bin/env python3
"""
Vercel ASGI handler for Maya Cosmic Blueprint Platform
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path to import our app
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from mangum import Mangum
    from app import app
    
    # Create ASGI handler for Vercel
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    # Fallback basic handler
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return JSONResponse({"message": "Maya Cosmic Blueprint Platform", "status": "initializing"})
    
    @app.get("/health")
    async def health():
        return JSONResponse({"status": "healthy"})
    
    handler = Mangum(app, lifespan="off")