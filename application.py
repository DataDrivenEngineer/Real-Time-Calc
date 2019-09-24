import eventlet
eventlet.monkey_patch()

import os, functools

from flask import Flask, render_template, url_for, redirect, request, g, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Calculation
from sqlalchemy import desc

from flask_socketio import SocketIO, send, emit

# Method that returns configred Flask app

def create_application():
    application = Flask(__name__.split('.')[0])

    application.config.from_mapping(
            SECRET_KEY='dev'
            )

    # Import config from config.py file
    application.config.from_pyfile('config.py', silent = True)

    # Mount the Flask app to SQLAlchemy instance
    db.init_app(application)

    # Definition of possible routes

    # Decorator to prevent accessing login-only routes
    def require_login(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if not g.user:
                return redirect(url_for('log_in'))
            return view(**kwargs)
        return wrapped_view

    # Get current user 
    
    @application.before_request
    def load_user():
        user_id = session.get('user_id')
        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

    
    # Return 404 page to unknown routes
    @application.errorhandler(404)
    def page_not_found(error):
        return 'Page not found', 404

    @application.route('/sign_up', methods=('GET', 'POST'))
    def sign_up():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken.'

            if error is None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))

            flash(error, 'error')

        return render_template('sign_up.html')

    @application.route('/log_in', methods=('GET', 'POST'))
    def log_in():
        print('Entered log_in() method...')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            user = db.session.query(User).filter_by(username=username).first() 

            if not user or not check_password_hash(user.password, password):
                error = 'Username or password are incorrect'

            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('calc_index'))

            flash(error, category='error')
        return render_template('log_in.html')

    @application.route('/log_out', methods=('GET', 'DELETE'))
    def log_out():
        session.clear()
        flash('Successfully logged out.', 'success')
        return redirect(url_for('log_in'))
    
    @application.route('/')
    def index():
        return redirect(url_for('calc_index'))    

    @application.route('/calc')
    @require_login
    def calc_index():
        print('Entered calc_index method()...')
        equations = get_initial_equations()
        return render_template('calc_index.html', equations=equations)
    
    return application

# Main begins

application  = create_application()

# Intitializing Flask-SocketIO with eventlet

socketio = SocketIO(application, logger=True, engineio_logger=True)

# Get previous equations from db
def get_initial_equations():
    with application.app_context():
        initial_equations = db.session.query(Calculation).order_by(Calculation.created_at.desc()).limit(10).all()
        equations = []
        if initial_equations:
            for item in initial_equations:
                socketio.sleep()
                equations.append(item.body)
        return equations

# Definition of websocket messages

@socketio.on_error
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

@socketio.on('connect')
def connected():
    print('client connected: ' + str(session['user_id']))

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected: ' + str(session['user_id']))    

# Main method, used for 2 things:
#   1) When a client completes an equation, it is emitted to all other connected clients
#   2) New equation is added to the database

@socketio.on('json')
def get_new_equation_item(someJson):
    try:
        #Sharing new equation with all other clients
        print('Entered get_newequation_item() nethod...')
        send(someJson, json=True, broadcast=True, include_self=False)

        #Adding new equation to the database
        print('adding new equation item to db:' + someJson["emitItem"])
        equation_item = Calculation(body=someJson["emitItem"])
        db.session.add(equation_item)
        db.session.commit()
        print('added')
    except:
        error = "Incorrect data from the client"
        flash(error, 'error')
        return render_template('calc_index.html')

# Initialization method, it is used for extracting previous equations to be displayed on client login

@socketio.on('initialization')
def initialize_equation_items(emptyJson):
    equations = get_initial_equations()
    emit('initial equations', {'equations': equations}, json=True, broadcast=True)

# Start eventlet webserver

if __name__ == '__main__':
    socketio.run(application)
