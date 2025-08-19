#!/usr/bin/env python3
"""
Alternative startup script - run from project root
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Astro AI Backend...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("💫 Press Ctrl+C to stop")
    
    # Run using module path to avoid import issues
    uvicorn.run(
        "backend.api:api", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=["backend", "tools"]
    )