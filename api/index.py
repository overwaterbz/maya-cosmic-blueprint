#!/usr/bin/env python3
"""
Vercel ASGI handler for Maya Cosmic Blueprint Platform
"""

import sys
import os
from mangum import Mangum

# Add the parent directory to Python path to import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from app import app

# Create ASGI handler for Vercel
handler = Mangum(app, lifespan="off")