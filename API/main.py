# API/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import TransactionManager

# ------------------- App Setup -------------------
app = FastAPI(title="Track My Money API with Auth", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transaction_manager = TransactionManager()

# ------------------- Schemas -------------------
class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TransactionCreate(BaseModel):
    title: str
    amount: float
    category: str
    type: str
    date: str
    notes: str | None = None
    user_id: str

class TransactionUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    category: str | None = None
    type: str | None = None
    date: str | None = None
    notes: str | None = None

# ------------------- Authentication Endpoints -------------------
@app.get("/")
def home():
    return {"message": "Track My Money API with Authentication 🚀"}

@app.post("/auth/register")
def register(user: UserRegister):
    """Register a new user"""
    result = transaction_manager.register_user(user.email, user.password)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/auth/login")
def login(user: UserLogin):
    """Login user"""
    result = transaction_manager.login_user(user.email, user.password)
    print(f"Login attempt for {user.email}: {result}")  # ADD THIS LINE
    if not result.get("Success"):
        raise HTTPException(status_code=401, detail=result.get("message"))
    return result

@app.post("/auth/logout")
def logout():
    """Logout user"""
    result = transaction_manager.logout_user()
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ------------------- Transaction Endpoints -------------------
@app.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    """Add a new Transaction"""
    result = transaction_manager.add_transaction(
        transaction.title,
        transaction.amount,
        transaction.category,
        transaction.type,
        transaction.date,
        transaction.notes,
        transaction.user_id
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/transactions/{user_id}")
def get_transactions(user_id: str):
    """Retrieve all transactions for a specific user"""
    return transaction_manager.get_transactions(user_id)

@app.put("/transactions/{transaction_id}/{user_id}")
def update_transaction(transaction_id: int, user_id: str, updated_data: TransactionUpdate):
    """Update a transaction by ID (only user's own)"""
    result = transaction_manager.change_transaction(
        transaction_id, updated_data.dict(exclude_none=True), user_id
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/transactions/{transaction_id}/{user_id}")
def delete_transaction(transaction_id: int, user_id: str):
    """Delete a transaction by ID (only user's own)"""
    result = transaction_manager.remove_transaction(transaction_id, user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result