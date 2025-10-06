#!/usr/bin/env python3
"""
Startup script for Track My Money application
"""
import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import streamlit
        import supabase
        import pandas
        import matplotlib
        import requests
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment and database"""
    print("🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        try:
            with open('.env', 'w') as f:
                f.write('SUPABASE_URL="https://uwznjoflnjcjjdzggbqg.supabase.co"\n')
                f.write('SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3em5qb2ZsbmpjampkemdnYnFnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNDQsImV4cCI6MjA3MzY1ODA0NH0.Klw4Zw0BOml-pxQnsjLTTbUtdgUXz11YTnk_DhlpZIo"\n')
            print("✅ .env file created!")
        except Exception as e:
            print(f"⚠️ Could not create .env file: {e}")
    
    # Setup database
    print("🗄️ Setting up database...")
    try:
        from setup_database import setup_database
        setup_database()
    except Exception as e:
        print(f"⚠️ Database setup warning: {e}")

def start_api():
    """Start the FastAPI backend"""
    print("🚀 Starting API server...")
    try:
        # Change to API directory and start the server
        os.chdir('API')
        subprocess.Popen([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'])
        print("✅ API server started on http://127.0.0.1:8000")
        os.chdir('..')
        return True
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("🌐 Starting frontend...")
    try:
        # Start Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'Frontend/app.py', '--server.port', '8501'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main startup function"""
    print("💰 Track My Money - Starting Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Start API server
    if start_api():
        print("⏳ Waiting for API server to start...")
        time.sleep(3)
        
        # Start frontend
        start_frontend()
    else:
        print("❌ Cannot start application without API server")

if __name__ == "__main__":
    main()
