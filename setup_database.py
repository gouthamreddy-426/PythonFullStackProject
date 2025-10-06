#!/usr/bin/env python3
"""
Database setup script to create the transactions table in Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def setup_database():
    """Create the transactions table if it doesn't exist"""
    load_dotenv()
    
    # Use default credentials if .env file doesn't exist
    url = os.getenv("SUPABASE_URL", "https://uwznjoflnjcjjdzggbqg.supabase.co")
    key = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3em5qb2ZsbmpjampkemdnYnFnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNDQsImV4cCI6MjA3MzY1ODA0NH0.Klw4Zw0BOml-pxQnsjLTTbUtdgUXz11YTnk_DhlpZIo")
    
    try:
        client: Client = create_client(url, key)
        print("✅ Connected to Supabase successfully!")
        
        # SQL to create the transactions table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id BIGSERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
            date DATE NOT NULL,
            notes TEXT,
            user_id UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create an index on user_id for better performance
        CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
        
        -- Create an index on date for better performance
        CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
        """
        
        # Execute the SQL
        result = client.rpc('exec_sql', {'sql': create_table_sql})
        print("✅ Database table setup completed!")
        print("📋 Created table: transactions")
        print("📋 Created indexes for better performance")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("💡 Please run this SQL in your Supabase SQL Editor:")
        print("""
        CREATE TABLE IF NOT EXISTS transactions (
            id BIGSERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
            date DATE NOT NULL,
            notes TEXT,
            user_id UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
        CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
        """)
        return False

if __name__ == "__main__":
    setup_database()
