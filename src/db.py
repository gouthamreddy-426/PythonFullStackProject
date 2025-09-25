import os
from supabase import create_client
from dotenv import load_dotenv

#load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url,key)

#create Transaction
def create_transaction(title,amount,category,type_,date,notes):
    return supabase.table("transactions").insert({
        "title":title,
        "amount":amount,
        "category":category,
        "type":type_,
        "date":date,
        "notes":notes,
    }).execute()

#retrieve transactions
def get_all_transactions():
    return supabase.table("transactions").select("*").execute()

#update transactions
def update_transactions(transaction_id,updated_data:dict):
    return supabase.table("transactions").update(updated_data).eq("id",transaction_id).execute()

#delete Transactions
def delete_transactions(transaction_id):
    return supabase.table("transactions").delete().eq("id",transaction_id).execute()