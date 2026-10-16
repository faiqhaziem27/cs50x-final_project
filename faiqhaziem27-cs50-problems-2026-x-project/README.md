#STUDYIQ - Personalized Study Tracker
#### Video Demo: https://youtu.be/PJ0ruDKGlNk
#### Description: StudyIQ is a full-stack web application made with Python, Flask, SQLite and Bootstrap that works as a study and productivity tracker for students. The application has an easy to use dashboard where students can record study hours look at past learning trends manage account security and keep their schedules in one place.

## Key Features

* **User Authentication**: Secure user registration, password hashing and user login tracking using Flask sessions.

* **Session Logging**: A input system that lets users record subjects, study times and personal progress notes.

* **Interactive Dashboard**: A visual summary that brings together total study time and shows metrics when a user logs in.

* **Chronological History**: A table that gets user- records from the SQLite database to show past learning milestones.

* **Account Customization**: A password change feature that lets users update their profile settings easily.

## Technical Design Choices

During development several choices were made to make the user experience better and keep the data safe:

1. **Flask & Python**: Flask was selected because of its size, which makes it simple to use for backend routing and quick use with Jinja templates.

2. **SQLite**: Tables were made in a SQLite file (`study.db`) to handle one-to-many relationships between a single user profile and many study sessions quickly.

3. **Bootstrap & Custom CSS**: Bootstrap was used to make sure the design works on all devices while custom CSS was used to create a multi-color navbar and smooth hover effects on dashboard cards.

## Project Structure and Core Files

To meet the CS50x project requirements the project is divided into several key files:

* **app.py: The main backend part of the application. It starts the Flask app sets up the database connection and sets up all the main routes (`/` `/login` `/register` `/add` `/history` and `/change_password`) to handle user requests form submissions and database queries.

* **helpers.py**: Has custom functions used throughout the application the `login_required` decorator that stops unauthorized users from accessing private routes and keeps tracking data safe.

* **study.db**: The SQLite database file that keeps user account details (including hashed passwords) and study tracking records in a relational format.

* **templates/layout.html**: The main layout template made with HTML and Jinja. It gives a look to all pages a responsive navigation bar and includes scripts and styles, for other sub-pages.

* **templates/index.html**: The dashboard page that users see when they log in showing their study overview, summary metrics and welcome messages.

* **templates/add.html**: A form that lets users safely add study sessions or time allocations directly to the database.

* **templates/history.html**: A page that gets data from the database to show a time-based view of past study logs and productivity records.

* **templates/login.html & templates/register.html**: forms that help users sign up log in and create secure sessions.

* **static/style.css**: The custom style sheet that handles the apps look including responsive changes, spacing and card effects.

## How to Run the Application

1. Make sure all needed parts (Flask, CS50 library) are installed in your workspace.

2. Open your terminal. Go to the project folder that has `app.py`.

3. Start the web server by running:

```bash

flask run

```

4. Click on the server link that appears in the terminal to use StudyIQ in your browser.
