from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from src.main.spotifyapi import add_song
from src.main.formattime import format_time

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'music.db')
app.config['SECRET_KEY'] = 'allofmeng'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Song(db.Model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=True)
    songlength = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String, nullable=True)  # Adjust to nullable if desired
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')
        try:
            song_info = add_song(url)
            # Create a new song and add it to the database
            new_song = Song(
                title=song_info['title'],
                artist=song_info['artist'],
                album=song_info['album'],
                songlength=song_info['length'],
                user_id=current_user.id
            )
            db.session.add(new_song)
            db.session.commit()
            flash(song_info['message'], 'success')  # Flash the success message
            return jsonify({'success': True, 'song_info': song_info})
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')  # Flash the error message
            return jsonify({'success': False, 'error': str(e)}), 400

    # GET request
    songs = Song.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', songs=songs , format_time = format_time)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        print(f"Received registration attempt: username={username}, email={email}")

        if not username or not email or not password or not confirm_password:
            flash('All fields are required')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        try:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists')
                return redirect(url_for('register'))

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already in use')
                return redirect(url_for('register'))

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"User registered successfully: username={username}, email={email}")
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {str(e)}")
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))
@app.route('/edit_song/<int:song_id>', methods=['POST'])
@login_required
def edit_song(song_id):
    song = Song.query.get_or_404(song_id)
    if song.user_id != current_user.id:
        return jsonify(success=False, error="You don't have permission to edit this song"), 403

    data = request.json
    song.title = data['title']
    song.artist = data['artist']
    song.album = data['album']
    song.songlength = request.json.get('length', song.songlength)
    song.notes = data['notes']

    try:
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500

@app.route('/delete_song/<int:song_id>', methods=['POST'])
@login_required
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    if song.user_id != current_user.id:
        return jsonify(success=False, error="You don't have permission to delete this song"), 403

    try:
        db.session.delete(song)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500






if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Tables created successfully")

            # Check if tables exist
            inspector = db.inspect(db.engine)
            for table_name in inspector.get_table_names():
                print(f"Table '{table_name}' exists")
                columns = inspector.get_columns(table_name)
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    app.run(debug=True)
