import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# A small database is created automatically the first time the app runs.
DB_NAME = "club_events.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            description TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            registered_on TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    """)

    # Add a few sample events only when the events table is empty.
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:
        sample_events = [
            ("Math Quiz", "2026-11-05", "A short quiz covering general mathematics."),
            ("Puzzle Hour", "2026-11-12", "Solve logic puzzles with other students."),
            ("Number Theory Talk", "2026-11-20", "An informal introduction to number theory.")
        ]
        cur.executemany(
            "INSERT INTO events (title, event_date, description) VALUES (?, ?, ?)",
            sample_events
        )

    conn.commit()
    conn.close()


def get_events():
    conn = connect_db()
    data = pd.read_sql_query(
        "SELECT id, title, event_date, description FROM events ORDER BY event_date",
        conn
    )
    conn.close()
    return data


def get_registrations():
    conn = connect_db()
    data = pd.read_sql_query("""
        SELECT registrations.id, events.title AS event,
               registrations.student_name, registrations.student_email,
               registrations.registered_on
        FROM registrations
        JOIN events ON registrations.event_id = events.id
        ORDER BY registrations.registered_on DESC
    """, conn)
    conn.close()
    return data


def main():
    st.set_page_config(page_title="Math Club Event Manager", page_icon="➗", layout="wide")
    setup_database()

    st.title("➗ Mathematics Club Event Manager")
    st.write("A simple place to view club events and register for them.")
    st.caption("Student project prototype • Sample event data is included")

    events = get_events()
    registrations = get_registrations()

    total_events = len(events)
    total_registrations = len(registrations)
    st.metric("Events listed", total_events)
    st.metric("Student registrations", total_registrations)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Upcoming Events", "Register", "Club Records"])

    with tab1:
        st.subheader("Events")
        if events.empty:
            st.info("There are no events yet.")
        else:
            for _, event in events.iterrows():
                with st.container(border=True):
                    st.subheader(event["title"])
                    st.write("**Date:**", event["event_date"])
                    st.write(event["description"] or "No description added.")

    with tab2:
        st.subheader("Register for an event")
        if events.empty:
            st.warning("Please add an event before registering.")
        else:
            event_options = {
                f'{row["title"]} — {row["event_date"]}': int(row["id"])
                for _, row in events.iterrows()
            }

            with st.form("registration_form"):
                chosen_event = st.selectbox("Choose an event", list(event_options.keys()))
                student_name = st.text_input("Your name")
                student_email = st.text_input("College email or contact email")
                submitted = st.form_submit_button("Submit registration")

                if submitted:
                    if not student_name.strip() or not student_email.strip():
                        st.error("Please fill in both your name and email.")
                    elif "@" not in student_email or "." not in student_email:
                        st.error("Please enter a valid email address.")
                    else:
                        conn = connect_db()
                        cur = conn.cursor()
                        cur.execute("""
                            SELECT id FROM registrations
                            WHERE event_id = ? AND lower(student_email) = lower(?)
                        """, (event_options[chosen_event], student_email.strip()))
                        already_registered = cur.fetchone()

                        if already_registered:
                            st.warning("This email is already registered for that event.")
                        else:
                            cur.execute("""
                                INSERT INTO registrations
                                (event_id, student_name, student_email, registered_on)
                                VALUES (?, ?, ?, ?)
                            """, (
                                event_options[chosen_event],
                                student_name.strip(),
                                student_email.strip(),
                                date.today().isoformat()
                            ))
                            conn.commit()
                            st.success("Registration saved. See you at the event!")
                        conn.close()

    with tab3:
        st.subheader("Club records")
        st.write("This section is for the club team to check registrations.")
        if registrations.empty:
            st.info("No registrations have been submitted yet.")
        else:
            st.dataframe(registrations, use_container_width=True, hide_index=True)
            csv_data = registrations.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download registrations as CSV",
                data=csv_data,
                file_name="club_registrations.csv",
                mime="text/csv"
            )

        st.divider()
        st.subheader("Add an event")
        with st.form("add_event_form"):
            new_title = st.text_input("Event name", key="new_title")
            new_date = st.date_input("Event date", value=date.today(), key="new_date")
            new_description = st.text_area("Short description", key="new_description")
            add_event = st.form_submit_button("Add event")

            if add_event:
                if not new_title.strip():
                    st.error("Please enter an event name.")
                else:
                    conn = connect_db()
                    conn.execute(
                        "INSERT INTO events (title, event_date, description) VALUES (?, ?, ?)",
                        (new_title.strip(), new_date.isoformat(), new_description.strip())
                    )
                    conn.commit()
                    conn.close()
                    st.success("Event added. Refresh the page if it does not appear immediately.")


if __name__ == "__main__":
    main()
