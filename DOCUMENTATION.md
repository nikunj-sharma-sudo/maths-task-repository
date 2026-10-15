# Project Documentation: Mathematics Club Event Manager

## 1. Problem identified
The Mathematics Club runs quizzes, workshops and other events. If registrations are collected manually through messages or separate forms, it can take extra time to organise the names and check the number of participants.

## 2. Proposed solution
I made a small web app where students can view events and register for them. The club team can see all registrations together and download the list when needed.

## 3. Features implemented
- View event names, dates and descriptions.
- Register for an event using a name and email.
- Basic checks for empty fields and email format.
- Prevent duplicate registration with the same email for the same event.
- View the registration list.
- Download registrations as a CSV file.
- Add new events.

## 4. Technologies used
- **Python** is used for the logic and database operations.
- **Streamlit** is used to build the web interface without needing to write HTML or JavaScript.
- **SQLite** stores events and registrations in a local database file.
- **Pandas** helps show the records in a table and export them.

## 5. How I tested it
1. Started the app and checked that the sample events appeared.
2. Registered with a name and email.
3. Tried submitting the form with missing details.
4. Tried registering the same email for the same event again.
5. Checked that the registration appeared in Club Records.
6. Tested the CSV download.
7. Added a new event.

## 6. Future improvements
- Add a login for club organisers.
- Allow students to cancel a registration.
- Add attendance marking on event day.
- Send a confirmation email.
- Host the app online so the club can use it from different devices.

## 7. Current limitations
- The prototype stores its database locally.
- There is no login system, so it should not be used for sensitive information.
- Email checking is basic and does not send a verification email.

## 8. Demo plan
1. Open the Upcoming Events tab.
2. Register for the Math Quiz using a test name and email.
3. Open Club Records and show the new registration.
4. Download the CSV file.
5. Add a sample event to show that the list can be updated.

Use test details for the demo rather than real student contact information.
