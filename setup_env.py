#!/usr/bin/env python3
"""
Setup script to create .env file with Supabase credentials
"""
import os

def create_env_file():
    """Create .env file with Supabase credentials"""
    env_content = '''SUPABASE_URL="https://uwznjoflnjcjjdzggbqg.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3em5qb2ZsbmpjampkemdnYnFnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNDQsImV4cCI6MjA3MzY1ODA0NH0.Klw4Zw0BOml-pxQnsjLTTbUtdgUXz11YTnk_DhlpZIo"
'''
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("SUCCESS: .env file created successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Error creating .env file: {e}")
        return False

if __name__ == "__main__":
    create_env_file()
