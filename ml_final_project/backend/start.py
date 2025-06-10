#!/usr/bin/env python3
"""
Startup script for the FastAPI Lung Disease Detection Backend
"""

import uvicorn
import os
import sys

def main():
    """Main function to start the FastAPI server"""
    
    # Set environment variables if needed
    os.environ.setdefault("PYTHONPATH", ".")
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("DEBUG", "True").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print("🚀 Starting Lung Disease Detection API...")
    print(f"📍 Server will run on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {reload}")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 