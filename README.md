# Mathematics Club Event Manager

This is a small beginner-level project for managing Mathematics Club events.

## Problem
Club events can be announced in different places, and collecting registrations manually can get confusing. It is also harder to check how many students signed up.

## What the prototype does
- Shows a list of events.
- Lets a student register for an event with their name and email.
- Stops the same email from registering twice for the same event.
- Shows the registrations in one place.
- Lets the club team download the registration list as a CSV file.
- Lets the club team add a new event.

## Technology used
- Python: main application logic
- Streamlit: simple web interface
- SQLite: saves events and registrations locally
- Pandas: displays and exports records

## How to run it

You need Python installed on your computer.

1. Extract this folder.
2. Open a terminal or Command Prompt inside the folder.
3. Install the packages:

   `python -m pip install -r requirements.txt`

4. Start the app:

   `python -m streamlit run app.py`

5. Open the local address shown in the terminal (usually `http://localhost:8501`).

The database file `club_events.db` is created automatically when you run the app.

## Notes
This is a prototype for a college club, not a production system. The records are stored on the computer where the app runs. It does not yet have club-admin accounts or online hosting.
