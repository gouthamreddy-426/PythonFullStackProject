# frontend/app.py - COMPLETE WITH AUTHENTICATION

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date, datetime
import time
import random

st.set_page_config(page_title="Track My Money", page_icon="💰", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
    }
    div[data-baseweb="select"] input {
        cursor: pointer !important;
        user-select: none !important;
        pointer-events: none !important;
    }
    .stSelectbox {
        cursor: pointer !important;
    }
    div[role="listbox"] li {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

# BASE_API_URL = "http://127.0.0.1:8000"
BASE_API_URL = "https://pythonfullstackproject-l13w.onrender.com"
API_URL = f"{BASE_API_URL}/transactions"

# ============================= SESSION STATE =============================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# ============================= AUTH FUNCTIONS =============================
def register_user(email, password):
    try:
        response = requests.post(f"{BASE_API_URL}/auth/register", json={"email": email, "password": password})
        return response
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Cannot connect to API server")
        return None
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return None

def login_user(email, password):
    try:
        response = requests.post(f"{BASE_API_URL}/auth/login", json={"email": email, "password": password})
        return response
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Cannot connect to API server")
        return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def logout_user():
    try:
        requests.post(f"{BASE_API_URL}/auth/logout")
    except:
        pass
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.rerun()

# ============================= LOGIN/SIGNUP PAGE =============================
if not st.session_state.logged_in:
    st.title("🔐 Track My Money")
    st.markdown("### Manage Your Finances Securely")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="your@email.com")
            password = st.text_input("🔒 Password", type="password")
            login_btn = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if login_btn:
                if email and password:
                    with st.spinner("Logging in..."):
                        response = login_user(email, password)
                    if response and response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = data['user']['id']
                        st.session_state.user_email = data['user']['email']
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                else:
                    st.error("❌ Please fill in all fields")
    
    with tab2:
        st.subheader("Create Your Account")
        with st.form("signup_form"):
            new_email = st.text_input("📧 Email", placeholder="your@email.com", key="signup_email")
            new_password = st.text_input("🔒 Password (min 6 characters)", type="password", key="signup_password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            signup_btn = st.form_submit_button("📝 Create Account", use_container_width=True)
            
            if signup_btn:
                if new_email and new_password and confirm_password:
                    if len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        with st.spinner("Creating account..."):
                            response = register_user(new_email, new_password)
                        if response and response.status_code == 200:
                            st.success("✅ Account created! Please login.")
                            time.sleep(2)
                            st.rerun()
                        else:
                            if response:
                                try:
                                    error_msg = response.json().get('detail', 'Registration failed')
                                except:
                                    error_msg = f"Registration failed (Status: {response.status_code})"
                            else:
                                error_msg = "❌ Connection error: Cannot connect to API server. Please make sure the API is running."
                            st.error(f"❌ {error_msg}")
                else:
                    st.error("❌ Please fill in all fields")
    
    st.stop()

# ============================= MAIN APP (AFTER LOGIN) =============================
st.title("💰 Track My Money")

# Sidebar with user info and logout
with st.sidebar:
    st.success(f"👤 **{st.session_state.user_email}**")
    if st.button("🚪 Logout", use_container_width=True, type="primary"):
        logout_user()
    st.markdown("---")

# ============================= HELPER FUNCTIONS =============================
def fetch_transactions():
    """Fetch transactions for the logged-in user only"""
    try:
        response = requests.get(f"{API_URL}/{st.session_state.user_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def generate_financial_insights(df):
    if df.empty:
        return None
    
    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    net_balance = total_income - total_expense
    
    insights = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'savings_rate': 0,
        'financial_status': '',
        'recommendations': [],
        'category_analysis': {},
        'spending_warnings': [],
        'achievement_badges': []
    }
    
    if total_income > 0:
        insights['savings_rate'] = (net_balance / total_income) * 100
    
    savings_rate = insights['savings_rate']
    
    if savings_rate >= 20:
        insights['financial_status'] = "🌟 Excellent Saver!"
        insights['recommendations'] = [
            f"🎉 Outstanding! You're saving {round(savings_rate, 1)}% of your income!",
            "💡 Consider investing your surplus",
            "🎯 You're on track for financial security"
        ]
        insights['achievement_badges'].append("🏆 Elite Saver")
    elif savings_rate >= 10:
        insights['financial_status'] = "💚 Good Financial Health"
        insights['recommendations'] = [
            f"✅ Great! Saving {round(savings_rate, 1)}% of income",
            "🎯 Try to reach 20% savings rate",
            "💡 Look for areas to cut expenses"
        ]
        insights['achievement_badges'].append("🥈 Good Saver")
    elif savings_rate >= 0:
        insights['financial_status'] = "⚠️ Breaking Even"
        insights['recommendations'] = [
            f"📊 Saving {round(savings_rate, 1)}% - room for improvement",
            "🎯 Aim for 10-20% savings",
            "💡 Review expense categories"
        ]
    else:
        insights['financial_status'] = "🚨 Overspending Alert"
        insights['recommendations'] = [
            f"⚠️ Spending {abs(round(savings_rate, 1))}% more than earning!",
            "🛑 Reduce expenses immediately",
            "📝 Create a strict budget"
        ]
    
    expense_df = df[df["type"] == "expense"]
    if not expense_df.empty:
        category_spending = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
        insights['category_analysis'] = category_spending.to_dict()
    
    return insights

def display_enhanced_feedback(insights):
    if not insights:
        return
    
    st.header("🎯 Financial Health Report")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Income", f"${insights['total_income']:,.2f}")
    with col2:
        st.metric("💸 Expenses", f"${insights['total_expense']:,.2f}")
    with col3:
        delta_color = "normal" if insights['net_balance'] >= 0 else "inverse"
        st.metric("💵 Net Savings", f"${insights['net_balance']:,.2f}", 
                 delta=f"{insights['savings_rate']:.1f}%", delta_color=delta_color)
    
    if insights['savings_rate'] >= 10:
        st.success(f"**{insights['financial_status']}**")
    elif insights['savings_rate'] >= 0:
        st.warning(f"**{insights['financial_status']}**")
    else:
        st.error(f"**{insights['financial_status']}**")
    
    if insights['achievement_badges']:
        st.info(f"{insights['achievement_badges'][0]}")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(insights['recommendations'][:4], 1):
            st.write(f"{i}. {rec}")
    
    with col_right:
        if insights['category_analysis']:
            st.subheader("📊 Top Spending")
            sorted_cats = sorted(insights['category_analysis'].items(), key=lambda x: x[1], reverse=True)[:3]
            for cat, amt in sorted_cats:
                pct = (amt / insights['total_income'] * 100) if insights['total_income'] > 0 else 0
                color = "🔴" if pct > 25 else "🟡" if pct > 15 else "🟢"
                st.write(f"{color} **{cat}**: ${amt:,.2f} ({pct:.1f}%)")
        
        st.subheader("💰 Quick Tips")
        tips = ["☕ Make coffee at home", "🍽️ Meal prep weekly", "💳 Pay bills on time", "🛒 Compare prices"]
        for tip in tips:
            st.caption(tip)

# ============================= NAVIGATION =============================
st.sidebar.title("🧭 Navigation")
operation = st.sidebar.selectbox(
    "Choose Operation",
    ["📊 Dashboard", "➕ Add Transaction", "📝 Update Transaction", "🗑️ Delete Transaction", "📋 View All"]
)

# ============================= DASHBOARD =============================
if operation == "📊 Dashboard":
    st.header("📊 Financial Dashboard")
    
    transactions = fetch_transactions()
    
    if transactions:
        df = pd.DataFrame(transactions)
        
        st.subheader("📈 Visual Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Income vs Expense**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            type_summary = df.groupby("type")["amount"].sum()
            colors = ["#4CAF50" if idx == "income" else "#F44336" for idx in type_summary.index]
            type_summary.plot.pie(autopct='%1.1f%%', ax=ax1, startangle=90, colors=colors, labels=type_summary.index.str.title())
            ax1.set_ylabel("")
            st.pyplot(fig1)
        
        with col2:
            st.markdown("**Expenses by Category**")
            expense_df = df[df["type"] == "expense"]
            if not expense_df.empty:
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                cat_exp = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
                cat_exp.plot.bar(ax=ax2, color="#FF9800")
                ax2.set_xlabel("Category")
                ax2.set_ylabel("Amount ($)")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig2)
            else:
                st.info("No expense data")
        
        st.markdown("---")
        insights = generate_financial_insights(df)
        display_enhanced_feedback(insights)
    else:
        st.info("📂 No transactions. Add your first one!")

# ============================= ADD TRANSACTION =============================
elif operation == "➕ Add Transaction":
    st.header("➕ Add New Transaction")
    
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title*", placeholder="e.g., Salary, Groceries")
            amount = st.number_input("Amount*", min_value=0.01, step=0.01, format="%.2f")
            category = st.text_input("Category*", placeholder="e.g., Food, Income")
        
        with col2:
            trans_type = st.selectbox("Type*", ["expense", "income"])
            date_input = st.date_input("Date*", value=date.today())
            notes = st.text_area("Notes", placeholder="Optional details...")
        
        submit = st.form_submit_button("💾 Add Transaction", use_container_width=True)
        
        if submit:
            if title and amount > 0 and category:
                payload = {
                    "title": title,
                    "amount": amount,
                    "category": category,
                    "type": trans_type,
                    "date": str(date_input),
                    "notes": notes or "",
                    "user_id": st.session_state.user_id
                }
                
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        st.success("✅ Transaction added!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
            else:
                st.error("❌ Please fill required fields")

# ============================= VIEW ALL =============================
elif operation == "📋 View All":
    st.header("📋 All Transactions")
    
    transactions = fetch_transactions()
    
    if transactions:
        df = pd.DataFrame(transactions)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox("Type", ["All", "income", "expense"])
        with col2:
            cats = ["All"] + list(df['category'].unique())
            filter_cat = st.selectbox("Category", cats)
        with col3:
            sort_by = st.selectbox("Sort by", ["date", "amount", "title"])
        
        # Apply filters
        filtered = df.copy()
        if filter_type != "All":
            filtered = filtered[filtered["type"] == filter_type]
        if filter_cat != "All":
            filtered = filtered[filtered["category"] == filter_cat]
        filtered = filtered.sort_values(sort_by, ascending=False)
        
        st.subheader(f"📊 {len(filtered)} transactions")
        
        # Display
        for _, row in filtered.iterrows():
            with st.expander(f"{'📈' if row['type']=='income' else '📉'} {row['title']} - ${row['amount']:,.2f}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Category:** {row['category']}")
                col2.write(f"**Date:** {row['date']}")
                col3.write(f"**Type:** {row['type'].title()}")
                if row.get('notes'):
                    st.write(f"**Notes:** {row['notes']}")
    else:
        st.info("📂 No transactions found")

# ============================= UPDATE TRANSACTION =============================
elif operation == "📝 Update Transaction":
    st.header("📝 Update Transaction")
    
    transactions = fetch_transactions()
    
    if transactions:
        trans_opts = {f"{t['title']} - ${t['amount']} ({t['date']})": t for t in transactions}
        selected = st.selectbox("Select Transaction", list(trans_opts.keys()))
        trans = trans_opts[selected]
        
        with st.form("update_form"):
            st.subheader(f"Updating: {trans['title']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_title = st.text_input("Title", value=trans['title'])
                new_amount = st.number_input("Amount", value=float(trans['amount']), min_value=0.01, step=0.01)
                new_category = st.text_input("Category", value=trans['category'])
            
            with col2:
                new_type = st.selectbox("Type", ["expense", "income"], 
                                      index=0 if trans['type'] == 'expense' else 1)
                current_date = datetime.strptime(trans['date'], '%Y-%m-%d').date()
                new_date = st.date_input("Date", value=current_date)
                new_notes = st.text_area("Notes", value=trans.get('notes', ''))
            
            update_btn = st.form_submit_button("💾 Update Transaction", use_container_width=True)
            
            if update_btn:
                update_data = {
                    "title": new_title,
                    "amount": new_amount,
                    "category": new_category,
                    "type": new_type,
                    "date": str(new_date),
                    "notes": new_notes
                }
                
                try:
                    response = requests.put(
                        f"{API_URL}/{trans['id']}/{st.session_state.user_id}", 
                        json=update_data
                    )
                    if response.status_code == 200:
                        st.success("✅ Transaction updated!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
    else:
        st.info("📂 No transactions to update")

# ============================= DELETE TRANSACTION =============================
elif operation == "🗑️ Delete Transaction":
    st.header("🗑️ Delete Transaction")
    
    transactions = fetch_transactions()
    
    if transactions:
        df = pd.DataFrame(transactions)
        
        st.warning("⚠️ Deleted transactions cannot be recovered!")
        
        for _, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    icon = "📈" if row['type'] == 'income' else "📉"
                    st.write(f"{icon} **{row['title']}** - ${row['amount']:,.2f} | {row['category']} | {row['date']}")
                    if row.get('notes'):
                        st.caption(f"Notes: {row['notes']}")
                
                with col2:
                    delete_key = f"delete_confirm_{row['id']}"
                    
                    if st.session_state.get(delete_key, False):
                        if st.button("⚠️ CONFIRM", key=f"final_{row['id']}", type="secondary"):
                            try:
                                response = requests.delete(f"{API_URL}/{row['id']}/{st.session_state.user_id}")
                                if response.status_code == 200:
                                    st.success("✅ Deleted!")
                                    st.session_state[delete_key] = False
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Error deleting")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                        
                        if st.button("❌ Cancel", key=f"cancel_{row['id']}"):
                            st.session_state[delete_key] = False
                            st.rerun()
                    else:
                        if st.button("🗑️ Delete", key=f"delete_{row['id']}", type="secondary"):
                            st.session_state[delete_key] = True
                            st.rerun()
                
                st.divider()
    else:
        st.info("📂 No transactions to delete")

# ============================= FOOTER =============================
st.markdown("---")
st.markdown("### 📊 Quick Stats")
col1, col2, col3 = st.columns(3)

transactions = fetch_transactions()

with col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

with col2:
    st.metric("Total Transactions", len(transactions))

with col3:
    if transactions:
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        net = total_income - total_expense
        st.metric("Net Balance", f"${net:,.2f}")