# src/logic.py
from src.db import DatabaseManager

class TransactionManager:
    """
    Acts as a bridge between frontend and database with authentication
    """
    def __init__(self):
        self.db = DatabaseManager()

    # --- Authentication Methods ---
    def register_user(self, email, password):
        """Register a new user"""
        if not email or not password:
            return {"Success": False, "message": "Email and password are required"}
        
        if len(password) < 6:
            return {"Success": False, "message": "Password must be at least 6 characters"}
        
        result = self.db.sign_up(email, password)
        if result.get("Success"):
            return {"Success": True, "message": "Registration successful! Please login.", "user": result.get("user")}
        return {"Success": False, "message": f"Error: {result.get('error')}"}

    def login_user(self, email, password):
        """Login user"""
        if not email or not password:
            return {"Success": False, "message": "Email and password are required"}
        
        result = self.db.sign_in(email, password)
        if result.get("Success"):
            return {"Success": True, "message": "Login successful!", "user": result.get("user"), "session": result.get("session")}
        return {"Success": False, "message": f"Error: {result.get('error')}"}

    def logout_user(self):
        """Logout user"""
        result = self.db.sign_out()
        if result.get("Success"):
            return {"Success": True, "message": "Logged out successfully!"}
        return {"Success": False, "message": f"Error: {result.get('error')}"}

    # --- Transaction Methods (with user_id) ---
    def add_transaction(self, title, amount, category, type, date, notes, user_id):
        """Add a new Transaction for specific user"""
        if not title or not amount:
            return {"Success": False, "message": "Title and amount are required"}
        
        result = self.db.create_transaction(title, amount, category, type, date, notes, user_id)
        if result.get("Success"):
            return {"Success": True, "message": "Transaction added Successfully!", "data": result.get("data")}
        return {"Success": False, "message": f"Error: {result.get('error')}"}

    def get_transactions(self, user_id):
        """Get all Transactions for specific user only"""
        result = self.db.get_all_transactions(user_id)
        if result.get("Success"):
            return result.get("data", [])
        return []
    
    def change_transaction(self, transaction_id, updated_data: dict, user_id):
        """Update a transaction (only user's own transaction)"""
        if not transaction_id or not updated_data:
            return {"Success": False, "message": "Transaction ID and updated data are required"}
        
        result = self.db.update_transactions(transaction_id, updated_data, user_id)
        if result.get("Success"):
            return {"Success": True, "message": "Transaction updated successfully!", "data": result.get("data")}
        return {"Success": False, "message": f"Error: {result.get('error')}"}
    
    def remove_transaction(self, transaction_id, user_id):
        """Delete a transaction (only user's own transaction)"""
        if not transaction_id:
            return {"Success": False, "message": "Transaction ID is required"}
        
        result = self.db.delete_transactions(transaction_id, user_id)
        if result.get("Success"):
            return {"Success": True, "message": "Transaction deleted successfully!"}
        return {"Success": False, "message": f"Error: {result.get('error')}"}