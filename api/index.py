#!/usr/bin/env python3
"""
Vercel Entry Point for Maya Cosmic Blueprint Platform
Proper serverless adapter using Mangum for FastAPI
"""

import sys
import os

# Add the parent directory to the Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from mangum import Mangum
    # Import the complete FastAPI application
    from app import app
    
    # Create proper serverless handler using Mangum
    # This preserves ALL functionality: authentication, AI guidance, soul contracts, cosmic blueprints
    handler = Mangum(app)
    
except Exception as e:
    # Fallback to basic response if import fails
    def handler(event, context):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Maya Platform Import Error: {str(e)}'
        }