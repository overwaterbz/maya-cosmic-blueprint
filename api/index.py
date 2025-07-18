#!/usr/bin/env python3
"""
Vercel handler for Maya Cosmic Blueprint Platform
"""

import sys
import os

# Add the parent directory to Python path to import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel handler - this is the entry point for Vercel
handler = app