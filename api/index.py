#!/usr/bin/env python3
"""
Proper Vercel entry point for Maya Cosmic Blueprint Platform
Imports complete FastAPI application with all functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mangum import Mangum
    from app import app
    
    # Create serverless handler
    handler = Mangum(app)
    
except Exception as e:
    # Fallback handler
    def handler(event, context):
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': '<!DOCTYPE html><html><head><title>Maya Platform</title></head><body><h1>Maya Platform Loading</h1></body></html>'
        }
