# Title : Track My Money

# Description :– 

    A Python-based personal finance management application with Supabase integration. Users can securely log in, record daily expenses across multiple categories, visualize spending trends with charts, and receive intelligent feedback to make informed budgeting decisions.

# Features :-

    1. User Authentication 🔑 – Secure login and registration with private accounts for each user.

    2. Add & Manage Expenses 💰 – Record, edit, or delete daily expenses with date, category, amount, and notes.

    3. Expense Categorization 🗂️ – Track spending across categories like Food, Travel, Bills, Shopping, and Others.

    4. Data Storage in Supabase ☁️ – Store user and expense data securely in a cloud database with multi-user support.

    5. Data Visualization 📊 – Generate pie charts (and optionally bar/line charts) for expense trends.

    6. Feedback & Insights 💡 – Provide intelligent alerts and suggestions based on spending patterns and budgets.


# Project Structure :-
    TrackMyMoney/
    |
    |---src/            #core Application logic
    |   |---logic.py    #Business logic and task
    operations
    |   |__db.py        #Database Operations
    |
    |---API/            #Backend API
    |   |main.py        #FastApi endpoints
    |
    |---frontend/       #frontend Application
    |   |__app.py       #Stremlit web interface
    |
    |___requiremnets.txt  #Python dependencies
    |
    |___README.md       #Project Documentation
    |
    |___.env            #Python Variables


# Quick Start :-
## Prerequisites

    - Python 3.8 or higher
    - A superbase Account
    - Git (push,cloning)
##1. Clone or download the porject
    option 1: clone with git
        git clone <repository-url>
    option 2: Download and extract the ZIP file
##2. Install Dependencies
    #Install all required python packages
        pip install -r requirements.txt
##3. Set up SupaBase DataBase
    1. Create a supabase Project:

    2. Create the Tasks Table:

    -> Go to the sql editor in your supabase dashboard
    -> Run this Sql Command:
        CREATE TABLE tasks (
            id BIGSERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date DATE NOT NULL,
            priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    3. **Get Your Credentials**

##4. Configure Environmental Variables
    1. create a ".env" file in the project root

    2. Add your supabase credentials to ".env" :
        SUPABASE_URL="https://uwznjoflnjcjjdzggbqg.supabase.co"
        SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3em5qb2ZsbmpjampkemdnYnFnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNDQsImV4cCI6MjA3MzY1ODA0NH0.Klw4Zw0BOml-pxQnsjLTTbUtdgUXz11YTnk_DhlpZIo"
###5. Run the Application

    ## . Streamlit Frontend
        stremlit run frontend/app.py

        The app will open in your browswer at `http://localhost:8080`

    ## Fast API Backend
        cd API
        python main.py

        The app will be available at `http://localhost:8091`

    ## How To Use:

        1. Open the Application – Launch the Streamlit frontend (app.py).

        2. Register or Login – Create a new account or log in with your credentials.

        3. Add Expenses – Enter your daily expenses by selecting a category, amount, and optional note.

        4. View Charts – Generate visual charts to see your spending distribution.

        5. Get Feedback – Receive insights and suggestions to manage your budget better.

        6. Repeat Daily – Keep adding expenses and watch your spending patterns over time.



    ## Technical Details :

    ## Technologies Used :

        -**Frontend**: Stremlit (Python Web Framework)
        -**Backend**: FastAPI (Python Rest API Framework)
        -**Database**: Supabase (PostgreSQL-based backend-as-a-service)
        -**Language**: Python 3.8+

    ## Key Components :
        1. **`src/db.py`** : Database Operations 
            -Handles all CRUD Operations with supabase
        
        2. **`src/logic.py`** : Business Logic 
            - Task validation and Processing

    ## Troble Shooting :

        1. Supabase Connection – Check .env for correct URL & API key; ensure project is active.

        2. Missing Python Modules – Run pip install -r requirements.txt and select correct Python interpreter.

        3. Login Issues – Verify user exists in Supabase and passwords match.

        4. Expenses Not Saving – Ensure user_id is correct and API is running.

        5. Charts Not Displaying – Check data isn’t empty and use st.pyplot(fig) in Streamlit.

        6. FastAPI Errors – Confirm endpoints exist and server is running with uvicorn API.main:app --reload.

    ## Common Issues : 
        1. **Module Not FOund Errors**
            -Make sure you've installed all dependencies `pip install -r requirments.txt`
            -check that you're runnuing commands from the correct Directory 
        

    ##Future Enhancement : 

        1. Multi-Currency Support – Allow users to log expenses in different currencies and convert automatically.

        2. Recurring Expenses – Automatically add regular expenses like rent, subscriptions, and EMIs.

        3. Advanced Analytics – Provide monthly/yearly trends, category-wise spending patterns, and predictive insights.

        4. Notifications & Alerts – Notify users when they exceed budget limits or when bills are due.

        5. Export Reports – Export expenses and charts as PDF, Excel, or CSV files.

        6. Mobile App Integration – Extend the application to Android/iOS for on-the-go tracking.

        7. Custom Categories – Let users create their own expense categories.

        8. Goal Tracking – Allow users to set savings goals and track progress.

        9. Dark Mode / UI Enhancements – Improve frontend appearance and usability.

        10. Data Backup & Restore – Enable users to back up and restore their data securely.

##Support : 

    If you encounter any issues or have questions: 
    contact : 6301466251
    email : gouthamreddybijjam630@gmail.com
