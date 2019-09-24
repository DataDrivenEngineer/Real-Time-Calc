# Real Time Calculator

## Description

A real time calculator that logs calculations as they happen and immediately shares them with everyone connected to the app

## Use case

1. User A and user B log in at the same time
2. User A calculates "5 + 5", which equals "10". This is logged as "5+5 = 10"
3. New calculation is immediately displayed to User B
4. Now, user B calculates "3x4". This calculates to 12 and displays "3x4=12"
5. This calculation is immediately displayed to User A
6. All equations are stored in the database. However, only 10 most recent equations are displayed in the logging box

## Tech stack

- Server side: Flask-SocketIO (eventlet)
- Client side: VueJS + Socket.IO
- Database: PostgreSQL 9.6.8 running locally in the Docker container

## Installation

The app is currently pending deployment to GUnicorn + Nginx and can only be run locally in development mode.

For local installation:
1. Run postgres96-install-docker.sh script (see project folder) to configure docker and launch PostgreSQL 9.6.8 container
2. Define environment variables to match config.py
3. Ensure that you have Python 3.6+ installed
4. Run `pip install -r requirements.txt`
5. Run `python -i application.py` and open `http://localhost:5000` in the browser
