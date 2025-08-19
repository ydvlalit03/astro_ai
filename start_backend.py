#!/usr/bin/env python3
"""
Simple script to start the FastAPI backend server
"""

import sys
import os
import uvicorn

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api import api

if __name__ == "__main__":
    print("🚀 Starting Astro AI Backend...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("💫 Press Ctrl+C to stop")
    
    uvicorn.run(
        "backend.api:api", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=["backend", "tools"]
    )