# src/db.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

class DatabaseManager:
    """
    Handles all database operations using Supabase with user authentication
    """
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        # If .env file doesn't exist, try to use default credentials from README
        if not url or not key:
            print("⚠️ .env file not found. Using default credentials...")
            url = "https://uwznjoflnjcjjdzggbqg.supabase.co"
            key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3em5qb2ZsbmpjampkemdnYnFnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNDQsImV4cCI6MjA3MzY1ODA0NH0.Klw4Zw0BOml-pxQnsjLTTbUtdgUXz11YTnk_DhlpZIo"

        if not url or not key:
            raise ValueError("Supabase credentials are missing. Please create a .env file or run setup_env.py")

        try:
            self.client: Client = create_client(url, key)
            print("✅ Connected to Supabase successfully!")
        except Exception as e:
            raise ValueError(f"Failed to connect to Supabase: {str(e)}")

    # --- Authentication Methods ---
    def sign_up(self, email, password):
        """Register a new user"""
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            if response.user:
                return {"Success": True, "user": response.user, "error": None}
            else:
                return {"Success": False, "user": None, "error": "User registration failed - no user returned"}
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                return {"Success": False, "user": None, "error": "User already exists with this email"}
            elif "invalid email" in error_msg.lower():
                return {"Success": False, "user": None, "error": "Invalid email format"}
            else:
                return {"Success": False, "user": None, "error": f"Registration failed: {error_msg}"}

    def sign_in(self, email, password):
        """Login existing user"""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user and response.session:
                return {"Success": True, "user": response.user, "session": response.session, "error": None}
            else:
                return {"Success": False, "user": None, "session": None, "error": "Login failed - invalid response"}
        except Exception as e:
            error_msg = str(e)
            if "invalid login credentials" in error_msg.lower():
                return {"Success": False, "user": None, "session": None, "error": "Invalid email or password"}
            elif "email not confirmed" in error_msg.lower():
                return {"Success": False, "user": None, "session": None, "error": "Please check your email and confirm your account"}
            else:
                return {"Success": False, "user": None, "session": None, "error": f"Login failed: {error_msg}"}

    def sign_out(self):
        """Logout current user"""
        try:
            self.client.auth.sign_out()
            return {"Success": True, "error": None}
        except Exception as e:
            return {"Success": False, "error": str(e)}

    # --- Create ---
    def create_transaction(self, title, amount, category, type_, date, notes, user_id):
        try:
            response = self.client.table("transactions").insert({
                "title": title,
                "amount": amount,
                "category": category,
                "type": type_,
                "date": date,
                "notes": notes,
                "user_id": user_id
            }).execute()
            return {"Success": True, "data": response.data, "error": None}
        except Exception as e:
            return {"Success": False, "data": None, "error": str(e)}

    # --- Read ---
    def get_all_transactions(self, user_id):
        """Get all transactions for a specific user only"""
        try:
            response = self.client.table("transactions").select("*").eq("user_id", user_id).execute()
            return {"Success": True, "data": response.data, "error": None}
        except Exception as e:
            return {"Success": False, "data": None, "error": str(e)}

    # --- Update ---
    def update_transactions(self, transaction_id, updated_data: dict, user_id):
        """Update transaction (only if it belongs to the user)"""
        try:
            response = self.client.table("transactions").update(updated_data).eq("id", transaction_id).eq("user_id", user_id).execute()
            return {"Success": True, "data": response.data, "error": None}
        except Exception as e:
            return {"Success": False, "data": None, "error": str(e)}

    # --- Delete ---
    def delete_transactions(self, transaction_id, user_id):
        """Delete transaction (only if it belongs to the user)"""
        try:
            response = self.client.table("transactions").delete().eq("id", transaction_id).eq("user_id", user_id).execute()
            return {"Success": True, "data": response.data, "error": None}
        except Exception as e:
            return {"Success": False, "data": None, "error": str(e)}