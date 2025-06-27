#!/usr/bin/env python3
"""
Tuari Inventory Management System - Startup Script
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    try:
        from database import create_tables
        create_tables()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

def check_database():
    """Check if database exists and is accessible"""
    db_path = Path("data/inventory.db")
    if db_path.exists():
        print(f"✅ Database found: {db_path}")
        return True
    else:
        print("⚠️  Database not found, will be created on startup")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Tuari Inventory Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("=" * 50)
    print("🎯 Tuari Inventory Management System")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt not found")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Initialize database
    initialize_database()
    
    # Check database status
    check_database()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 